"""Services"""
from .RequestInfoService import RequestInfoService
from .ConfigService import ConfigService
from .HanchanService import HanchanService
from .MatchService import MatchService
from .MessageService import MessageService
from .OcrService import OcrService
from .ReplyService import ReplyService
from .RichMenuService import RichMenuService
from .GroupService import GroupService
from .UserService import UserService

request_info_service = RequestInfoService()
config_service = ConfigService()
hanchan_service = HanchanService()
match_service = MatchService()
message_service = MessageService()
ocr_service = OcrService()
reply_service = ReplyService()
rich_menu_service = RichMenuService()
group_service = GroupService()
user_service = UserService()
