from typing import Dict, List
from .interfaces.IGraphService import IGraphService
import env_var
from DomainModel.entities.Hanchan import Hanchan

class GraphService(IGraphService):
    def create_users_point_plot_graph_url(
        self,
        line_id_name_dict: Dict[str, str],
        plot_dict: Dict[str, List[int]],
        upload_file_path: str,
    ) -> (str, str):
        # グラフ描画
        import matplotlib
        import matplotlib.pyplot as plt
        from matplotlib.ticker import MaxNLocator
        matplotlib.use('agg')

        fig, ax = plt.subplots()
        for line_id in line_id_name_dict:
            plt.plot(
                range(len(plot_dict[line_id])),
                plot_dict[line_id],
                label=line_id_name_dict[line_id])
            
        plt.grid(which='major', axis='y')
        plt.legend()
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))

        try:
            fig.savefig(f"src/uploads{upload_file_path}")
        except FileNotFoundError:
            return (None, '対戦履歴の画像アップロードに失敗しました')
        
        plt.clf()
        plt.close()

        path = f'uploads{upload_file_path}'
        return (f'{env_var.SERVER_URL}{path}', None)

    def create_users_point_plot_data(
        self,
        hanchans: List[Hanchan]
    ) -> (List[str], Dict[str, List[int]]):
        line_id_list: List[str] = []
        total_score_dict = {}
        score_plot_dict = {}
        for hanchan in hanchans:
            for line_id in hanchan.converted_scores:
                if line_id not in line_id_list:
                    line_id_list.append(line_id)
                    total_score_dict[line_id] = 0
                    score_plot_dict[line_id] = [0]
  
        for hanchan in hanchans:
            for line_id in line_id_list:
                if line_id in hanchan.converted_scores:
                    total_score_dict[line_id] += hanchan.converted_scores[line_id]
                score_plot_dict[line_id].append(total_score_dict[line_id])

        return (line_id_list, score_plot_dict)
