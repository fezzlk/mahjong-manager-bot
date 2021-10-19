from .user.FollowUseCase import FollowUseCase
from .user.UnfollowUseCase import UnfollowUseCase
from .user.ChangeUserModeUseCase import ChangeUserModeUseCase
from .user.SetZoomUrlToUserUseCase import SetZoomUrlToUserUseCase
from .user.ReplyUserHelpUseCase import ReplyUserHelpUseCase
from .user.ReplyUserModeUseCase import ReplyUserModeUseCase
from .user.ReplyFortuneUseCase import ReplyFortuneUseCase
from .user.ReplyGitHubUrlUseCase import ReplyGitHubUrlUseCase
from .user.GetUsersForWebUseCase import GetUsersForWebUseCase
from .user.DeleteUsersForWebUseCase import DeleteUsersForWebUseCase

from .group.JoinRoomUseCase import JoinRoomUseCase
from .group.RoomQuitUseCase import RoomQuitUseCase
from .group.SetZoomUrlToRoomUseCase import SetZoomUrlToRoomUseCase
from .group.SetMyZoomUrlToRoomUseCase import SetMyZoomUrlToRoomUseCase
from .group.ReplyRoomHelpUseCase import ReplyRoomHelpUseCase
from .group.ReplyRoomSettingsMenuUseCase import ReplyRoomSettingsMenuUseCase
from .group.ReplyStartMenuUseCase import ReplyStartMenuUseCase
from .group.ReplyOthersMenuUseCase import ReplyOthersMenuUseCase
from .group.ReplyRoomModeUseCase import ReplyRoomModeUseCase
from .group.ReplyRoomZoomUrlUseCase import ReplyRoomZoomUrlUseCase
from .group.GetRoomsForWebUseCase import GetRoomsForWebUseCase
from .group.DeleteRoomsForWebUseCase import DeleteRoomsForWebUseCase

from .hanchan.AddHanchanByPointsTextUseCase import AddHanchanByPointsTextUseCase
from .hanchan.AddPointByJsonTextUseCase import AddPointByJsonTextUseCase
from .hanchan.AddPointByTextUseCase import AddPointByTextUseCase
from .hanchan.StartInputUseCase import StartInputUseCase
from .hanchan.ReplySumHanchansUseCase import ReplySumHanchansUseCase
from .hanchan.InputResultFromImageUseCase import InputResultFromImageUseCase
from .hanchan.CalculateWithTobiUseCase import CalculateWithTobiUseCase
from .hanchan.GetHanchansForWebUseCase import GetHanchansForWebUseCase
from .hanchan.DeleteHanchansForWebUseCase import DeleteHanchansForWebUseCase

from .match.ReplyMatchesUseCase import ReplyMatchesUseCase
from .match.ReplySumHanchansByMatchIdUseCase import ReplySumHanchansByMatchIdUseCase
from .match.ReplySumMatchesByIdsUseCase import ReplySumMatchesByIdsUseCase
from .match.DisableMatchUseCase import DisableMatchUseCase
from .match.DropHanchanByIndexUseCase import DropHanchanByIndexUseCase
from .match.MatchFinishUseCase import MatchFinishUseCase
from .match.GetMatchesForWebUseCase import GetMatchesForWebUseCase
from .match.DeleteMatchesForWebUseCase import DeleteMatchesForWebUseCase

from .config.UpdateConfigUseCase import UpdateConfigUseCase
from .config.GetConfigsForWebUseCase import GetConfigsForWebUseCase
from .config.DeleteConfigsForWebUseCase import DeleteConfigsForWebUseCase

follow_use_case = FollowUseCase()
unfollow_use_case = UnfollowUseCase()
join_room_use_case = JoinRoomUseCase()
add_hanchan_by_points_text_use_case = AddHanchanByPointsTextUseCase()
add_point_by_text_use_case = AddPointByTextUseCase()
add_point_by_Json_text_use_case = AddPointByJsonTextUseCase()
drop_hanchan_by_index_use_case = DropHanchanByIndexUseCase()
start_input_use_case = StartInputUseCase()
room_quit_use_case = RoomQuitUseCase()
match_finish_use_case = MatchFinishUseCase()
reply_user_mode_use_case = ReplyUserModeUseCase()
reply_room_mode_use_case = ReplyRoomModeUseCase()
change_user_mode_use_case = ChangeUserModeUseCase()
reply_fortune_use_case = ReplyFortuneUseCase()
reply_sum_hanchans_use_case = ReplySumHanchansUseCase()
reply_sum_hanchans__by_match_id_use_case = ReplySumHanchansByMatchIdUseCase()
reply_matches_use_case = ReplyMatchesUseCase()
reply_user_help_use_case = ReplyUserHelpUseCase()
reply_room_help_use_case = ReplyRoomHelpUseCase()
reply_github_url_use_case = ReplyGitHubUrlUseCase()
reply_start_menu_use_case = ReplyStartMenuUseCase()
reply_others_menu_use_case = ReplyOthersMenuUseCase()
reply_room_settings_menu_use_case = ReplyRoomSettingsMenuUseCase()
reply_room_zoom_url_use_case = ReplyRoomZoomUrlUseCase()
set_my_zoom_url_to_room_use_case = SetMyZoomUrlToRoomUseCase()
set_zoom_url_to_user_use_case = SetZoomUrlToUserUseCase()
set_zoom_url_to_room_use_case = SetZoomUrlToRoomUseCase()
calculate_with_tobi_use_case = CalculateWithTobiUseCase()
get_rooms_for_web_use_case = GetRoomsForWebUseCase()
get_configs_for_web_use_case = GetConfigsForWebUseCase()
get_hanchans_for_web_use_case = GetHanchansForWebUseCase()
get_matches_for_web_use_case = GetMatchesForWebUseCase()
get_users_for_web_use_case = GetUsersForWebUseCase()
delete_rooms_for_web_use_case = DeleteRoomsForWebUseCase()
delete_configs_for_web_use_case = DeleteConfigsForWebUseCase()
delete_hanchans_for_web_use_case = DeleteHanchansForWebUseCase()
delete_matches_for_web_use_case = DeleteMatchesForWebUseCase()
delete_users_for_web_use_case = DeleteUsersForWebUseCase()
update_config_use_case = UpdateConfigUseCase()
input_result_from_image_use_case = InputResultFromImageUseCase()
reply_sum_matches_by_ids_use_case = ReplySumMatchesByIdsUseCase()
disable_match_use_case = DisableMatchUseCase()
