"""use cases"""
from .calculate import CalculateUseCases
from .config import ConfigUseCases
from .hanchans import HanchansUseCases
from .matches import MatchesUseCases
from .message import MessageUseCases
from .ocr import OcrUseCases
from .points import PointsUseCases
from .room import RoomUseCases
from .user import UserUseCases

calculate_use_cases = CalculateUseCases()
config_use_cases = ConfigUseCases()
hanchans_use_cases = HanchansUseCases()
matches_use_cases = MatchesUseCases()
message_use_cases = MessageUseCases()
ocr_use_cases = OcrUseCases()
points_use_cases = PointsUseCases()
room_use_cases = RoomUseCases()
user_use_cases = UserUseCases()
