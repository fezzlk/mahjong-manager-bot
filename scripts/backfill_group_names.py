"""Backfill group_name and group_picture_url for existing groups.

Iterates all Group documents that have no group_name yet and fetches
the group summary from LINE API. Groups where the bot has already left
will fail the API call and are silently skipped.

Usage:
  DATABASE_URL=... YOUR_CHANNEL_ACCESS_TOKEN=... DATABASE_NAME=mahjong-manager \
    python3 scripts/backfill_group_names.py

  Or: put DATABASE_URL / YOUR_CHANNEL_ACCESS_TOKEN / DATABASE_NAME in a
  .env.backfill file and run:
    set -a && source .env.backfill && set +a && python3 scripts/backfill_group_names.py
"""
import os

import certifi
from dotenv import load_dotenv
from linebot.v3.messaging import ApiClient, Configuration, MessagingApi
from linebot.v3.messaging.exceptions import ApiException
from pymongo import MongoClient

load_dotenv(".env.backfill")

_DATABASE_URL = os.environ["DATABASE_URL"]
_DATABASE_NAME = os.environ.get("DATABASE_NAME", "mahjong-manager")
_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]

_mongo = MongoClient(_DATABASE_URL, tlsCAFile=certifi.where())
groups_collection = _mongo[_DATABASE_NAME]["groups"]

_cfg = Configuration(access_token=_TOKEN, ssl_ca_cert=certifi.where())
line_bot_api = MessagingApi(ApiClient(_cfg))


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
