"""Atlas → Firestore 全データ移行スクリプト

MongoDB Atlas から Firestore (MongoDB 互換 API) へ全コレクションをコピーし、
スキーマ変換（status→is_deleted, tip→chip）を同時に実行する。

使い方:
  python scripts/migrate_atlas_to_firestore.py \
    --source "mongodb+srv://user:pass@cluster.mongodb.net/?retryWrites=true" \
    --target "mongodb://uid.location.firestore.goog:443/db?loadBalanced=true&authMechanism=SCRAM-SHA-256&tls=true&retryWrites=false" \
    --source-db "mahjong-manager" \
    --target-db "mahjong-manager" \
    [--dry-run]

注意:
  - 移行先に既存データがある場合、_id 重複でエラーになる。
    事前に移行先を空にするか、--drop-target で自動削除。
  - hanchan_matches コレクションは移行しない（refactor-to-v3 で廃止）。
"""

import argparse
import sys
from datetime import datetime

from pymongo import MongoClient
from pymongo.errors import BulkWriteError

# 移行対象コレクション
COLLECTIONS = [
    "line_users",
    "groups",
    "group_settings",
    "user_groups",
    "hanchans",
    "matches",
    "user_matches",
    "user_hanchans",
    "command_aliases",
    "web_users",
    "yakuman_users",
]

# 移行しないコレクション
SKIP_COLLECTIONS = [
    "hanchan_matches",  # refactor-to-v3 で廃止 (DB-05)
]


def transform_hanchan(doc: dict) -> dict:
    """hanchans: status → is_deleted"""
    if "status" in doc and "is_deleted" not in doc:
        doc["is_deleted"] = doc["status"] == 0
        del doc["status"]
    if "is_deleted" not in doc:
        doc["is_deleted"] = False
    return doc


def transform_group_setting(doc: dict) -> dict:
    """group_settings: tip_rate → chip_rate"""
    if "tip_rate" in doc and "chip_rate" not in doc:
        doc["chip_rate"] = doc.pop("tip_rate")
    if "chip_rate" not in doc:
        doc["chip_rate"] = 0
    return doc


def transform_match(doc: dict) -> dict:
    """matches: status → is_deleted, tip_* → chip_*"""
    # status → is_deleted
    if "status" in doc and "is_deleted" not in doc:
        doc["is_deleted"] = doc["status"] == 0
        del doc["status"]
    if "is_deleted" not in doc:
        doc["is_deleted"] = False

    # tip_scores → chip_scores
    if "tip_scores" in doc:
        doc["chip_scores"] = doc.pop("tip_scores")
    if "chip_scores" not in doc:
        doc["chip_scores"] = {}

    # tip_prices → chip_prices
    if "tip_prices" in doc:
        doc["chip_prices"] = doc.pop("tip_prices")
    if "chip_prices" not in doc:
        doc["chip_prices"] = {}

    # sum_prices_with_tip → sum_prices_with_chip
    if "sum_prices_with_tip" in doc:
        doc["sum_prices_with_chip"] = doc.pop("sum_prices_with_tip")
    if "sum_prices_with_chip" not in doc:
        doc["sum_prices_with_chip"] = {}

    return doc


def _ensure_timestamps(doc: dict) -> dict:
    """created_at / updated_at が欠損している場合にデフォルト値を補完"""
    now = datetime.utcnow()
    if "created_at" not in doc or doc["created_at"] is None:
        doc["created_at"] = now
    if "updated_at" not in doc or doc["updated_at"] is None:
        doc["updated_at"] = now
    return doc


def _compose(*funcs):
    """複数の変換関数を合成"""
    def composed(doc):
        for f in funcs:
            doc = f(doc)
        return doc
    return composed


TRANSFORMERS = {
    "hanchans": _compose(transform_hanchan, _ensure_timestamps),
    "matches": _compose(transform_match, _ensure_timestamps),
    "group_settings": _compose(transform_group_setting, _ensure_timestamps),
    "line_users": _ensure_timestamps,
    "groups": _ensure_timestamps,
    "user_groups": _ensure_timestamps,
    "user_matches": _ensure_timestamps,
    "user_hanchans": _ensure_timestamps,
    "command_aliases": _ensure_timestamps,
}


