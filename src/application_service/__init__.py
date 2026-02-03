"""services"""
from .calculate_service import CalculateService
from .graph_service import GraphService
from .message_service import MessageService

# from .OcrService import OcrService
from .reply_service import ReplyService
from .request_info_service import RequestInfoService
from .rich_menu_service import RichMenuService

request_info_service = RequestInfoService()
message_service = MessageService()
# ocr_service = OcrService()
graph_service = GraphService()
reply_service = ReplyService()
rich_menu_service = RichMenuService()
calculate_service = CalculateService()
