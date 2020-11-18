from .app import AppService
from .calculate import CalculateService
from .config import ConfigService
from .matches import MatchesService
from .mode import ModeService
from .points import PointsService
from .reply import ReplyService
from .results import ResultsService
from .rich import RichMenuService

class Services:

    def __init__(self):
        self.app_service = AppService()
        self.calculate_service = CalculateService(self)
        self.config_service = ConfigService(self)
        self.matches_service = MatchesService(self)
        self.mode_service = ModeService(self)
        self.points_service = PointsService(self)
        self.reply_service = ReplyService(self)
        self.results_service = ResultsService(self)
        self.rich_menu_service = RichMenuService(self)