def migrate_collection(
    source_db,
    target_db,
    collection_name: str,
    dry_run: bool = False,
) -> dict:
    """1コレクションを移行し、結果を返す。"""
    source_col = source_db[collection_name]
    target_col = target_db[collection_name]

    docs = list(source_col.find())
    source_count = len(docs)

    if source_count == 0:
        print(f"  [{collection_name}] 0 docs (skip)")
        return {"collection": collection_name, "source": 0, "target": 0, "status": "skip"}

    # スキーマ変換
    transformer = TRANSFORMERS.get(collection_name)
    if transformer:
        docs = [transformer(doc) for doc in docs]
        print(f"  [{collection_name}] {source_count} docs (transformed)")
    else:
        print(f"  [{collection_name}] {source_count} docs")

    if dry_run:
        print(f"  [{collection_name}] DRY RUN: would insert {source_count} docs")
        return {"collection": collection_name, "source": source_count, "target": 0, "status": "dry_run"}

    # 書き込み
    try:
        result = target_col.insert_many(docs, ordered=False)
        inserted = len(result.inserted_ids)
    except BulkWriteError as e:
        inserted = e.details.get("nInserted", 0)
        print(f"  [{collection_name}] WARNING: BulkWriteError - {inserted}/{source_count} inserted")

    # 検証
    target_count = target_col.count_documents({})
    status = "ok" if target_count == source_count else "MISMATCH"
    if status == "MISMATCH":
        print(f"  [{collection_name}] ERROR: source={source_count}, target={target_count}")
    else:
        print(f"  [{collection_name}] OK: {target_count} docs")

    return {
        "collection": collection_name,
        "source": source_count,
        "target": target_count,
        "status": status,
    }


def main():
    parser = argparse.ArgumentParser(description="Atlas → Firestore migration")
    parser.add_argument("--source", required=True, help="Source MongoDB Atlas URL")
    parser.add_argument("--target", required=True, help="Target Firestore MongoDB URL")
    parser.add_argument("--source-db", default="mahjong-manager", help="Source DB name")
    parser.add_argument("--target-db", default="mahjong-manager", help="Target DB name")
    parser.add_argument("--dry-run", action="store_true", help="Don't write, just show what would happen")
    parser.add_argument("--drop-target", action="store_true", help="Drop target collections before migration")
    args = parser.parse_args()

    print(f"Migration started at {datetime.now().isoformat()}")
    print(f"Source DB: {args.source_db}")
    print(f"Target DB: {args.target_db}")
    print(f"Dry run: {args.dry_run}")
    print()

    source_client = MongoClient(args.source)
    target_client = MongoClient(args.target)
    source_db = source_client[args.source_db]
    target_db = target_client[args.target_db]

    # 接続確認
    try:
        source_client.admin.command("ping")
        print("Source (Atlas): connected")
    except Exception as e:
        print(f"ERROR: Cannot connect to source: {e}")
        sys.exit(1)

    try:
        target_client.admin.command("ping")
        print("Target (Firestore): connected")
    except Exception as e:
        print(f"ERROR: Cannot connect to target: {e}")
        sys.exit(1)

    print()

    # スキップ対象の確認
    for skip_name in SKIP_COLLECTIONS:
        count = source_db[skip_name].count_documents({})
        print(f"  [{skip_name}] SKIP: {count} docs (not migrated)")
    print()

    # ターゲットの既存データ削除
    # NOTE: Firestore MongoDB API では drop() が非サポートのため delete_many を使用
    if args.drop_target and not args.dry_run:
        print("Clearing target collections...")
        for name in COLLECTIONS:
            result = target_db[name].delete_many({})
            print(f"  [{name}] deleted {result.deleted_count} docs")
        print()

    # 移行実行
    results = []
    for name in COLLECTIONS:
        result = migrate_collection(source_db, target_db, name, dry_run=args.dry_run)
        results.append(result)

    # サマリー
    print()
    print("=" * 60)
    print("Migration Summary")
    print("=" * 60)
    total_source = 0
    total_target = 0
    has_error = False
    for r in results:
        total_source += r["source"]
        total_target += r["target"]
        flag = "" if r["status"] in ("ok", "skip", "dry_run") else " *** ERROR ***"
        if flag:
            has_error = True
        print(f"  {r['collection']:25s} source={r['source']:5d}  target={r['target']:5d}  {r['status']}{flag}")

    print(f"  {'TOTAL':25s} source={total_source:5d}  target={total_target:5d}")
    print()

    if has_error:
        print("MIGRATION COMPLETED WITH ERRORS. Please investigate.")
        sys.exit(1)
    else:
        print("Migration completed successfully.")
        if not args.dry_run:
            print("Next steps:")
            print("  1. Run scripts/setup_indexes.py on the target DB")
            print("  2. Run scripts/verify_migration.py to validate data integrity")


if __name__ == "__main__":
    main()
