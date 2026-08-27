# Firestore バックアップ・DR 手順

## 目的

本番データ（`mahjang-manager` プロジェクトの Firestore, MongoDB compatibility mode）を手動でバックアップ・復旧するための手順をまとめる。

## 現状の方針

2026-08-27、**Firestoreネイティブの「スケジュールバックアップ」機能を有効化済み**（本番DBのみ、週次・SUNDAY・保持期間28日）。PITR（継続的ポイントインタイム復旧）ではなくスケジュールバックアップを採用した理由: ストレージ単価がPITRの約1/5、かつCloud Scheduler/Cloud Functions等の追加インフラが不要なため。本サービスの利用規模（少人数・週1回程度）ではストレージ費用は月額数円未満の見込み。詳細は下記「自動スケジュールバックアップ」を参照。

これとは別に、一括編集操作の直前など任意タイミングでの手動エクスポート手順も引き続き以下に残す（スケジュールバックアップの粒度（週次）では拾えない直前状態を保存したい場合に使う）。

## 前提

- `gcloud` CLI が対象プロジェクト（`mahjang-manager`）に対する権限を持つアカウントで認証済みであること
- 対象データベース ID（`<DATABASE_ID>`）は本番の `DATABASE_URL`（Secret Manager 管理、`mongodb://...@<UID>.<LOCATION>.firestore.goog:443/<DATABASE_ID>?...`）から確認する。または以下で一覧取得できる:

  ```bash
  gcloud firestore databases list --project=mahjang-manager
  ```

- エクスポート先の GCS バケットが必要（未作成の場合は下記「GCS バケットの作成」を参照）

## 手動エクスポート手順

```bash
PROJECT_ID="mahjang-manager"
DATABASE_ID="<DATABASE_ID>"          # 上記で確認した値に置き換える
BUCKET="gs://mahjang-manager-firestore-backup"  # 未作成なら先にバケットを作成する
TIMESTAMP=$(date +%Y%m%dT%H%M%S)

gcloud firestore export "${BUCKET}/${TIMESTAMP}" \
  --project="${PROJECT_ID}" \
  --database="${DATABASE_ID}"
```

実行後、`${BUCKET}/${TIMESTAMP}` にエクスポートが作成される。完了まで数分かかることがある（`gcloud firestore operations list --project="${PROJECT_ID}"` で進捗確認可能）。

## リストア手順

**注意**: `import` は対象コレクションの既存データを上書きする。本番データベースへ直接リストアする前に、可能であればテスト用データベース（`mahjong-manager-test` 等）で復元内容を確認すること。

```bash
gcloud firestore import "${BUCKET}/${TIMESTAMP}" \
  --project="${PROJECT_ID}" \
  --database="${DATABASE_ID}"
```

## GCS バケットの作成（未作成の場合）

初回のみ、エクスポート先バケットを作成する。実行前にユーザーに確認すること（ストレージ課金が発生するため）。

```bash
gcloud storage buckets create gs://mahjang-manager-firestore-backup \
  --project=mahjang-manager \
  --location=asia-northeast1 \
  --uniform-bucket-level-access
```

**概算費用の目安**（2026-07時点、GCP公式料金ページで実施前に最新値を要確認）: Standard Storage は東京リージョンで約 $0.023/GiB/月。本サービスの想定データ規模（少人数・週1回程度の利用、`pico/projects/mahjong-manager-bot.md` 記載）であれば、エクスポート1回あたり数MB〜数十MB程度で、月100円未満の見込み。古いエクスポートを世代管理せず溜め続けると徐々に増えるため、[ライフサイクルルール](https://cloud.google.com/storage/docs/lifecycle)で一定期間後に自動削除する設定を検討する。

## 推奨頻度

- 月次（手動）を目安とする
- 加えて、`update_hanchan_scores` / `delete_match` 等の一括編集操作（FEZ-30 で追加した Web 編集機能）をまとめて行う前など、リスクの高い操作の直前に取得する

## 自動スケジュールバックアップ

2026-08-27に設定。設定内容:

```bash
gcloud firestore backups schedules create \
  --project=mahjang-manager \
  --database=mahjong-manager \
  --recurrence=weekly \
  --day-of-week=SUN \
  --retention=28d
```

- 対象は本番DB（`mahjong-manager`）のみ。`mahjong-manager-test` には設定していない
- 毎週日曜に自動作成、作成から28日後に自動削除（世代管理不要）
- 料金体系: バックアップのストレージサイズ × 保持日数の按分 × 単価（$0.00004〜0.00007/GiB・月程度、東京リージョン）で計算される。データ量が小さいうちは月額数円未満
- 設定確認: `gcloud firestore backups schedules list --project=mahjang-manager --database=mahjong-manager`
- バックアップ一覧確認: `gcloud firestore backups list --project=mahjang-manager --location=asia-northeast1`
- リストア: `gcloud firestore databases restore --source-backup=<backup name> --destination-database=<復元先DB> --project=mahjang-manager`（既存DBには直接復元できず、新規または別DBへの復元となる点に注意。本番へ反映する場合は復元後にデータ移行の追加作業が必要）
- 単価・仕様変更の可能性があるため、保持期間や頻度を変更する場合は [Firestore Enterprise pricing](https://cloud.google.com/firestore/enterprise/pricing) で最新値を確認してから変更する
