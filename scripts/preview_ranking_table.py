"""ランキングテーブル画像のプレビュー生成スクリプト

Usage:
    cd mahjong-manager-bot
    python scripts/preview_ranking_table.py

出力先: ~/ai-output/mahjong-manager-bot/other/
"""

import os
import sys
from pathlib import Path

# src をモジュールパスに追加
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from PIL import Image, ImageDraw, ImageFont

# --- 設定 ---
PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = Path.home() / "ai-output" / "mahjong-manager-bot" / "other"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# macOS 用の日本語フォント候補
FONT_CANDIDATES = [
    "/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc",
    "/System/Library/Fonts/ヒラギノ角ゴシック W6.ttc",
    "/Library/Fonts/Arial Unicode.ttf",
    "/usr/share/fonts/opentype/noto/NotoSerifCJK-Medium.ttc",  # Linux (Docker)
]


def find_font() -> str:
    for path in FONT_CANDIDATES:
        if Path(path).exists():
            return path
    raise FileNotFoundError(
        "日本語フォントが見つかりません。FONT_CANDIDATES にパスを追加してください。",
    )


# --- 定数 (ranking_table_image_builder と同一) ---
BG_COLOR = (33, 33, 33, 255)
FONT_COLOR = (255, 255, 255)
WIDTH = 1024
ROW_HEIGHT = 110
BASE_HEIGHT = 768

# --- サンプルデータ ---
SAMPLE_USERS = [
    ("user_A", "たかし", +520, [60, 40, 80, -20, 50, 30], 80, {1: 3, 2: 2, 3: 1, 4: 0, 0: 0}),
    ("user_B", "はなこ", +310, [50, -10, 70, 20, 40], 70, {1: 2, 2: 1, 3: 1, 4: 1, 0: 1}),
    ("user_C", "さとし", +150, [30, 20, -30, 60], 60, {1: 1, 2: 2, 3: 0, 4: 1, 0: 1}),
    ("user_D", "みさき", -80, [-10, -20, 30, -40, 10], 30, {1: 0, 2: 1, 3: 2, 4: 2, 0: 2}),
    ("user_E", "ゆうた", -200, [-50, -30, -20, -10], -10, {1: 0, 2: 0, 3: 2, 4: 2, 0: 3}),
]


def create_dummy_profile_images():
    """ダミーのプロフィール画像 (カラフルな丸) を生成"""
    profile_dir = PROJECT_ROOT / "src" / "uploads" / "profile_image"
    profile_dir.mkdir(parents=True, exist_ok=True)

    colors = [
        (76, 175, 80),   # green
        (233, 30, 99),   # pink
        (33, 150, 243),  # blue
        (255, 152, 0),   # orange
        (156, 39, 176),  # purple
    ]

    for i, (user_id, name, *_) in enumerate(SAMPLE_USERS):
        img = Image.new("RGB", (100, 100), colors[i % len(colors)])
        draw = ImageDraw.Draw(img)
        # ユーザーイニシャルを描画
        try:
            font = ImageFont.truetype(find_font(), 40)
        except Exception:
            font = ImageFont.load_default()
        initial = name[0]
        bbox = draw.textbbox((0, 0), initial, font=font)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        draw.text(((100 - tw) / 2, (100 - th) / 2 - 5), initial, fill=(255, 255, 255), font=font)
        img.save(profile_dir / f"{user_id}.jpeg", "JPEG")

    return profile_dir


def create_base_image(num_users: int) -> Image.Image:
    width = WIDTH
    height = BASE_HEIGHT + ROW_HEIGHT * max(0, num_users - 6)
    base = Image.new("RGBA", (width, height), BG_COLOR)

    # 王冠画像
    crowns_image = Image.new("RGBA", base.size, (255, 255, 255, 0))
    crown_dir = PROJECT_ROOT / "src" / "static" / "images" / "ranking_table"
    crown_files = [
        (crown_dir / "crown_gold.png", 7, 77),
        (crown_dir / "crown_silver.png", 13, 190),
        (crown_dir / "crown_bronze.png", 7, 300),
    ]
    for i in range(min(3, num_users)):
        path, x, y = crown_files[i]
        crown = Image.open(path)
        crowns_image.paste(crown, (x, y))
    return Image.alpha_composite(base, crowns_image)


def paste_profile_images(base: Image.Image, sorted_ids: list) -> None:
    for i, line_id in enumerate(sorted_ids):
        profile_dir = PROJECT_ROOT / "src" / "uploads" / "profile_image"
        profile_image = Image.open(profile_dir / f"{line_id}.jpeg")
        profile_image = profile_image.resize((50, 50))
        mask = Image.new("L", profile_image.size, 0)
        draw_mask = ImageDraw.Draw(mask)
        draw_mask.ellipse((0, 0, 50, 50), fill=255)
        h = 90 + ROW_HEIGHT * i
        base.paste(profile_image, (110, h), mask)


