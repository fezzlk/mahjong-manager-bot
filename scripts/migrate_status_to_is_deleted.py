"""DB-01 migration: status:int → is_deleted:bool

Run once after deploying the code change.

  hanchans / matches:
    status == 0  (DISABLE) → is_deleted = True
    status != 0  (ACTIVE/ARCHIVE) → is_deleted = False
    field "status" is removed after migration.

Usage:
  PYTHONPATH=src python scripts/migrate_status_to_is_deleted.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import env_var  # noqa: F401 — loads .env
from mongo_client import hanchans_collection, matches_collection


def migrate_collection(collection, name: str) -> None:
    # 0 → is_deleted=True
    res = collection.update_many(
        {"status": 0, "is_deleted": {"$exists": False}},
        {"$set": {"is_deleted": True}, "$unset": {"status": ""}},
    )
    print(f"[{name}] status=0 → is_deleted=True : {res.modified_count} docs")

    # non-zero → is_deleted=False
    res = collection.update_many(
        {"status": {"$exists": True}, "is_deleted": {"$exists": False}},
        {"$set": {"is_deleted": False}, "$unset": {"status": ""}},
    )
    print(f"[{name}] status≠0 → is_deleted=False : {res.modified_count} docs")


if __name__ == "__main__":
    migrate_collection(hanchans_collection, "hanchans")
    migrate_collection(matches_collection, "matches")
    print("Migration complete.")
