"""services"""
from .group_service import GroupService
from .group_setting_service import GroupSettingService
from .hanchan_service import HanchanService
from .match_service import MatchService
from .user_group_service import UserGroupService
from .user_hanchan_service import UserHanchanService
from .user_match_service import UserMatchService
from .user_service import UserService

user_service = UserService()
user_group_service = UserGroupService()
user_match_service = UserMatchService()
user_hanchan_service = UserHanchanService()
group_service = GroupService()
group_setting_service = GroupSettingService()
match_service = MatchService()
hanchan_service = HanchanService()