def draw_text_centered(draw, w, h, text, font, *, anchor="mm", align="center", stroke_width=0):
    x, y, _, _ = draw.textbbox((w, h), text, font=font, anchor=anchor)
    draw.text((x, y), text, FONT_COLOR, font=font, align=align, stroke_width=stroke_width)


def build_score_table(font_path: str) -> Image.Image:
    """累計得点表を生成"""
    # ソート済みデータ
    sorted_data = sorted(SAMPLE_USERS, key=lambda u: u[2], reverse=True)

    num_users = len(sorted_data)
    base = create_base_image(num_users)
    paste_profile_images(base, [u[0] for u in sorted_data])

    draw = ImageDraw.Draw(base)
    col_font = ImageFont.truetype(font_path, 20)
    font = ImageFont.truetype(font_path, 30)

    # ヘッダー
    for label, w in [("累計得点", 450), ("参加半荘数", 600), ("最高得点", 775), ("平均素点", 950)]:
        draw_text_centered(draw, w, 50, label, col_font)
    draw.line((0, 65, WIDTH, 65), fill=FONT_COLOR, width=2)

    # 各行
    for i, (_line_id, name, total, points, max_score, _rank_dict) in enumerate(sorted_data):
        h = 120 + ROW_HEIGHT * i

        # 順位
        draw_text_centered(draw, 50, h, str(i + 1), font, stroke_width=1)
        # 名前
        draw_text_centered(draw, 190, h, name, font, anchor="lm", align="left")
        # 累計得点
        text = f"+{total}" if total > 0 else str(total)
        draw_text_centered(draw, 450, h, text, font)
        # 参加半荘数
        draw_text_centered(draw, 600, h, str(len(points)), font)
        # 最高得点
        text = f"+{max_score}" if max_score > 0 else str(max_score)
        draw_text_centered(draw, 775, h, text, font)
        # 平均素点
        avg = int(sum(points) / len(points)) if points else 0
        draw_text_centered(draw, 950, h, str(avg), font)

        # 区切り線
        line_h = 175 + ROW_HEIGHT * i
        draw.line((0, line_h, WIDTH, line_h), fill=FONT_COLOR, width=1)

    return base


def build_rank_table(font_path: str) -> Image.Image:
    """順位表を生成"""
    # 平均順位でソート
    def calc_ave_rank(u):
        rd = u[5]
        h_count = sum(rd[i] for i in range(1, 5))
        if h_count == 0:
            return 5.0
        return sum(rd[i] * i for i in range(1, 5)) / h_count

    sorted_data = sorted(SAMPLE_USERS, key=calc_ave_rank)

    num_users = len(sorted_data)
    base = create_base_image(num_users)
    paste_profile_images(base, [u[0] for u in sorted_data])

    draw = ImageDraw.Draw(base)
    col_font = ImageFont.truetype(font_path, 20)
    font = ImageFont.truetype(font_path, 30)

    # ヘッダー
    for label, w in [("平均順位", 450), ("1位", 550), ("2位", 650), ("3位", 750), ("4位", 850), ("飛び", 950)]:
        draw_text_centered(draw, w, 50, label, col_font)
    draw.line((0, 65, WIDTH, 65), fill=FONT_COLOR, width=2)

    # 各行
    for i, (line_id, name, _total, _points, _max_score, rank_dict) in enumerate(sorted_data):
        h = 120 + ROW_HEIGHT * i
        ave = calc_ave_rank(SAMPLE_USERS[[u[0] for u in SAMPLE_USERS].index(line_id)])

        # 順位
        draw_text_centered(draw, 50, h, str(i + 1), font, stroke_width=1)
        # 名前
        draw_text_centered(draw, 190, h, name, font, anchor="lm", align="left")
        # 平均順位
        ave_str = f"{ave:.2f}" if ave < 5 else "-"
        draw_text_centered(draw, 450, h, ave_str, font)
        # 1位〜4位
        for rank, w in [(1, 550), (2, 650), (3, 750), (4, 850)]:
            draw_text_centered(draw, w, h, str(rank_dict[rank]), font)
        # 飛び
        draw_text_centered(draw, 950, h, str(rank_dict[0]), font)

        # 区切り線
        line_h = 175 + ROW_HEIGHT * i
        draw.line((0, line_h, WIDTH, line_h), fill=FONT_COLOR, width=1)

    return base


def main():
    font_path = find_font()
    print(f"使用フォント: {font_path}")

    create_dummy_profile_images()
    print("ダミープロフィール画像を生成しました")

    # 累計得点表
    score_img = build_score_table(font_path)
    score_path = OUTPUT_DIR / "preview_score_table.png"
    score_img.save(score_path, "PNG")
    print(f"累計得点表: {score_path}")

    # 順位表
    rank_img = build_rank_table(font_path)
    rank_path = OUTPUT_DIR / "preview_rank_table.png"
    rank_img.save(rank_path, "PNG")
    print(f"順位表: {rank_path}")

    print("\n生成完了！上記パスの画像を確認してください。")


if __name__ == "__main__":
    main()
