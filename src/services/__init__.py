"""services"""
from .RequestInfoService import RequestInfoService
from .calculate import CalculateService
from .config import ConfigService
from .hanchans import HanchansService
from .matches import MatchesService
from .MessageService import MessageService
from .ocr import OcrService
from .points import PointsService
from .reply import ReplyService
from .RichMenuService import RichMenuService
from .room import RoomService
from .UserService import UserService

request_info_service = RequestInfoService()
calculate_service = CalculateService()
config_service = ConfigService()
hanchans_service = HanchansService()
matches_service = MatchesService()
message_service = MessageService()
ocr_service = OcrService()
points_service = PointsService()
reply_service = ReplyService()
rich_menu_service = RichMenuService()
room_service = RoomService()
user_service = UserService()
