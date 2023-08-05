# About
麻雀対戦結果管理用 LINE Bot

## Demo
(TBD)
## Try it!
<a href="https://lin.ee/JzAiLbG"><img src="https://scdn.line-apps.com/n/line_add_friends/btn/ja.png" alt="友だち追加" height="36" border="0"></a>

## Features
(TBD)

# For Developer
## Create Your LINE Bot Messaging API Channel
1. LINE Devlopers にてプロバイダ及び messaging API のチャンネルを作成
   - 参考: https://developers.line.biz/ja/services/messaging-api/
   - messaging API 設定にて、応答メッセージを無効, webhook の利用を有効にする
   - LINE App にて友達登録しておく

## Build Server
- Install Python
- Create a virtual env(recommend)
  - `$ python -m venv mmvenv`
- apply the virtual env
  - `$ source mmvenv/bin/activate`
- Install dependencies
  - `$ python -m pip install --upgrade pip`
  - `$ pip install -r requirements.txt`
- Set the env var "FLASK_APP" "src/server"
  - `$ export FLASK_APP="src/server"`
- run flask server
  - `$ flask run`

## Build Mongo DB Container by docker-compose(Recommend)
- Install Docker
- run docker-compose on root directory of mahjong-manager
  - `$ docker-compose up`

## Architecture
### Servers
![SALB_Devlop_Isoflow_Diagram_2021_12_10 (1)](https://github.com/fezzlk/mahjong-manager-bot/assets/38426468/00731ee3-07bd-4e37-958d-2c35cb312b3c)

### Layers
![ScreenShot 2023-08-05 8 58 15](https://github.com/fezzlk/mahjong-manager-bot/assets/38426468/3e980260-48b5-4bcc-b12d-3798c93ba12a)

#### View Layer
クライアントからの受け口となる層

- LINE Handler
  - LINE APP のアクションをトリガーに呼ばれる処理
  - ReplyService に返答情報を格納し、LINE のテキストメッセージとして返答する。
- Views
  - Web ブラウザの画面表示処理
  - 基本的にhtmlを返す
- Apis:
  - 基本的にjsonを返す

#### Application Service Layer
クライアントの求める機能を提供する層
- Use Cases
  - ユーザの1アクションが求める1シナリオ
  - そのシナリオの流れがわかるように詳細な処理はできる限りApp ServiceやDomain Serviceに任せる
- Application Service
  - データに直接関係しない、共有可能な処理（Utility的な）

#### Domain Layer
ドメイン（このアプリで管理する業務データのこと）の情報や操作に関する層
- Domain Service
  - ドメインを操作する処理
- Entity
  - ドメインの情報を表すクラス

#### Infrastructure Layer
DBアクセス層
- Repository
  - データのレコード操作処理
