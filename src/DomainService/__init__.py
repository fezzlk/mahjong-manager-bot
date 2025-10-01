"""services"""
from .GroupService import GroupService
from .GroupSettingService import GroupSettingService
from .HanchanService import HanchanService
from .MatchService import MatchService
from .UserGroupService import UserGroupService
from .UserHanchanService import UserHanchanService
from .UserMatchService import UserMatchService
from .UserService import UserService

user_service = UserService()
user_group_service = UserGroupService()
user_match_service = UserMatchService()
user_hanchan_service = UserHanchanService()
group_service = GroupService()
group_setting_service = GroupSettingService()
match_service = MatchService()
hanchan_service = HanchanService()
