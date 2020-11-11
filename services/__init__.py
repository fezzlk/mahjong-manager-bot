from .app import AppService
from .calculate import CalculateService
from .config import ConfigService
from .mode import ModeService
from .points import PointsService
from .reply import ReplyService
from .results import ResultsService
from .rich import RichMenuService

class Services:

    def __init__(self):
        self.app_service = AppService()
        self.reply_service = ReplyService(self)
        self.config_service = ConfigService(self)
        self.points_service = PointsService(self)
        self.results_service = ResultsService(self)
        self.calculate_service = CalculateService(self)
        self.mode_service = ModeService(self)
        self. rich_menu_service = RichMenuService(self)
