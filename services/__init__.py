"""services"""
from .app import AppService
from .calculate import CalculateService
from .config import ConfigService
from .matches import MatchesService
from .points import PointsService
from .reply import ReplyService
from .results import ResultsService
from .rich import RichMenuService
from .room import RoomService
from .user import UserService


class Services:
    """services"""

    def __init__(self):
        self.app_service = AppService()
        self.calculate_service = CalculateService(self)
        self.config_service = ConfigService(self)
        self.matches_service = MatchesService(self)
        self.points_service = PointsService(self)
        self.reply_service = ReplyService(self)
        self.results_service = ResultsService(self)
        self.rich_menu_service = RichMenuService(self)
        self.room_service = RoomService(self)
        self.user_service = UserService(self)
