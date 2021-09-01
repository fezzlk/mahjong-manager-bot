import os
from linebot import LineBotApi
from server import logger


line_bot_api = None

if "YOUR_CHANNEL_ACCESS_TOKEN" in os.environ:
    YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
    line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
else:
    logger.warning(
        'line_bot_api is not setup: YOUR_CHANNEL_ACCESS_TOKEN is not found.')
