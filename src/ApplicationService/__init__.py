"""services"""
from .CalculateService import CalculateService
from .GraphService import GraphService
from .MessageService import MessageService

# from .OcrService import OcrService
from .ReplyService import ReplyService
from .RequestInfoService import RequestInfoService
from .RichMenuService import RichMenuService

request_info_service = RequestInfoService()
message_service = MessageService()
# ocr_service = OcrService()
graph_service = GraphService()
reply_service = ReplyService()
rich_menu_service = RichMenuService()
calculate_service = CalculateService()
