"""services"""
from .ConfigService import ConfigService
from .HanchanService import HanchanService
from .MatchService import MatchService
from .GroupService import GroupService
from .UserService import UserService

config_service = ConfigService()
hanchan_service = HanchanService()
match_service = MatchService()
group_service = GroupService()
user_service = UserService()
