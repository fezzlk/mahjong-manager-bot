"""services"""
from .calculate_service import CalculateService
from .graph_service import GraphService
from .message_service import MessageService
from .ranking_table_image_builder import RankingTableImageBuilder
from .reply_service import ReplyService
from .request_info_service import RequestInfoService

request_info_service = RequestInfoService()
message_service = MessageService()
graph_service = GraphService()
reply_service = ReplyService()
calculate_service = CalculateService()
ranking_table_image_builder = RankingTableImageBuilder()
