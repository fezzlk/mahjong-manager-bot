"""services"""
from .UserService import UserService
from .UserGroupService import UserGroupService
from .UserMatchService import UserMatchService
from .GroupService import GroupService
from .GroupSettingService import GroupSettingService
from .MatchService import MatchService
from .HanchanService import HanchanService

user_service = UserService()
user_group_service = UserGroupService()
user_match_service = UserMatchService()
group_service = GroupService()
group_setting_service = GroupSettingService()
match_service = MatchService()
hanchan_service = HanchanService()
