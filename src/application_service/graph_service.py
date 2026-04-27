import io
import logging
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import matplotlib as mpl

mpl.use("agg")
import matplotlib.dates as mdates
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

    def save_figure(self, fig, upload_file_path: str) -> Tuple[str, str]:
        """Matplotlib Figure を GCS またはローカルに保存し (url, err) を返す"""
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

    def build_history_step_graph(
        self,
        histories: Dict[str, Dict[datetime, int]],
        start_date: datetime,
        to_dt: Optional[datetime],
        line_id_name_dict: Optional[Dict[str, str]] = None,
        match_count: Optional[int] = None,
    ) -> plt.Figure:
        """スコア推移のステップグラフを構築する。

        histories: {line_id: {match_datetime: cumulative_score}} ※ダミー値なし
        """
        if to_dt is None:
            to_dt = datetime.now()

        # ダミー値(y=0パディング)と最終点を追加
        padded: Dict[str, Dict[datetime, int]] = {}
        for line_id, raw in histories.items():
            last_score = raw[max(raw.keys())]
            padded[line_id] = {
                start_date - timedelta(minutes=2): 0,
                start_date - timedelta(minutes=1): 0,
                **raw,
                to_dt: last_score,
            }

        fig, ax = plt.subplots(figsize=(8, 4))

        for line_id, history in padded.items():
            xs = sorted(history.keys())
            ys = [history[x] for x in xs]
            label = (line_id_name_dict or {}).get(line_id)
            ax.step(xs, ys, where="post", marker="o",
                    markersize=5, markeredgewidth=0, label=label)

        # y=0 強調線
        ax.axhline(y=0, color="#e74c3c", linewidth=1.0,
                   alpha=0.7, linestyle="--", zorder=0)

        # グリッド・スパイン
        ax.grid(which="major", axis="y", alpha=0.3, linestyle="--")
        ax.spines["right"].set_visible(False)
        ax.spines["top"].set_visible(False)

        # X軸
        ax.set_xlim([start_date - timedelta(minutes=1), to_dt])
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%m/%d %H時"))
        plt.xticks(rotation=30, fontsize=9)
        plt.yticks(fontsize=9)

        if line_id_name_dict:
            ax.legend(fontsize=9)

        # 1ユーザー: 累計/対戦数タイトル + 最高/最低注釈
        if len(histories) == 1:
            line_id = next(iter(histories))
            raw = histories[line_id]
            scores = list(raw.values())
            total = raw[max(raw.keys())]
            total_str = f"+{total}" if total > 0 else str(total)
            count_str = f"  {match_count}対戦" if match_count is not None else ""
            ax.set_title(f"累計: {total_str}pt{count_str}",
                         loc="right", fontsize=10)

            max_score = max(scores)
            min_score = min(scores)
            for dt, score in raw.items():
                if score == max_score:
                    sign = "+" if score > 0 else ""
                    ax.annotate(f"▲ {sign}{score}",
                                xy=(dt, score), xytext=(5, 5),
                                textcoords="offset points",
                                fontsize=8, color="#2980b9")
                if score == min_score and min_score != max_score:
                    sign = "+" if score > 0 else ""
                    ax.annotate(f"▼ {sign}{score}",
                                xy=(dt, score), xytext=(5, -12),
                                textcoords="offset points",
                                fontsize=8, color="#e74c3c")

        fig.tight_layout()
        return fig

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
