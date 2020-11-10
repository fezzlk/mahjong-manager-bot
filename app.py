import os
from flask import Flask, request, abort, logging
from linebot import LineBotApi, WebhookHandler, exceptions
from linebot.models import (
    FollowEvent,
    MessageEvent,
    TextMessage, 
    ImageMessage,
    PostbackEvent,
)

# import original module
import local_env
local_env.set_env()

YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

app = Flask(__name__)
logger = logging.create_logger(app)

import router

### server root
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except exceptions.InvalidSignatureError:
        abort(400)
    return 'OK'

### handle event
# follow
@handler.add(FollowEvent)
def handle_follow(event):
    logger.info('follow')
    router.follow(event)

# receive message
@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    logger.info('recieve text message')
    router.textMessage(event)

@handler.add(MessageEvent, message=ImageMessage)
def handle_image_message(event):
    logger.info('recieve image message')
    router.imageMessage(event)

@handler.add(PostbackEvent)
def handle_postback(event):
    logger.info('recieve postback message')
    router.postback(event)

if __name__ == "__main__":
   app.run()
    # port = int(os.getenv("PORT"))
    # app.run(host="0.0.0.0", port=port)
