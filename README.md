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

## Architecture
(TBD)

### Domains
- User
  - Mahjong player's LINE account
- Group
  - LINE chat group
- Group Setting
  - Mahjong rule setting on group
- Hanchan
  - Result of a hanchan
- Match
  - Overall result of hanchans
