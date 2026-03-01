from linebot.v3.messaging import ApiClient, Configuration, MessagingApi
import env_var

if not env_var.YOUR_CHANNEL_ACCESS_TOKEN:
    raise RuntimeError('env var "YOUR_CHANNEL_ACCESS_TOKEN" is not set.')

_configuration = Configuration(access_token=env_var.YOUR_CHANNEL_ACCESS_TOKEN)
_api_client = ApiClient(_configuration)
line_bot_api: MessagingApi = MessagingApi(_api_client)
