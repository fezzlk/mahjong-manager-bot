from .CommandAliasRepository import CommandAliasRepository
from .GroupRepository import GroupRepository
from .GroupSettingRepository import GroupSettingRepository
from .HanchanRepository import HanchanRepository
from .MatchRepository import MatchRepository
from .UserGroupRepository import UserGroupRepository
from .UserHanchanRepository import UserHanchanRepository
from .UserMatchRepository import UserMatchRepository
from .UserRepository import UserRepository
from .WebUserRepository import WebUserRepository

command_alias_repository = CommandAliasRepository()
group_setting_repository = GroupSettingRepository()
user_repository = UserRepository()
web_user_repository = WebUserRepository()
hanchan_repository = HanchanRepository()
user_group_repository = UserGroupRepository()
match_repository = MatchRepository()
user_match_repository = UserMatchRepository()
user_hanchan_repository = UserHanchanRepository()
group_repository = GroupRepository()
