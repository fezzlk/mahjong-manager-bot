"""services"""
from .RequestInfoService import RequestInfoService
from .MessageService import MessageService
# from .OcrService import OcrService
from .ReplyService import ReplyService
from .RichMenuService import RichMenuService

request_info_service = RequestInfoService()
message_service = MessageService()
# ocr_service = OcrService()
reply_service = ReplyService()
rich_menu_service = RichMenuService()
