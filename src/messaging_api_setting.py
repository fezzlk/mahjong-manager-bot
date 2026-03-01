from linebot import LineBotApi
import env_var

if not env_var.YOUR_CHANNEL_ACCESS_TOKEN:
    raise RuntimeError('env var "YOUR_CHANNEL_ACCESS_TOKEN" is not set.')

line_bot_api: LineBotApi = LineBotApi(env_var.YOUR_CHANNEL_ACCESS_TOKEN)
