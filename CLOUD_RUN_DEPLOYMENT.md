# Cloud Run デプロイメント手順

このドキュメントでは、麻雀マネージャーボットを Google Cloud Run にデプロイする手順を説明します。

## 前提条件

1. Google Cloud Platform アカウント
2. Google Cloud SDK (gcloud) のインストール
3. Docker のインストール
4. プロジェクトの作成と課金の有効化

## 1. 事前準備

### 1.1 Google Cloud プロジェクトの設定

```bash
# プロジェクトIDを設定
export PROJECT_ID="your-gcp-project-id"

# プロジェクトを設定
gcloud config set project $PROJECT_ID

# 必要なAPIを有効化
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable containerregistry.googleapis.com
```

### 1.2 認証設定

```bash
# Google Cloudにログイン
gcloud auth login

# Docker認証を設定
gcloud auth configure-docker
```

## 2. データベース設定

### 2.1 MongoDB Atlas の設定

1. [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)でアカウントを作成
2. クラスターを作成
3. データベースユーザーを作成
4. ネットワークアクセスを設定（Cloud Run の IP アドレスを許可）
5. 接続文字列を取得

### 2.2 環境変数の設定

`env.cloudrun.example`を参考に、実際の環境変数を設定してください：

```bash
# 重要な環境変数
EXTERNAL_DATABASE_URL=mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority
YOUR_CHANNEL_ACCESS_TOKEN=your_line_channel_access_token
YOUR_CHANNEL_SECRET=your_line_channel_secret
SERVER_URL=https://your-cloud-run-url.run.app
```

## 3. デプロイ方法

### 方法 1: 自動デプロイスクリプトを使用

```bash
# deploy.shのプロジェクトIDを編集
vim deploy.sh

# デプロイを実行
./deploy.sh
```

### 方法 2: 手動デプロイ

```bash
# 1. Dockerイメージをビルド
docker build -t gcr.io/$PROJECT_ID/mahjong-manager-bot .

# 2. Container Registryにプッシュ
docker push gcr.io/$PROJECT_ID/mahjong-manager-bot

# 3. Cloud Runにデプロイ
gcloud run deploy mahjong-manager-bot \
  --image gcr.io/$PROJECT_ID/mahjong-manager-bot \
  --platform managed \
  --region asia-northeast1 \
  --allow-unauthenticated \
  --memory 1Gi \
  --cpu 1 \
  --max-instances 10 \
  --timeout 300 \
  --set-env-vars FLASK_ENV=production,PORT=8080
```

### 方法 3: Cloud Build を使用

```bash
# Cloud Buildでデプロイ
gcloud builds submit --config cloudbuild.yaml .
```

## 4. 環境変数の設定

Cloud Run コンソールまたは gcloud コマンドで環境変数を設定：

```bash
gcloud run services update mahjong-manager-bot \
  --region asia-northeast1 \
  --set-env-vars \
    FLASK_ENV=production,\
    PORT=8080,\
    YOUR_CHANNEL_ACCESS_TOKEN=your_token,\
    YOUR_CHANNEL_SECRET=your_secret,\
    EXTERNAL_DATABASE_URL=your_mongodb_url,\
    DATABASE_NAME=your_db_name,\
    SERVER_URL=https://your-service-url.run.app
```

## 5. デプロイ後の確認

### 5.1 サービス URL の確認

```bash
gcloud run services describe mahjong-manager-bot \
  --region asia-northeast1 \
  --format 'value(status.url)'
```

### 5.2 ログの確認

```bash
gcloud logs tail --service mahjong-manager-bot
```

### 5.3 ヘルスチェック

```bash
curl https://your-service-url.run.app/
```

## 6. トラブルシューティング

### 6.1 よくある問題

1. **データベース接続エラー**

   - MongoDB Atlas のネットワークアクセス設定を確認
   - 接続文字列の形式を確認

2. **LINE Bot の応答エラー**

   - Channel Access Token と Channel Secret が正しいか確認
   - Webhook URL が正しく設定されているか確認

3. **メモリ不足エラー**
   - Cloud Run のメモリ設定を 1Gi 以上に増やす

### 6.2 ログの確認

```bash
# リアルタイムログ
gcloud logs tail --service mahjong-manager-bot

# 特定の時間範囲のログ
gcloud logs read --service mahjong-manager-bot --since 1h
```

## 7. 継続的デプロイの設定

### 7.1 GitHub Actions の設定

`.github/workflows/deploy.yml`を作成：

```yaml
name: Deploy to Cloud Run

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - name: Setup Google Cloud SDK
        uses: google-github-actions/setup-gcloud@v0
        with:
          service_account_key: ${{ secrets.GCP_SA_KEY }}
          project_id: ${{ secrets.GCP_PROJECT_ID }}

      - name: Deploy to Cloud Run
        run: |
          gcloud builds submit --config cloudbuild.yaml .
```

## 8. セキュリティ考慮事項

1. **環境変数の管理**

   - 機密情報は Google Secret Manager を使用
   - 環境変数ではなく、シークレットとして管理

2. **ネットワークセキュリティ**

   - 必要に応じて認証を有効化
   - VPC コネクタの使用を検討

3. **データベースセキュリティ**
   - MongoDB Atlas の IP ホワイトリスト設定
   - データベースユーザーの権限最小化

## 9. コスト最適化

1. **インスタンス設定**

   - 最小インスタンス数を 0 に設定
   - 最大インスタンス数を適切に設定

2. **リソース設定**
   - 必要最小限のメモリと CPU を設定
   - タイムアウト設定の最適化

---

この手順に従って、麻雀マネージャーボットを Cloud Run にデプロイできます。
