#!/usr/bin/env python3
"""FEZ-66 Phase A マイグレーション: Match に status/name をバックフィル

実行手順:
    cd /path/to/project
    python scripts/migrate_match_status_and_name.py

内容:
    - 各 Group の active_match_id が指す Match に status="open" をセット
    - 同じ line_group_id を持つ他の Match のうち status 未設定のものに
      status="settled" をセット
    - name が未設定の Match に、created_at の日付から "M/D" ベースの
      デフォルト名を付与する（同日同グループ内で複数件あれば created_at
      昇順に "(2)", "(3)"... を付与）
    - settings は今回バックフィルしない（既存コードはまだ Match.settings
      を参照しないため実害なし。新規作成分のみコード変更で自動的に埋まる）

注意:
    - この script は idempotent(何度実行しても安全)。既に status が
      設定済みの Match はスキップする。
"""
import os
import sys
from collections import defaultdict

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import env_var  # noqa: F401 — loads .env
from mongo_client import groups_collection, matches_collection


def migrate():
    print("FEZ-66 Phase A マイグレーション開始: Match.status / Match.name バックフィル")

    # 1. status のバックフィル
    open_ids = set()
    for group in groups_collection.find({"active_match_id": {"$ne": None}}):
        open_ids.add(group["active_match_id"])

    open_count = 0
    for match_id in open_ids:
        res = matches_collection.update_one(
            {"_id": match_id, "status": {"$exists": False}},
            {"$set": {"status": "open"}},
        )
        open_count += res.modified_count

    res = matches_collection.update_many(
        {"_id": {"$nin": list(open_ids)}, "status": {"$exists": False}},
        {"$set": {"status": "settled"}},
    )
    settled_count = res.modified_count
    print(f"  status: open={open_count}件, settled={settled_count}件")

    # 2. name のバックフィル(同日同グループ内は created_at 昇順で連番)
    unnamed = list(
        matches_collection.find(
            {"name": {"$exists": False}},
            sort=[("line_group_id", 1), ("created_at", 1)],
        ),
    )
    seen_counts: dict = defaultdict(int)
    named_count = 0
    for m in unnamed:
        created_at = m.get("created_at")
        if created_at is None:
            print(f"  SKIP (created_at なし): {m['_id']}")
            continue
        key = (m["line_group_id"], created_at.date())
        seen_counts[key] += 1
        seq = seen_counts[key]
        base_name = f"{created_at.month}/{created_at.day}"
        name = base_name if seq == 1 else f"{base_name} ({seq})"
        matches_collection.update_one({"_id": m["_id"]}, {"$set": {"name": name}})
        named_count += 1
    print(f"  name: {named_count}件に付与")

    print("完了")


if __name__ == "__main__":
    migrate()
