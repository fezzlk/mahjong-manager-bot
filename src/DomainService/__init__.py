"""services"""
from .UserService import UserService
from .UserGroupService import UserGroupService
from .UserMatchService import UserMatchService
from .UserHanchanService import UserHanchanService
from .GroupService import GroupService
from .GroupSettingService import GroupSettingService
from .MatchService import MatchService
from .HanchanService import HanchanService

user_service = UserService()
user_group_service = UserGroupService()
user_match_service = UserMatchService()
user_hanchan_service = UserHanchanService()
group_service = GroupService()
group_setting_service = GroupSettingService()
match_service = MatchService()
hanchan_service = HanchanService()
