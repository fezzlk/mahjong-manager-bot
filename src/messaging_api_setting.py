from linebot import LineBotApi
from src import env_var

line_bot_api: LineBotApi = None

if env_var.YOUR_CHANNEL_ACCESS_TOKEN is not None:
    line_bot_api = LineBotApi(env_var.YOUR_CHANNEL_ACCESS_TOKEN)
else:
    print('line_bot_api is not setup: YOUR_CHANNEL_ACCESS_TOKEN is not found.')
