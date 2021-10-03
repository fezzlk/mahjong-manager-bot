"""use cases"""
from .calculate import CalculateUseCases
from .config import ConfigUseCases
from .hanchans import HanchansUseCases
from .matches import MatchesUseCases
from .ocr import OcrUseCases
from .points import PointsUseCases
from .room import RoomUseCases
from .reply import ReplyUseCases
from .user import UserUseCases
from .FollowUseCase import FollowUseCase
from .UnfollowUseCase import UnfollowUseCase
from .JoinRoomUseCase import JoinRoomUseCase
from .AddPointByTextUseCase import AddPointByTextUseCase
from .StartInputUseCase import StartInputUseCase
from .RoomQuitUseCase import RoomQuitUseCase
from .MatchFinishUseCase import MatchFinishUseCase

follow_use_case = FollowUseCase()
unfollow_use_case = UnfollowUseCase()
join_room_use_case = JoinRoomUseCase()
add_point_by_text_use_case = AddPointByTextUseCase()
start_input_use_case = StartInputUseCase()
room_quit_use_case = RoomQuitUseCase()
match_finish_use_case = MatchFinishUseCase()
calculate_use_cases = CalculateUseCases()
config_use_cases = ConfigUseCases()
hanchans_use_cases = HanchansUseCases()
matches_use_cases = MatchesUseCases()
ocr_use_cases = OcrUseCases()
points_use_cases = PointsUseCases()
room_use_cases = RoomUseCases()
reply_use_cases = ReplyUseCases()
user_use_cases = UserUseCases()
