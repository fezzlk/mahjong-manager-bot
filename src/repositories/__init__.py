from .command_alias_repository import CommandAliasRepository
from .group_repository import GroupRepository
from .group_setting_repository import GroupSettingRepository
from .hanchan_repository import HanchanRepository
from .history_session_repository import HistorySessionRepository
from .match_repository import MatchRepository
from .user_group_repository import UserGroupRepository
from .user_hanchan_repository import UserHanchanRepository
from .user_match_repository import UserMatchRepository
from .user_repository import UserRepository
from .web_user_repository import WebUserRepository
from .yakuman_user_repository import YakumanUserRepository

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
yakuman_user_repository = YakumanUserRepository()
history_session_repository = HistorySessionRepository()
