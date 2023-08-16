"""services"""
from .UserService import UserService
from .UserGroupService import UserGroupService
from .GroupService import GroupService
from .GroupSettingService import GroupSettingService
from .MatchService import MatchService
from .HanchanService import HanchanService

user_service = UserService()
user_group_service = UserGroupService()
group_service = GroupService()
group_setting_service = GroupSettingService()
match_service = MatchService()
hanchan_service = HanchanService()
