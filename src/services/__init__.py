"""services"""
from .app import AppService
from .calculate import CalculateService
from .config import ConfigService
from .hanchans import HanchansService
from .matches import MatchesService
from .message import MessageService
from .points import PointsService
from .reply import ReplyService
from .rich import RichMenuService
from .room import RoomService
from .user import UserService

app_service = AppService()
calculate_service = CalculateService()
config_service = ConfigService()
hanchans_service = HanchansService()
matches_service = MatchesService()
message_service = MessageService()
points_service = PointsService()
reply_service = ReplyService()
rich_menu_service = RichMenuService()
room_service = RoomService()
user_service = UserService()
