from abc import ABCMeta, abstractmethod
from typing import Dict, List


class IGraphService(metaclass=ABCMeta):

    @abstractmethod
    def create_users_point_plot_graph_url(
        self,
        line_id_name_dict: Dict[str, str],
        plot_dict: Dict[str, List[int]],
        upload_file_path: str,
    ) -> str:
        pass
