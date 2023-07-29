"""services"""
from .UserService import UserService
from .GroupService import GroupService
from .GroupSettingService import GroupSettingService
from .MatchService import MatchService
from .HanchanService import HanchanService

user_service = UserService()
group_service = GroupService()
group_setting_service = GroupSettingService()
match_service = MatchService()
hanchan_service = HanchanService()
