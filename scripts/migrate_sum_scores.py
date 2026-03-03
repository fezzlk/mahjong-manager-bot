#!/usr/bin/env python3
"""DB-04 マイグレーション: match.sum_scores を dict 形式から配列形式に変換

実行手順:
    cd /path/to/project
    python scripts/migrate_sum_scores.py

内容:
    - matches コレクションの各ドキュメントを取得
    - sum_scores が dict 形式のドキュメントを配列形式に変換
    - すでに配列形式のドキュメントはスキップ

注意:
    - この script は idempotent（何度実行しても安全）
    - 変換後は sum_scores: [{"line_user_id": "...", "score": N}, ...] 形式になる
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import dotenv

dotenv.load_dotenv()

from datetime import datetime

from mongo_client import matches_collection


def migrate():
    print("DB-04 マイグレーション開始: match.sum_scores dict → list")

    all_matches = list(matches_collection.find({}))
    print(f"  matches 件数: {len(all_matches)}")

    migrated = 0
    skipped = 0

    for match in all_matches:
        sum_scores = match.get("sum_scores")

        # すでに list 形式ならスキップ
        if isinstance(sum_scores, list):
            skipped += 1
            continue

        # None や空 dict もスキップ（変換不要）
        if not sum_scores:
            skipped += 1
            continue

        # dict → list 変換
        new_sum_scores = [
            {"line_user_id": uid, "score": score}
            for uid, score in sum_scores.items()
        ]
        matches_collection.update_one(
            {"_id": match["_id"]},
            {"$set": {"sum_scores": new_sum_scores, "updated_at": datetime.now()}},
        )
        migrated += 1

    print(f"\n完了: migrated={migrated}, skipped={skipped}")


if __name__ == "__main__":
    migrate()
