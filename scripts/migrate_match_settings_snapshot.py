#!/usr/bin/env python3
"""FEZ-66 Phase D マイグレーション: 進行中(open)MatchにMatch.settingsをバックフィル

実行手順:
    cd /path/to/project
    python scripts/migrate_match_settings_snapshot.py

内容:
    - status="open"かつsettings未設定のMatchに、そのMatchが属するGroupの
      現在のsettingsをコピーする(ベストエフォート。開設時点のレート等は
      分からないため、実行時点のグループ設定を使う)
    - 精算済み(settled)・sim用サンドボックスのMatchは対象外(Phase Dの
      コード側フォールバックで表示上問題ないため、履歴データは触らない)
    - グループにsettings未設定の場合はデフォルト設定(EmbeddedGroupSettings())
      を使う

注意:
    - この script は idempotent(何度実行しても安全)。既にsettingsが
      設定済みのMatchはスキップする。
    - バックフィル対象は手動確認できるようログ出力する。
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import env_var  # noqa: F401 — loads .env
from domain_model.entities.group_setting import EmbeddedGroupSettings
from mongo_client import groups_collection, matches_collection


def migrate():
    print("FEZ-66 Phase D マイグレーション開始: Match.settings バックフィル(openのみ)")

    open_matches = list(
        matches_collection.find(
            {"status": "open", "settings": {"$exists": False}},
        ),
    )

    settings_cache: dict = {}
    updated_count = 0
    for match in open_matches:
        line_group_id = match["line_group_id"]
        if line_group_id not in settings_cache:
            group = groups_collection.find_one({"line_group_id": line_group_id})
            raw_settings = group.get("settings") if group else None
            settings = (
                EmbeddedGroupSettings.from_dict(raw_settings)
                if raw_settings
                else EmbeddedGroupSettings()
            )
            settings_cache[line_group_id] = settings.to_dict()

        matches_collection.update_one(
            {"_id": match["_id"], "settings": {"$exists": False}},
            {"$set": {"settings": settings_cache[line_group_id]}},
        )
        updated_count += 1
        print(f"  match={match['_id']} line_group_id={line_group_id} settings={settings_cache[line_group_id]}")

    print(f"完了: {updated_count}件のopen Matchにsettingsをバックフィル")


if __name__ == "__main__":
    migrate()
