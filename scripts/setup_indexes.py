#!/usr/bin/env python3
"""
MongoDB インデックス設定スクリプト (REPO-06)

各コレクションに一意インデックスを設定する。
初回デプロイ時または DB 再作成時に一度だけ実行する。

使い方:
    cd /path/to/project
    python scripts/setup_indexes.py
"""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import dotenv
dotenv.load_dotenv()

from pymongo import ASCENDING
from mongo_client import (
    groups_collection,
    group_settings_collection,
    line_users_collection,
    user_groups_collection,
    user_hanchans_collection,
    user_matches_collection,
    hanchans_collection,
    matches_collection,
    command_aliases_collection,
)


def setup_indexes():
    print("インデックス設定を開始します...")

    # groups: line_group_id で一意
    groups_collection.create_index(
        [("line_group_id", ASCENDING)],
        unique=True,
        name="idx_groups_line_group_id_unique",
    )
    print("  groups.line_group_id: unique index OK")

    # group_settings: line_group_id で一意
    group_settings_collection.create_index(
        [("line_group_id", ASCENDING)],
        unique=True,
        name="idx_group_settings_line_group_id_unique",
    )
    print("  group_settings.line_group_id: unique index OK")

    # line_users: line_user_id で一意
    line_users_collection.create_index(
        [("line_user_id", ASCENDING)],
        unique=True,
        name="idx_line_users_line_user_id_unique",
    )
    print("  line_users.line_user_id: unique index OK")

    # user_groups: (line_user_id, line_group_id) 複合で一意
    user_groups_collection.create_index(
        [("line_user_id", ASCENDING), ("line_group_id", ASCENDING)],
        unique=True,
        name="idx_user_groups_composite_unique",
    )
    print("  user_groups.(line_user_id, line_group_id): unique index OK")

    # hanchans: match_id でフィルタが多いのでインデックス
    hanchans_collection.create_index(
        [("match_id", ASCENDING), ("status", ASCENDING)],
        name="idx_hanchans_match_id_status",
    )
    print("  hanchans.(match_id, status): index OK")

    # matches: line_group_id でフィルタが多いのでインデックス
    matches_collection.create_index(
        [("line_group_id", ASCENDING), ("status", ASCENDING)],
        name="idx_matches_line_group_id_status",
    )
    print("  matches.(line_group_id, status): index OK")

    # user_hanchans: (line_user_id, hanchan_id) 複合で一意
    user_hanchans_collection.create_index(
        [("line_user_id", ASCENDING), ("hanchan_id", ASCENDING)],
        unique=True,
        name="idx_user_hanchans_composite_unique",
    )
    print("  user_hanchans.(line_user_id, hanchan_id): unique index OK")

    # user_matches: (user_id, match_id) 複合で一意
    user_matches_collection.create_index(
        [("user_id", ASCENDING), ("match_id", ASCENDING)],
        unique=True,
        name="idx_user_matches_composite_unique",
    )
    print("  user_matches.(user_id, match_id): unique index OK")

    # command_aliases: (line_user_id, alias) でフィルタが多いのでインデックス
    command_aliases_collection.create_index(
        [("line_user_id", ASCENDING), ("alias", ASCENDING)],
        name="idx_command_aliases_user_alias",
    )
    print("  command_aliases.(line_user_id, alias): index OK")

    print("\nインデックス設定が完了しました。")


if __name__ == "__main__":
    setup_indexes()
