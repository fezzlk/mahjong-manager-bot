# Firestore (MongoDB compatibility) 運用メモ

## 目的
本プロジェクトを、Cloud Run + Firestore (MongoDB compatibility) で運用するための最小設定をまとめる。

## 前提
- このコードベースは `pymongo` を使用している
- そのため Firestore は **MongoDB compatibility** を使う
- Firestore Native mode を使う場合は repository 層の全面改修が必要

## 必須環境変数
```env
FLASK_APP=src/server
FLASK_ENV=production

YOUR_CHANNEL_ACCESS_TOKEN=...
YOUR_CHANNEL_SECRET=...

DATABASE_URL=mongodb://<UID>.<LOCATION>.firestore.goog:443/<DATABASE_ID>?loadBalanced=true&tls=true&retryWrites=false
DATABASE_NAME=...

SERVER_URL=https://<your-cloud-run-service>.run.app
SERVER_ADMIN_LINE_USER_ID=...
```

## 接続URLの注意点
`src/mongo_client.py` で以下の3パラメータを必須チェックしている。
- `loadBalanced=true`
- `tls=true`
- `retryWrites=false`

不足すると起動時に例外となる。

## Cloud Run デプロイ時の要点
1. 公開アクセスは許可（LINE Webhook受信用）
2. コンテナポートは `8080`
3. `SERVER_URL` は実際の Cloud Run URL に合わせる
4. Secret Manager を使って LINE token/secret, DB URL を注入する

## コスト運用メモ
- Firestore は従量課金中心（アイドル時の固定費が Cloud SQL より軽い）
- 読み取り回数が多いエンドポイントは集計結果を再利用して read 削減する

