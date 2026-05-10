"""Backfill group_name and group_picture_url for existing groups.

Iterates all Group documents that have no group_name yet and fetches
the group summary from LINE API. Groups where the bot has already left
will fail the API call and are silently skipped.

Usage:
  PYTHONPATH=src python scripts/backfill_group_names.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from linebot.v3.exceptions import ApiException

import env_var  # noqa: F401 — loads .env
from messaging_api_setting import line_bot_api
from mongo_client import groups_collection


def main() -> None:
    targets = list(groups_collection.find({"group_name": {"$exists": False}}))
    print(f"対象グループ数: {len(targets)}")

    updated = 0
    skipped = 0

    for doc in targets:
        group_id = doc["line_group_id"]
        try:
            summary = line_bot_api.get_group_summary(group_id)
            groups_collection.update_one(
                {"line_group_id": group_id},
                {"$set": {
                    "group_name": summary.group_name,
                    "group_picture_url": summary.picture_url,
                }},
            )
            print(f"[SUCCESS] {group_id} → {summary.group_name}")
            updated += 1
        except ApiException as e:
            print(f"[SKIP]    {group_id} → API error ({e.status})")
            skipped += 1

    print(f"\nDone: {updated} updated, {skipped} skipped")


if __name__ == "__main__":
    main()
