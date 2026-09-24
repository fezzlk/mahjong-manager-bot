# LINE Bot(グループ)全ユースケース一覧

`src/use_cases/group_line/`配下の全37ファイルおよび`src/routing_by_text_in_group_line.py`の実装を直接読んで作成。推測は排除し、コードで確認できた事実のみを断定的に記載する。確認できなかった点は「要確認」と明記する。

2026-09-22作成。FEZ-168システムテストの準備中に実施したコマンド単位のボタン導線棚卸しを、ユーザー視点のユースケース単位に再編し、前提条件・処理フロー・結果まで踏み込んで整理したもの。

2026-09-23、[FEZ-234](https://linear.app/fezzlk/issue/FEZ-234)のメニュー再設計に合わせて更新。以降の記述は各PRの反映状況に合わせて更新する。

## メニュー構造(FEZ-234)

配置の原則:
- **QuickReply**: 直後の一手・確認・取り消し・一覧からの選択など、そのメッセージを見ている時にしか押さない操作(他のメッセージが挟まると消える)
- **ButtonsTemplate**: 会話履歴に残り、時間が空いても押せる操作(最大4アクション)
- **FlexCarousel**: 4件を超えるメニュー。会話履歴に残る

| メニュー | 形式 | 項目 |
|---|---|---|
| スタートメニュー | ButtonsTemplate | 結果を入力 / 精算 / 対戦管理 / 設定 |
| 対戦管理(`_others`) | FlexCarousel(2枚) | 「進行中の対戦」: 途中経過を確認・新しい対戦を始める・シミュレーション / 「戦績」: 成績推移・対戦履歴・累計得点表・順位表・個人の順位推移・個人の順位分布 |

隠しコマンド(メニューに出さない): `_fortune`、`_mode`

トリガー分類は以下の3種:
- **A(ボタンのみ)**: 実際のユーザーは手打ちしない
- **B(最初の一手だけ手打ち)**: 起点のみ手打ち、以降はボタン
- **C(手打ちのみ)**: ボタン導線が存在しない

---

## 1. グループにBotを招待する(初期化)

- **トリガー**: LINEグループへのBot招待(`JoinEvent`)。ユーザー操作ではなくシステムイベント
- **前提条件**: なし
- **処理の流れ**: `group_service.find_or_create()`でGroupドキュメントを作成→`line_bot_api.get_group_summary()`でグループ名・アイコン取得を試み(`ApiException`時はログ警告のみで継続)→固定の案内メッセージ3件を送信→スタートメニューを自動表示
- **結果**: Groupドキュメント新規作成。スタートメニュー(下記2)が自動表示される
- **関連ファイル**: `src/use_cases/group_line/join_group_use_case.py`、`src/handle_event.py`(JoinEvent登録)

## 2. スタートメニューを表示する

- **トリガー**: A。グループ参加時に自動送信(上記1) + 精算確認メニュー「いいえ」ボタン(`data="_start"`) + Botへのメンション(下記32) + `_start`手打ちでも可
- **前提条件**: なし
- **処理の流れ**: `reply_service.add_start_menu()`を呼ぶのみ。「結果を入力」「精算」「対戦管理」「設定」の4ボタンを提示
- **結果**: ボタン付きメッセージ1通
- **関連ファイル**: `src/use_cases/group_line/reply_start_menu_use_case.py`

## 3. 結果を入力する(半荘の点数入力を開始する)

- **トリガー**: A。スタートメニュー「結果を入力」(`_input`) + open対戦2件以上時のピッカー選択(`_input_select?to=`)
- **前提条件**: `group.mode != input`(既に入力モード中なら「すでに入力モードです。」で終了)
- **処理の流れ**:
  1. open状態(`status=open`)のMatchを`line_group_id`で検索
  2. **0件**: 確認なしで新規Match作成→入力開始(黙って続行)
  3. **1件**: そのMatchへ即座に入力開始
  4. **2件以上**: 対戦名一覧+「新しい対戦を始める」(→`_new_match`)のQuick Replyピッカーを提示。選択後`_input_select?to=<match_id>`で該当対戦の入力開始
  5. 入力開始時、`group.mode`を`input`に更新(DB書き込み)→対象Matchの`active_hanchan_id`があればそれを使用、なければ新規Hanchan作成→「第N回戦お疲れ様です。各自点数を入力してください。」を返信
  6. モード更新を先に行い、その後にMatch/Hanchan作成を行う実装(`_input`直後にほぼ同時に数値が送られるレース条件対策として意図的にこの順序)
- **結果**: `Group.mode=input`、`Group.current_input_match_id`が対象Matchを指す。新規対戦なら`Match`ドキュメント新規作成
- **関連ファイル**: `src/use_cases/group_line/start_input_use_case.py`

## 4. 点数を入力する(半荘結果の確定まで)

- **トリガー**: C(数値テキスト直接送信。ボタンなし。ただし直前に`_input`実行済みならモードが`input`のためコマンド判定を経ず自動的にこのユースケースへ渡る=事実上「入力モード中のテキストは全てこれ」という意味では自然なフロー)
- **前提条件**: `Group.mode == input`
- **処理の流れ**: `InputPointUseCase`でテキストから対象ユーザー(メンション)と点数を抽出→`Group.current_input_match_id`が指すMatchの`active_hanchan_id`のHanchanへ`raw_scores`を追加/上書き(同一ユーザーの再入力は上書き、`@[ユーザー名]`送信で取り消し)→現在の入力状況を返信→`Match.settings`(なければグループ現在設定)の`num_of_players`と入力済み人数が一致したら「5. 半荘結果を確定する」へ自動遷移。超過時は警告メッセージ
- **結果**: Hanchan.raw_scoresが更新される
- **関連ファイル**: `src/use_cases/group_line/add_point_by_text_use_case.py`、`src/use_cases/utility/input_point_use_case.py`

## 5. 半荘結果を確定する(自動)

- **トリガー**: 上記4の内部から自動呼び出し。ユーザーが直接呼ぶコマンドではない
- **前提条件**: 入力済み点数が`num_of_players`と一致
- **処理の流れ**:
  1. 人数チェック→点数合計チェック(`開始点×人数`〜`+99`の範囲)→同点チェック、いずれか不正なら該当メッセージで中断
  2. マイナス点(飛び)があれば「6. 飛び賞受取者を指定する」へ分岐(`tobashita_player_id`未指定時)
  3. `calculate_service.run()`で得点計算(`Match.settings`優先、なければグループ現在設定にフォールバック=FEZ-66 Phase D)
  4. `try_clear_active_hanchan()`でこの半荘確定処理の所有権をアトミックに確保(同時到達対策)。失敗時は何もせず終了(既に他プロセスが処理中)
  5. Hanchan.converted_scores更新、User/UserGroup/UserMatchの作成、Match.sum_scores更新、Hanchan.results(embedded)保存
  6. DB書き込み中の例外時: `try_clear_active_hanchan`でクリアした状態を復元し再試行可能にした上で管理者へPush通知
  7. 結果表示後`Group.mode=wait`に戻し、スタートメニューを再表示
- **結果**: Hanchan確定、Match.sum_scores更新、GroupModeがwaitに戻る
- **関連ファイル**: `src/use_cases/group_line/submit_hanchan_use_case.py`

## 6. 飛び賞受取者を指定する

- **トリガー**: A(飛びが発生した半荘確定時に自動提示されるボタン、`data="_tobi " + player_id`)
- **前提条件**: 上記5の途中で、マイナス点のプレイヤーが存在
- **処理の流れ**: `SubmitHanchanUseCase().execute(tobashita_player_id=body)`を再実行(飛び賞受取者を指定した状態で計算)
- **結果**: 上記5と同じ
- **関連ファイル**: `src/routing_by_text_in_group_line.py`(`_tobi`関数)、`src/use_cases/group_line/submit_hanchan_use_case.py`

## 7. 新しい対戦(系列)を明示的に開始する

- **トリガー**: A。対戦管理メニュー「新しい対戦を始める」(`_new_match`) + open対戦2件以上時のピッカーの「新しい対戦を始める」ボタン
- **前提条件**: `Group.mode != input`
- **処理の流れ**: `_new_match`でグループ現在設定を反映した確認ボタン(「作成する」)提示→`_new_match_confirm`で新規Match作成し即座に入力開始(`StartInputUseCase.enter_match()`を再利用)。既存のopen対戦数に関わらず常に1件追加
- **結果**: 新規Matchドキュメント作成、入力開始
- **関連ファイル**: `src/use_cases/group_line/new_match_use_case.py`

## 8. 精算する

- **トリガー**: A。スタートメニュー「精算」(`_finish_confirm`)→確認ボタン「はい」(`_finish`) + open対戦2件以上時のピッカー(`_finish_select?to=`)
- **前提条件**: 対象対戦が`status=open`
- **処理の流れ**:
  1. open対戦検索。**0件**: 「計算対象の試合が見つかりません。」。**1件**: 即座に精算。**2件以上**: ピッカー提示
  2. 他のopen対戦が入力セッション中(`current_input_match_id`が別対戦を指す)場合は精算をブロックし「先に完了するか`_exit`で中断してください」
  3. アーカイブ済みHanchanが0件なら「まだ対戦結果がありません。」
  4. `Match.settings`(対戦作成時の設定)優先でレート計算。`chip_rate != 0`かつまだチップ精算していなければ「9. チップ精算」へ分岐
  5. `sum_scores`×レートで`sum_prices`算出、`Match.status=settled`に更新
  6. このMatchが入力セッション対象だった場合のみ`Group.mode=wait`・`current_input_match_id=None`に戻す(他対戦のセッションには触れない)
  7. 複数系列を実際に使ったことがあるグループ(`count_non_sim_by_line_group_id > 1`)のみ対戦名を結果表示に含める
  8. 対戦detail画像(グラフ)を生成・送信
- **結果**: Match.status=settled、sum_prices確定
- **関連ファイル**: `src/use_cases/group_line/finish_match_use_case.py`、`create_match_detail_graph_use_case.py`

## 9. チップを精算する

- **トリガー**: A(精算確認ボタン。上記8の内部フローから提示)
- **前提条件**: `Group.mode == chip_input`
- **処理の流れ**: チップ増減の合計が0でなければ警告して中断。0なら`Group.mode=chip_ok`に更新→`FinishMatchUseCase().finish_pending_chip()`で改めて精算(この対戦は必ず`current_input_match_id`が指す対戦自身のため、open件数分岐は不要)
- **結果**: 上記8の精算処理が完了
- **関連ファイル**: `src/use_cases/group_line/finish_input_chip_use_case.py`

## 10. チップの増減枚数を入力する

- **トリガー**: C(数値テキスト直接送信。`Group.mode == chip_input`中の全テキストがこれに渡る)
- **前提条件**: `Group.mode == chip_input`
- **処理の流れ**: `InputPointUseCase`でユーザーと枚数を抽出→`Match.chip_scores`へ追加/上書き→現状を返信
- **結果**: Match.chip_scores更新
- **関連ファイル**: `src/use_cases/group_line/add_chip_by_text_use_case.py`

## 11. 途中経過を確認する

- **トリガー**: A。対戦管理メニュー「途中経過を確認」(`_active_match`) + open対戦2件以上時のピッカー(`_active_match_select?to=`)
- **前提条件**: なし(0件時は専用メッセージ)
- **処理の流れ**: open対戦検索。**0件**: 「現在進行中の対戦がありません。」。**1件**: 即座に表示。**2件以上**: ピッカー提示→対象対戦のアーカイブ済みHanchan一覧+累計スコア+推移グラフを表示。「第N回の半荘の削除は`_drop N`」の案内文言あり
- **結果**: なし(閲覧のみ)
- **関連ファイル**: `src/use_cases/group_line/reply_hanchans_of_active_match_use_case.py`

## 12. 過去の対戦一覧を見る

- **トリガー**: A。対戦管理メニュー「対戦履歴」(`_matches`)
- **前提条件**: なし
- **処理の流れ**: `status=settled`かつ`is_deleted=False`のMatch一覧取得(0件なら「まだ対戦結果がありません。」)→複数系列使用歴があれば対戦名を、なければ日付のみのリストを表示。「`_match N`」で詳細を見る案内
- **結果**: なし
- **関連ファイル**: `src/use_cases/group_line/reply_matches_use_case.py`

## 13. 対戦の詳細を見る

- **トリガー**: **C**(`_match N`、ボタン導線なし。番号は上記12の一覧を見て手打ちする前提の設計)
- **前提条件**: `1 <= N <= 精算済み対戦数`
- **処理の流れ**: 該当Matchの`settings`(精算時点。旧データはグループ現在設定にフォールバック)で結果表示を組み立て、半荘ごとの内訳・グラフを表示
- **結果**: なし
- **関連ファイル**: `src/use_cases/group_line/reply_match_by_index_use_case.py`

## 14. 現在の対戦の半荘を削除する

- **トリガー**: **C**(`_drop N`、ボタン導線なし。上記11の途中経過表示に「第N回の半荘の削除は`_drop N`」という案内文言があるのみでボタンではない)
- **前提条件**: `Group.current_input_match_id`が設定されている(=入力中の対戦がある)。`1 <= N <= 現在対戦のアーカイブ済み半荘数`
- **処理の流れ**: 該当Hanchanを`is_deleted=True`に更新するのみ(物理削除ではない)
- **結果**: Hanchan.is_deleted=True
- **関連ファイル**: `src/use_cases/group_line/drop_hanchan_by_index_use_case.py`

## 15. 対戦(系列)自体を再オープンする

- **トリガー**: **B**。`_reopen`(手打ち)→直近5件の精算済み対戦からのQuick Reply選択(`_reopen_confirm?to=`はボタン)
- **前提条件**: `status=settled`のMatchが1件以上存在(直近5件のみ選択肢に出す)
- **処理の流れ**: 選択したMatchの`sum_prices`/`chip_prices`/`sum_prices_with_chip`をリセットし`status=open`に戻す。グループの入力セッション状態(`current_input_match_id`/`mode`)には一切触れない設計(他の並行入力セッションを壊さないため)
- **結果**: Match.status=open、精算結果クリア
- **関連ファイル**: `src/use_cases/group_line/reopen_match_use_case.py`

## 16. グループ設定を見る・変更する

- **トリガー**: A。スタートメニュー「設定」(`_setting`)→階層ボタン(レート/順位点/チップ/飛び賞、端数計算方法/ゲスト)→`_update_config <key> <value>`(ボタンのdata値として送信されるため実質ボタン)
- **前提条件**: なし
- **処理の流れ**: `_setting`(body="")で現在設定一覧を表示しつつメニュー1のボタン提示。各項目ボタンでサブメニュー(値の選択肢)を表示、選択すると`_update_config`が呼ばれ値を検証(レート:0/1/2/3/4/5/10、チップ:0/1、飛び賞:0/10/20/30、順位点:人数分のカンマ区切り、端数計算方法:定義済みリスト内、単位:10文字以内の任意文字列)して`GroupSetting`を更新
- **結果**: GroupSettingドキュメント更新
- **関連ファイル**: `src/use_cases/group_line/reply_group_settings_menu_use_case.py`、`update_group_settings_use_case.py`

## 17. 人数(3人/4人麻雀)を変更する

- **トリガー**: **C**。`_update_config 人数 3`(または4)。**`_setting`メニューに人数のボタンは存在しない**(コード確認済み: `reply_service.py`のボタン定義に「人数」文言なし)。FEZ-167システムテストチェックリストは「`_setting`から人数を変更できる」と記載しているが誤り。`UpdateGroupSettingsUseCase`自体は`key == "人数"`のハンドラを持ち3/4を受け付けるため(`update_group_settings_use_case.py:52`で確認済み)機能自体は存在するが、到達手段が手打ちのみ
- **前提条件**: `value`が3または4
- **処理の流れ**: 上記16と同じ`UpdateGroupSettingsUseCase`経由
- **結果**: GroupSetting.num_of_players更新
- **関連ファイル**: `src/use_cases/group_line/update_group_settings_use_case.py`

## 18. ゲストを追加する

- **トリガー**: A。設定メニュー2「ゲスト」(`_setting ゲスト`)→ゲスト管理メニュー「追加」ボタン(`_guest_add`)
- **前提条件**: なし
- **処理の流れ**: `guest_service.register_next()`でグループ内の次の連番(`is_deleted`含む全件の最大値+1、削除後も再利用しない)を採番し`Guest`エンティティ作成
- **結果**: Guest新規作成
- **関連ファイル**: `src/use_cases/group_line/guest_add_use_case.py`

## 19. ゲストを削除する

- **トリガー**: A。ゲスト管理メニュー「削除」ボタン(`_setting ゲスト削除`、登録済みゲストがある場合のみボタン表示)→対象選択Quick Reply(`_guest_remove_confirm?number=`)
- **前提条件**: 削除対象の番号のゲストが存在
- **処理の流れ**: `guest_service.remove()`で該当Guestを削除(見つからなければ「指定されたゲストが見つかりません。」)
- **結果**: Guest削除
- **関連ファイル**: `src/use_cases/group_line/guest_remove_confirm_use_case.py`

## 20. 成績推移を見る(対象・期間選択フロー)

- **トリガー**: A。対戦管理メニュー「成績推移」(`_history_start`)。手打ちの`_history`も同じフローの起点(旧メンション指定版は廃止)→対象選択ボタン(自分だけ/グループ全員/選択する、`_history_target?t=`)→(選択する時のみ)ユーザーカルーセルでトグル選択(`_history_toggle?u=`)→確定ボタン(`_history_confirm`)→期間選択ボタン(今月/先月/3ヶ月/6ヶ月/全期間、`_history_exec?p=`)
- **前提条件**: 「選択する」を選んだ場合、最低1人以上選択が必要(0人のまま確定しようとするとカルーセル再提示)
- **処理の流れ**: 各ステップは`HistorySession`(`line_group_id`+`requester_line_id`キー、per-user状態)に選択状態を保存しながら進行。セッションタイムアウト時(`HistorySession`が見つからない)は全ステップで「タイムアウトしました。対戦管理メニューの「成績推移」から再度お試しください。」。最終ステップで対象ユーザーの`UserMatch`から該当Matchを集計し、累計推移の折れ線グラフを生成
- **結果**: なし(閲覧のみ、`HistorySession`は最後に削除)
- **関連ファイル**: `start_history_flow_use_case.py`、`select_history_target_use_case.py`、`toggle_history_user_use_case.py`、`confirm_history_selection_use_case.py`、`execute_history_use_case.py`

## 21. (廃止)成績推移を見る(メンション一括指定、簡易版)

FEZ-234で上記20に統合した。`_history`は上記20のフローの起点として動作する(`reply_multi_history_use_case.py`は削除)。

## 22. 累計得点表・順位表を見る

- **トリガー**: A。対戦管理メニュー「累計得点表・順位表」(`_ranking`)
- **前提条件**: なし
- **処理の流れ**: このグループで対戦参加歴がある全ユーザー(+送信者)を対象に(FEZ-234で旧メンション指定版を統合)累計スコア・平均順位・最高得点等を集計し、LINEプロフィール画像付きの画像テーブルを2枚(得点表・順位表)生成
- **結果**: なし
- **関連ファイル**: `src/use_cases/group_line/reply_ranking_table_use_case.py`

## 23. 個人の順位履歴・順位分布を見る

- **トリガー**: A。対戦管理メニュー「個人の順位推移」(`_rank`、順位履歴グラフ+平均順位)、「個人の順位分布」(`_rank_detail`、順位ヒストグラム)
- **前提条件**: なし
- **処理の流れ**: 送信者本人の`UserHanchan`を集計し、`_rank`は着順分布の棒グラフ+直近10半荘の順位推移折れ線、`_rank_detail`は着順ごとの時系列ヒストグラムを生成
- **結果**: なし
- **関連ファイル**: `src/use_cases/common_line/reply_rank_history_use_case.py`、`reply_rank_histogram_use_case.py`(group/personal共通)

## 24. 場代を精算する

- **トリガー**: **C**。`_badai <金額>`。ボタン導線なし
- **前提条件**: 直近のMatch(`find_latest_one`、simを除く)が精算済み(`sum_prices_with_chip`が存在)。未精算(進行中)の対戦がある場合は「対戦を終了するには`_finish`」と案内して中断
- **処理の流れ**: 場代を直近対戦の参加人数で割り、端数は1名ずつ多く負担する形で調整して各自の最終金額を再計算・表示
- **結果**: なし(表示のみ、DB更新なし)
- **関連ファイル**: `src/use_cases/group_line/reply_apply_badai_use_case.py`

## 25. グループの成績を他グループへ統合する

- **トリガー**: **B**。`_migrate`(手打ち)→統合先グループ選択Quick Reply(`_migrate_confirm?to=`はボタン)。個人DM版は`_personal_migrate`(パラメータ有無で3ステップ、統合元・統合先ともボタン選択、起点のみ手打ち)
- **前提条件**: 統合先が送信者の参加グループの中に存在し、かつ`merged_into=None`(未統合)。統合元・統合先いずれにも`status=open`のMatchが1件も存在しないこと(あれば「統合元・統合先のいずれかに進行中の対戦があるため統合できません」)
- **処理の流れ**: `group_service.set_merged_into(src, to)`で統合元グループに統合先を記録するのみ(過去データの物理的な付け替えは行わない、ポインタ方式)
- **結果**: Group.merged_into設定
- **関連ファイル**: `src/use_cases/group_line/migrate_group_use_case.py`

## 26. シミュレーションする

- **トリガー**: A。対戦管理メニュー「シミュレーション」(`_sim`)→点数入力(テキスト)
- **前提条件**: `Group.mode != sim`(既にsimモードなら「すでにシミュレーションモードです。」)。結果入力中(`input`/`chip_input`)は開始不可
- **処理の流れ**: `Group.sim_match_id`が指す専用サンドボックスMatch(`status=sim`、実系列の`current_input_match_id`とは完全に独立)がなければ作成→新規Hanchan作成しsimモードへ→点数入力の都度Hanchan.raw_scoresへ反映→人数分揃うと合計チェック・同点チェック(飛び賞は省略)の上で結果表示→Hanchanを`is_deleted=True`にして`Group.mode=wait`に戻す(記録は残らない)
- **結果**: 一時的なHanchan作成後、最終的に`is_deleted=True`(記録として残らない)
- **関連ファイル**: `src/use_cases/group_line/start_sim_use_case.py`、`simulate_score_use_case.py`

## 27. 入力・シミュレーションを中断する

- **トリガー**: **C**。`_exit`。ボタン導線なし(ソースコード上「danger」とコメントされている破壊的操作)
- **前提条件**: グループが登録済み
- **処理の流れ**: `Group.mode`が`sim`だったかどうかで対象(sim_match_idか current_input_match_id)を判定し、`Group.mode=wait`に戻す→対象Matchのactive_hanchan_idをNoneに戻し、該当Hanchanがあれば`is_deleted=True`にする
- **結果**: 入力中/シミュレーション中の未確定半荘が破棄される
- **関連ファイル**: `src/use_cases/group_line/exit_use_case.py`

## 28. 占いを見る

- **トリガー**: **C**。`_fortune`。ボタン導線なし
- **前提条件**: 送信者がLINE友だち登録済み(Userドキュメントが存在)
- **処理の流れ**: `line_user_id`をシードにしたランダムなラッキー牌を1つ表示
- **結果**: なし
- **関連ファイル**: `src/use_cases/common_line/reply_fortune_use_case.py`

## 29. ヘルプ(コマンド一覧)を見る

- **トリガー**: **C**。`_help`。ボタン導線なし
- **前提条件**: なし
- **処理の流れ**: dispatchテーブルに実際に登録されている全コマンド名を機械的に列挙する(`list(dispatch.keys())`をそのまま渡している。個別の説明文はなく単なる名前一覧)
- **結果**: なし
- **関連ファイル**: `src/use_cases/group_line/reply_group_help_use_case.py`

## 30. 現在のモードを確認する

- **トリガー**: **C**。`_mode`。ボタン導線なし(デバッグ用途と見られる)
- **前提条件**: なし
- **処理の流れ**: `Group.mode`の生値(`wait`/`input`/`sim`/`chip_input`等の文字列)をそのまま返信
- **結果**: なし
- **関連ファイル**: `src/use_cases/group_line/reply_group_mode_use_case.py`

## 31. グループから退出させる(Bot自身がグループを退出した時)

- **トリガー**: システムイベント(`LeaveEvent`)。ユーザーがコマンドで呼ぶものではない
- **前提条件**: なし
- **処理の流れ**: 該当`line_group_id`のGroupドキュメントを削除
- **結果**: Group削除
- **関連ファイル**: `src/use_cases/group_line/group_quit_use_case.py`

## 32. Botへのメンションでスタートメニューを再表示する

- **トリガー**: Botへのメンション(`is_self=True`のmentioneeを含む)
- **前提条件**: `Group.mode == wait`かつ他のどの分岐(コマンド・input/sim/chip_inputモード・直前`_input`のレース条件対策)にも一致しない場合のみ
- **処理の流れ**: `request_info_service`がLINE SDKの`UserMentionee.is_self`を見て`is_mention_self`フラグを立て、routing側でこのフラグを見てスタートメニュー相当の応答を返す
- **結果**: なし(閲覧のみ)
- **関連ファイル**: `src/application_service/request_info_service.py`、`src/routing_by_text_in_group_line.py`

---

## 対戦単位の削除・対戦横断の合計集計(`_drop_m` / `_sum_matches`)

FEZ-137で実装済み。対戦詳細画面・対戦履歴一覧への導線はFEZ-234のPR 4/5で追加する。素点一覧の貼り付け登録はPR #272でmainにマージ済み(`AddHanchanByPointsTextUseCase`、コマンドなしで自動判定)。`_add_result`はenumごと廃止。

---

## 要確認事項(コード調査だけでは断定できなかった点)

- `_help`が返す一覧は`dispatch.keys()`の生の列挙のみで、各コマンドの説明・引数形式は含まれない(実際にBotに送って表示を確認するのが確実)
