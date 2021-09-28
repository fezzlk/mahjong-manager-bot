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

follow_use_case = FollowUseCase()
calculate_use_cases = CalculateUseCases()
config_use_cases = ConfigUseCases()
hanchans_use_cases = HanchansUseCases()
matches_use_cases = MatchesUseCases()
ocr_use_cases = OcrUseCases()
points_use_cases = PointsUseCases()
room_use_cases = RoomUseCases()
reply_use_cases = ReplyUseCases()
user_use_cases = UserUseCases()
