"""services"""
from .RequestInfoService import RequestInfoService
from .CalculateService import CalculateService
from .ConfigService import ConfigService
from .HanchanService import HanchanService
from .MatchService import MatchService
from .MessageService import MessageService
from .ocr import OcrService
from .PointService import PointService
from .ReplyService import ReplyService
from .RichMenuService import RichMenuService
from .RoomService import RoomService
from .UserService import UserService

request_info_service = RequestInfoService()
calculate_service = CalculateService()
config_service = ConfigService()
hanchan_service = HanchanService()
match_service = MatchService()
message_service = MessageService()
ocr_service = OcrService()
point_service = PointService()
reply_service = ReplyService()
rich_menu_service = RichMenuService()
room_service = RoomService()
user_service = UserService()
