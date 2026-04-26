import io
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Tuple

from PIL import Image, ImageDraw, ImageFont

import env_var

logger = logging.getLogger(__name__)


class RankingTableImageBuilder:
    SCALE = 1
    BG_COLOR = (33, 33, 33, 255)
    FONT_COLOR = (255, 255, 255)
    WIDTH = 1024
    DUMMY_MIN_SCORE = -10000

    def _create_base_image(self, num_users: int) -> Image.Image:
        scale = self.SCALE
        width = self.WIDTH * scale
        height = (768 + 110 * max(0, num_users - 6)) * scale
        base_image = Image.new("RGBA", (width, height), self.BG_COLOR)

        crowns_image = Image.new("RGBA", base_image.size, (255, 255, 255, 0))
        gold = Image.open("src/static/images/ranking_table/crown_gold.png")
        silver = Image.open("src/static/images/ranking_table/crown_silver.png")
        bronze = Image.open("src/static/images/ranking_table/crown_bronze.png")
        crowns = [(gold, 7, 77), (silver, 13, 190), (bronze, 7, 300)]
        for i in range(min(3, num_users)):
            crowns_image.paste(
                crowns[i][0], (crowns[i][1] * scale, crowns[i][2] * scale),
            )
        return Image.alpha_composite(base_image, crowns_image)

    def _paste_profile_images(self, base: Image.Image, sorted_ids: list) -> None:
        scale = self.SCALE
        for i, line_id in enumerate(sorted_ids):
            profile_image_path = Path(f"src/uploads/profile_image/{line_id}.jpeg")
            if not profile_image_path.exists():
                continue
            profile_image = Image.open(profile_image_path)
            profile_image = profile_image.resize((50 * scale, 50 * scale))
            mask = Image.new("L", profile_image.size, 0)
            draw_mask = ImageDraw.Draw(mask)
            draw_mask.ellipse(
                (0, 0, profile_image.size[0], profile_image.size[1]), fill=255,
            )
            h = (90 + 110 * i) * scale
            base.paste(profile_image, (110 * scale, h), mask)

    def _save_image(self, image: Image.Image, upload_file_path: str) -> Tuple[str, str]:
        """PIL Image を GCS またはローカルに保存し (url, err) を返す"""
        buf = io.BytesIO()
        image.save(buf, format="PNG", quality=75)
        buf.seek(0)
        if env_var.GCS_BUCKET_NAME:
            return self._upload_to_gcs(buf, upload_file_path)
        return self._save_locally(buf, upload_file_path)

    def _upload_to_gcs(self, buf: io.BytesIO, upload_file_path: str) -> Tuple[str, str]:
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
            return (None, f"ランキング表の画像アップロードに失敗しました: {err}")

    def _save_locally(self, buf: io.BytesIO, upload_file_path: str) -> Tuple[str, str]:
        try:
            local_path = f"src/uploads{upload_file_path}"
            Path(os.path.dirname(local_path)).mkdir(parents=True, exist_ok=True)
            with open(local_path, "wb") as f:
                f.write(buf.read())
            return (f"{env_var.SERVER_URL}/uploads{upload_file_path}", None)
        except Exception as err:
            logger.exception("ローカルへの画像保存に失敗しました")
            return (None, f"ランキング表の画像アップロードに失敗しました: {err}")

    def build_score_table(
        self,
        sorted_total_dict: list,
        display_name_dict: dict,
        point_dict: dict,
        max_score_dict: dict,
        req_line_user_id: str,
    ) -> str:
        scale = self.SCALE
        width = self.WIDTH * scale
        font_color = self.FONT_COLOR

        base_image = self._create_base_image(len(sorted_total_dict))
        self._paste_profile_images(base_image, [r[0] for r in sorted_total_dict])

        draw = ImageDraw.Draw(base_image)
        font_path = env_var.FONT_FILE_PATH

        col_font = ImageFont.truetype(font_path, 20 * scale)
        h = 50 * scale
        for text, w in [
            ("累計得点", 450),
            ("参加半荘数", 600),
            ("最高得点", 775),
            ("平均素点", 950),
        ]:
            x, y, _x2, _y2 = draw.textbbox((w * scale, h), text, font=col_font, anchor="mm")
            draw.text((x, y), text, font_color, font=col_font, align="center")

        draw.line((0, 65 * scale, width, 65 * scale), fill=(255, 255, 255), width=2)

        font = ImageFont.truetype(font_path, 30 * scale)
        for i, r in enumerate(sorted_total_dict):
            line_id = r[0]
            h = (120 + 110 * i) * scale

            text = str(i + 1)
            x, y, _x2, _y2 = draw.textbbox((50 * scale, h), text, font=font, anchor="mm")
            draw.text((x, y), text, font_color, font=font, stroke_width=1, align="center")

            text = display_name_dict[line_id]
            x, y, _x2, _y2 = draw.textbbox((190 * scale, h), text, font=font, anchor="lm")
            draw.text((x, y), text, font_color, font=font, align="left")

            text = ("+" + str(r[1])) if r[1] > 0 else str(r[1])
            x, y, _x2, _y2 = draw.textbbox((450 * scale, h), text, font=font, anchor="mm")
            draw.text((x, y), text, font_color, font=font, align="center")

            text = str(len(point_dict[line_id]))
            x, y, _x2, _y2 = draw.textbbox((600 * scale, h), text, font=font, anchor="mm")
            draw.text((x, y), text, font_color, font=font, align="center")

            if max_score_dict[line_id] == self.DUMMY_MIN_SCORE:
                text = "-"
            else:
                m = max_score_dict[line_id]
                text = ("+" + str(m)) if m > 0 else str(m)
            x, y, _x2, _y2 = draw.textbbox((775 * scale, h), text, font=font, anchor="mm")
            draw.text((x, y), text, font_color, font=font, align="center")

            if len(point_dict[line_id]) == 0:
                text = "-"
            else:
                text = str(int(sum(point_dict[line_id]) / len(point_dict[line_id])))
            x, y, _x2, _y2 = draw.textbbox((950 * scale, h), text, font=font, anchor="mm")
            draw.text((x, y), text, font_color, font=font, align="center")

            draw.line(
                (0, (175 + 110 * i) * scale, width, (175 + 110 * i) * scale),
                fill=(255, 255, 255),
                width=1,
            )

        path = f"/ranking_table/{req_line_user_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}.png"
        url, err = self._save_image(base_image, path)
        if err:
            raise FileNotFoundError(err)
        return url

    def build_rank_table(
        self,
        sorted_ave_rank_dict: list,
        display_name_dict: dict,
        ave_rank_str_dict: dict,
        rank_dict: dict,
        req_line_user_id: str,
    ) -> str:
        scale = self.SCALE
        width = self.WIDTH * scale
        font_color = self.FONT_COLOR

        base_image = self._create_base_image(len(sorted_ave_rank_dict))
        self._paste_profile_images(base_image, [r[0] for r in sorted_ave_rank_dict])

        draw = ImageDraw.Draw(base_image)
        font_path = env_var.FONT_FILE_PATH

        col_font = ImageFont.truetype(font_path, 20 * scale)
        h = 50 * scale
        for text, w in [
            ("平均順位", 450),
            ("1位", 550),
            ("2位", 650),
            ("3位", 750),
            ("4位", 850),
            ("飛び", 950),
        ]:
            x, y, _x2, _y2 = draw.textbbox((w * scale, h), text, font=col_font, anchor="mm")
            draw.text((x, y), text, font_color, font=col_font, align="center")

        draw.line((0, 65 * scale, width, 65 * scale), fill=(255, 255, 255), width=2)

        font = ImageFont.truetype(font_path, 30 * scale)
        for i, r in enumerate(sorted_ave_rank_dict):
            line_id = r[0]
            h = (120 + 110 * i) * scale

            text = str(i + 1)
            x, y, _x2, _y2 = draw.textbbox((50 * scale, h), text, font=font, anchor="mm")
            draw.text((x, y), text, font_color, font=font, stroke_width=1, align="center")

            text = display_name_dict[line_id]
            x, y, _x2, _y2 = draw.textbbox((190 * scale, h), text, font=font, anchor="lm")
            draw.text((x, y), text, font_color, font=font, align="left")

            text = ave_rank_str_dict[line_id]
            x, y, _x2, _y2 = draw.textbbox((450 * scale, h), text, font=font, anchor="mm")
            draw.text((x, y), text, font_color, font=font, align="center")

            for rank, w in [(1, 550), (2, 650), (3, 750), (4, 850), (0, 950)]:
                text = str(rank_dict[line_id][rank])
                x, y, _x2, _y2 = draw.textbbox((w * scale, h), text, font=font, anchor="mm")
                draw.text((x, y), text, font_color, font=font, align="center")

            draw.line(
                (0, (175 + 110 * i) * scale, width, (175 + 110 * i) * scale),
                fill=(255, 255, 255),
                width=1,
            )

        path = f"/ranking_table_rank/{req_line_user_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}.png"
        url, err = self._save_image(base_image, path)
        if err:
            raise FileNotFoundError(err)
        return url
