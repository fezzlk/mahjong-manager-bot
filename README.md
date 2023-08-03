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
![ScreenShot 2023-08-03 23 31 48](https://github.com/fezzlk/mahjong-manager-bot/assets/38426468/9a7e471d-0736-4bda-bac0-f99c47d03f73)

