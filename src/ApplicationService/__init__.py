"""services"""
from .RequestInfoService import RequestInfoService
from .MessageService import MessageService
# from .OcrService import OcrService
from .ReplyService import ReplyService
from .GraphService import GraphService
from .RichMenuService import RichMenuService
from .CalculateService import CalculateService

request_info_service = RequestInfoService()
message_service = MessageService()
# ocr_service = OcrService()
graph_service = GraphService()
reply_service = ReplyService()
rich_menu_service = RichMenuService()
calculate_service = CalculateService()
