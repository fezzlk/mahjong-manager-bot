from abc import ABCMeta, abstractmethod
from datetime import datetime
from typing import Dict, List, Optional, Tuple


class IGraphService(metaclass=ABCMeta):

    @abstractmethod
    def create_users_point_plot_graph_url(
        self,
        line_id_name_dict: Dict[str, str],
        plot_dict: Dict[str, List[int]],
        upload_file_path: str,
    ) -> str:
        pass

    @abstractmethod
    def save_figure(self, fig, upload_file_path: str) -> Tuple[str, str]:
        pass

    @abstractmethod
    def build_history_step_graph(
        self,
        histories: Dict[str, Dict[datetime, int]],
        start_date: datetime,
        to_dt: Optional[datetime],
        line_id_name_dict: Optional[Dict[str, str]] = None,
        match_count: Optional[int] = None,
    ):
        pass
