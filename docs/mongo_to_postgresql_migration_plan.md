# MongoDB -> PostgreSQL データ移行計画書

## 1. 目的
既存の MongoDB 運用データを、要件起点で再設計した PostgreSQL スキーマへ安全に移行する。

## 2. 移行対象
主要コレクション:
- `line_users`
- `groups`
- `group_settings`
- `matches`
- `hanchans`
- `user_matches`
- `user_hanchans`
- `user_groups`
- `web_users`
- `command_aliases`
- `yakuman_users`

## 3. 移行方針
- 方針: **リハーサル2回 + 本番1回の段階移行**
- 方式: **バッチ移行（停止時間あり）**
- 整合性: 変換ルールを固定し、検証SQLで件数/合計値を照合
- ロールバック: 切替前バックアップと read-only フェーズで保証

## 4. 事前準備
1. PostgreSQL 環境作成（Cloud SQL or AlloyDB）
2. 新スキーマ作成（`postgresql_db_design_spec.md`）
3. マイグレーションツール導入（Alembic等）
4. MongoDB ダンプ手順確立
5. リハーサル用データセット作成
6. 移行判定基準（Go/No-Go）合意

## 5. マッピング定義

## 5.1 コレクション -> テーブル
- `line_users` -> `players`
- `groups` -> `groups`
- `group_settings` -> `group_settings`
- `user_groups` -> `group_memberships`
- `matches` -> `matches` + `match_settlements`（展開）
- `hanchans` -> `hanchans` + `hanchan_scores`（展開）
- `user_matches` -> `match_participants`
- `user_hanchans` -> `hanchan_scores` の補完情報（rank/yakumanなど）

## 5.2 主な変換ルール
1. `ObjectId` は直接保持しない。必要なら `legacy_mongo_id` を別列で保持
2. `status` の数値（0/1/2）は文字列 enum へ変換
3. `raw_scores`, `converted_scores` の Map は `(hanchan_id, line_user_id)` 行に展開
4. `match.sum_scores`, `sum_prices*`, `chip_scores`, `chip_prices` は `(match_id, line_user_id)` 行に展開
5. `created_at`, `updated_at` が欠損している場合は `now()` 補完（補完件数をログ化）
6. `line_user_id` 未登録データは `players` へ先行作成（名前は null 許容）

## 6. 実行フェーズ

## 6.1 フェーズA: スキーマ構築
1. DDL適用
2. インデックス作成
3. 初期整合性チェック（FK/UNIQUE）

## 6.2 フェーズB: リハーサル移行
1. Mongoダンプ取得
2. 変換バッチ実行
3. PostgreSQLロード
4. 検証実行
5. 差分分析と変換ロジック修正

## 6.3 フェーズC: 本番移行
1. メンテナンス告知
2. 書き込み停止（LINE Botをメンテモードへ）
3. 最終ダンプ取得
4. 変換/ロード
5. 検証完了後、アプリを PostgreSQL 接続で起動
6. read-only 監視期間（短時間）
7. 通常運用へ復帰

## 7. 検証計画

## 7.1 件数照合
- `line_users` 件数 = `players` 件数
- `groups` 件数 = `groups` 件数
- `hanchans` 件数 = `hanchans` 件数
- `raw_scores` のキー総数 = `hanchan_scores` 行数（raw分）
- `sum_scores` のキー総数 = `match_settlements` 行数（sum_score分）

## 7.2 数値照合
- 半荘単位で `raw_score` 合計が移行前後一致
- 対戦単位で `sum_score` 合計が移行前後一致
- chip関連 (`chip_score`, `chip_price`) の一致

## 7.3 業務照合
- `_matches` 表示結果の一致
- `_match {index}` の結果一致
- `_ranking`, `_rank`, `_rank_detail` の表示整合

## 8. ロールバック計画
1. 切替後に重大不整合が判明した場合、アプリ接続先を MongoDB に戻す
2. PostgreSQL 側データは退避して調査
3. 原因修正後に再リハーサルを実施
4. 再切替判断を再承認

## 9. リスクと対策
- リスク: Map展開時の欠損/重複
  - 対策: 変換前後のキー件数照合SQLを必須化
- リスク: キー不整合（`user_id` と `line_user_id` の混在）
  - 対策: 移行中に `line_user_id` を正として再解決テーブルを作成
- リスク: 切替時間超過
  - 対策: 事前リハーサルで処理時間上限を確定
- リスク: 移行後のクエリ性能不足
  - 対策: 主要クエリの EXPLAIN を事前実施し索引追加

## 10. 作業成果物
1. 変換仕様書（本書）
2. 変換スクリプト（ETL）
3. 検証SQLセット
4. 移行実施ログ
5. 切替判定チェックリスト

## 11. 実装タスク（次アクション）
1. ETLスクリプト雛形作成（collectionごと）
2. 検証SQLファイル作成
3. stagingでリハーサル1回目
4. 差分修正
5. stagingでリハーサル2回目
6. 本番移行日程確定

## 12. 実行コマンド例
```bash
# 0) 接続確認
POSTGRES_DATABASE_URL='postgresql://<user>:<pass>@<host>:5432/<db>' \
python3 scripts/migration/check_postgres_connection.py

# 1) スキーマ適用
POSTGRES_DATABASE_URL='postgresql://<user>:<pass>@<host>:5432/<db>' \
alembic upgrade head

# 2) ETL（まずは dry-run）
POSTGRES_DATABASE_URL='postgresql://<user>:<pass>@<host>:5432/<db>' \
EXTERNAL_DATABASE_URL='mongodb://...' \
DATABASE_NAME='<mongo_db>' \
python3 scripts/migration/mongo_to_postgres_etl.py --dry-run

# 3) 本実行
POSTGRES_DATABASE_URL='postgresql://<user>:<pass>@<host>:5432/<db>' \
EXTERNAL_DATABASE_URL='mongodb://...' \
DATABASE_NAME='<mongo_db>' \
python3 scripts/migration/mongo_to_postgres_etl.py

# 4) 検証SQL
psql "$POSTGRES_DATABASE_URL" -f scripts/migration/sql/verify_migration.sql
```
