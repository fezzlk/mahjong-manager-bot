#!/usr/bin/env python3
"""DB-02 マイグレーション: group_settings コレクションを groups に embedded 化

実行手順:
    cd /path/to/project
    python scripts/migrate_group_settings.py

内容:
    - group_settings コレクションの各ドキュメントを取得
    - 対応する group ドキュメントに settings フィールドとして埋め込む
    - すでに settings が設定済みのグループはスキップ

注意:
    - migration 完了後、group_settings コレクションは不要になる
    - この script は idempotent(何度実行しても安全)
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import dotenv

dotenv.load_dotenv()

from datetime import datetime

from mongo_client import group_settings_collection, groups_collection


def migrate():
    print("DB-02 マイグレーション開始: group_settings → groups.settings")

    all_settings = list(group_settings_collection.find({}))
    print(f"  group_settings 件数: {len(all_settings)}")

    migrated = 0
    skipped = 0

    for gs in all_settings:
        line_group_id = gs.get("line_group_id")
        if not line_group_id:
            print(f"  SKIP (line_group_id なし): {gs.get('_id')}")
            skipped += 1
            continue

        # 対応する group を検索
        group = groups_collection.find_one({"line_group_id": line_group_id})
        if group is None:
            print(f"  SKIP (group not found): {line_group_id}")
            skipped += 1
            continue

        # すでに settings が設定済みならスキップ
        if group.get("settings") is not None:
            print(f"  SKIP (already embedded): {line_group_id}")
            skipped += 1
            continue

        # settings を埋め込む
        settings_dict = {
            "rate": gs.get("rate", 0),
            "ranking_prize": gs.get("ranking_prize", [20, 10, -10, -20]),
            "chip_rate": gs.get("chip_rate", 0),
            "tobi_prize": gs.get("tobi_prize", 10),
            "num_of_players": gs.get("num_of_players", 4),
            "rounding_method": gs.get("rounding_method", 2),
        }
        groups_collection.update_one(
            {"line_group_id": line_group_id},
            {"$set": {"settings": settings_dict, "updated_at": datetime.now()}},
        )
        print(f"  MIGRATED: {line_group_id}")
        migrated += 1

    print(f"\n完了: migrated={migrated}, skipped={skipped}")
    print("group_settings コレクションは手動で削除してください (migration 確認後)")


if __name__ == "__main__":
    migrate()
