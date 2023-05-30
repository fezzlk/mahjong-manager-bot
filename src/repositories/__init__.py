from .GroupSettingRepository import GroupSettingRepository
from .UserRepository import UserRepository
from .WebUserRepository import WebUserRepository
from .HanchanRepository import HanchanRepository
from .UserGroupRepository import UserGroupRepository
from .MatchRepository import MatchRepository
from .UserMatchRepository import UserMatchRepository
from .HanchanMatchRepository import HanchanMatchRepository
from .GroupRepository import GroupRepository

group_setting_repository = GroupSettingRepository()
user_repository = UserRepository()
web_user_repository = WebUserRepository()
hanchan_repository = HanchanRepository()
user_group_repository = UserGroupRepository()
match_repository = MatchRepository()
user_match_repository = UserMatchRepository()
hanchan_match_repository = HanchanMatchRepository()
group_repository = GroupRepository()
