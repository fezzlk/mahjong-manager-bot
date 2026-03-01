import io
import logging
import os
from pathlib import Path
from typing import Dict, List, Tuple

import matplotlib as mpl

mpl.use("agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

import env_var
from domain_model.entities.hanchan import Hanchan

from .interfaces.i_graph_service import IGraphService

logger = logging.getLogger(__name__)


class GraphService(IGraphService):
    def create_users_point_plot_graph_url(
        self,
        line_id_name_dict: Dict[str, str],
        plot_dict: Dict[str, List[int]],
        upload_file_path: str,
    ) -> Tuple[str, str]:
        # グラフ描画
        fig, ax = plt.subplots()
        for line_id in line_id_name_dict:
            x_vals = [i for i, _ in enumerate(plot_dict[line_id])]
            plt.plot(
                x_vals,
                plot_dict[line_id],
                label=line_id_name_dict[line_id],
            )

        plt.grid(which="major", axis="y")
        plt.legend()
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))

        buf = io.BytesIO()
        try:
            fig.savefig(buf, format="png")
        except Exception as err:
            logger.exception("グラフ画像の生成に失敗しました")
            return (None, f"グラフ画像の生成に失敗しました: {err}")
        finally:
            plt.clf()
            plt.close()

        buf.seek(0)

        # GCS が設定されている場合は GCS にアップロード、なければローカル保存
        if env_var.GCS_BUCKET_NAME:
            return self._upload_to_gcs(buf, upload_file_path)
        return self._save_locally(buf, upload_file_path)

    def _upload_to_gcs(self, buf: io.BytesIO, upload_file_path: str) -> Tuple[str, str]:
        """Google Cloud Storage に画像をアップロードし公開 URL を返す"""
        try:
            from google.cloud import storage  # noqa: PLC0415

            blob_name = f"uploads{upload_file_path}"
            client = storage.Client()
            bucket = client.bucket(env_var.GCS_BUCKET_NAME)
            blob = bucket.blob(blob_name)
            blob.upload_from_file(buf, content_type="image/png")
            blob.make_public()
            return (blob.public_url, None)
        except Exception as err:
            logger.exception("GCS へのアップロードに失敗しました")
            return (None, f"対戦履歴の画像アップロードに失敗しました: {err}")

    def _save_locally(self, buf: io.BytesIO, upload_file_path: str) -> Tuple[str, str]:
        """ローカルファイルシステムに画像を保存する（開発環境用）""" # noqa: RUF002
        try:
            local_path = f"src/uploads{upload_file_path}"
            Path(os.path.dirname(local_path)).mkdir(parents=True, exist_ok=True)
            with open(local_path, "wb") as f:
                f.write(buf.read())
            path = f"uploads{upload_file_path}"
            return (f"{env_var.SERVER_URL}{path}", None)
        except Exception as err:
            logger.exception("ローカルへの画像保存に失敗しました")
            return (None, f"対戦履歴の画像アップロードに失敗しました: {err}")

    def create_users_point_plot_data(
        self,
        hanchans: List[Hanchan],
    ) -> Tuple[List[str], Dict[str, List[int]]]:
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
