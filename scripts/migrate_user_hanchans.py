#!/usr/bin/env python3
"""DB-03 マイグレーション: user_hanchans を hanchan.results として embedded 化

実行手順:
    cd /path/to/project
    python scripts/migrate_user_hanchans.py

内容:
    - user_hanchans コレクションの全ドキュメントを取得
    - 各 user_hanchan を対応する hanchan の results 配列に追加
    - すでに results が存在する hanchan はスキップ

注意:
    - この script は idempotent（何度実行しても安全）
    - 変換後は hanchan.results: [{line_user_id, rank, point, yakuman_count}, ...] 形式になる
    - マイグレーション完了後、user_hanchans コレクションはアーカイブ or 削除可
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import dotenv

dotenv.load_dotenv()

from collections import defaultdict
from datetime import datetime

from mongo_client import hanchans_collection, user_hanchans_collection


def migrate():
    print("DB-03 マイグレーション開始: user_hanchans → hanchan.results")

    all_user_hanchans = list(user_hanchans_collection.find({}))
    print(f"  user_hanchans 件数: {len(all_user_hanchans)}")

    # hanchan_id → list[user_hanchan] のマップを作成
    hanchan_results_map: dict = defaultdict(list)
    for uh in all_user_hanchans:
        hanchan_id = uh.get("hanchan_id")
        if hanchan_id is None:
            continue
        hanchan_results_map[hanchan_id].append({
            "line_user_id": uh.get("line_user_id"),
            "rank": uh.get("rank"),
            "point": uh.get("point"),
            "yakuman_count": uh.get("yakuman_count", 0),
        })

    migrated = 0
    skipped = 0

    for hanchan_id, results in hanchan_results_map.items():
        hanchan = hanchans_collection.find_one({"_id": hanchan_id})
        if hanchan is None:
            print(f"  WARNING: hanchan not found for _id={hanchan_id}, skipping")
            skipped += 1
            continue

        # すでに results が存在する場合はスキップ（idempotent）
        existing_results = hanchan.get("results") or []
        if existing_results:
            skipped += 1
            continue

        hanchans_collection.update_one(
            {"_id": hanchan_id},
            {"$set": {"results": results, "updated_at": datetime.now()}},
        )
        migrated += 1

    print(f"\n完了: migrated={migrated}, skipped={skipped}")


if __name__ == "__main__":
    migrate()
