# Firestore バックアップ・DR 手順

## 目的

本番データ（`mahjang-manager` プロジェクトの Firestore, MongoDB compatibility mode）を手動でバックアップ・復旧するための手順をまとめる。

## 現状の方針

**自動バックアップ・Point-in-Time Recovery (PITR) は現時点では有効化していない**（継続課金が発生するため）。まずは無料の手動エクスポート手順を整備し、必要になった時点で自動化を検討する。将来 PITR や定期エクスポートを自動化する場合は、GCP公式料金ページで最新の単価を確認したうえで概算費用を提示し、判断してから有効化する。

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

## 将来の自動化について

自動バックアップ・PITR を有効化する場合は、以下を GCP 公式料金ページで確認したうえで、費用をユーザーに提示してから実施する:

- PITR: 有効化すると読み取り・書き込み課金に加えてバージョン保持のためのストレージ課金が発生する
- 定期エクスポートの Cloud Scheduler + Cloud Functions/Run 化: 実行自体はほぼ無料枠内だが、エクスポート先ストレージの継続課金は上記と同様
