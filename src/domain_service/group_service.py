import copy
import logging
from typing import List, Optional

from domain_model.entities.group import Group, GroupMode
from domain_model.entities.group_setting import EmbeddedGroupSettings
from repositories import group_repository

from .interfaces.i_group_service import IGroupService

logger = logging.getLogger(__name__)


class GroupService(IGroupService):

    def find_or_create(self, line_group_id: str) -> Group:
        group = Group(
            line_group_id=line_group_id,
            mode=GroupMode.wait.value,
        )
        return group_repository.find_or_create(group)

    def chmod(
        self,
        line_group_id: str,
        mode: GroupMode,
    ) -> None:
        if not isinstance(mode, GroupMode):
            raise ValueError(f"予期しないモード変更リクエストを受け取りました。'{mode}'")

        if line_group_id is None:
            raise ValueError("LINE Group ID が None のためモードの変更ができません。")

        result = group_repository.update(
            {"line_group_id": line_group_id},
            {"mode": mode.value},
        )
        if result > 0:
            logger.info("chmod: %s: %s", line_group_id, mode.value)

    def get_mode(self, line_group_id: str) -> Optional[str]:
        groups = group_repository.find({"line_group_id": line_group_id})

        if len(groups) == 0:
            return None

        return groups[0].mode

    def find_one_by_line_group_id(self, line_group_id: str) -> Optional[Group]:
        groups = group_repository.find({"line_group_id": line_group_id})

        if len(groups) == 0:
            return None

        return groups[0]

    def update(self, target: Group) -> None:
        # UC-11: use copy to avoid mutating entity.__dict__ during dict comprehension
        entity_dict = copy.copy(target).__dict__
        values = {k: v for k, v in entity_dict.items() if k != "_id"}
        # EmbeddedGroupSettings を dict にシリアライズ
        if "settings" in values and values["settings"] is not None:
            values["settings"] = values["settings"].to_dict()
        # current_input_match_id -> Mongoの既存フィールド名active_match_idへ変換
        # (FEZ-66 Phase D、詳細はgroup_repository.domain_dict_to_mongoのコメント参照)
        values = group_repository.domain_dict_to_mongo(values)
        group_repository.update({"_id": target._id}, values)

    def get_settings_or_create(self, line_group_id: str) -> EmbeddedGroupSettings:
        """group.settings を取得し、未設定の場合はデフォルト設定を作成して保存する"""
        group = self.find_one_by_line_group_id(line_group_id)
        if group is None:
            return EmbeddedGroupSettings()
        if group.settings is not None:
            return group.settings
        # settings が未設定（migration 前のデータ）→ デフォルトを作成して保存
        default_settings = EmbeddedGroupSettings()
        group_repository.update_settings(line_group_id, default_settings)
        return default_settings

    def update_settings(self, line_group_id: str, column: str, value) -> None:
        """group.settings の特定フィールドを更新する"""
        settings = self.get_settings_or_create(line_group_id)
        setattr(settings, column, value)
        group_repository.update_settings(line_group_id, settings)

    def update_group_info(
        self,
        line_group_id: str,
        group_name: str,
        group_picture_url: Optional[str],
    ) -> None:
        group_repository.update(
            {"line_group_id": line_group_id},
            {"group_name": group_name, "group_picture_url": group_picture_url},
        )

    def set_merged_into(self, line_group_id: str, merged_into: str) -> None:
        group_repository.update(
            {"line_group_id": line_group_id},
            {"merged_into": merged_into},
        )

    def get_final_merge_destination(self, line_group_id: str) -> str:
        """指定グループが最終的に統合された先のグループIDを返す。

        A→B→C と連鎖統合されている場合、Aを起点にすると最終到達点のCを返す。
        統合されていなければ自分自身を返す。データ不整合による循環がある場合も
        無限ループしないようガードする。
        """
        current = line_group_id
        seen = {current}
        while True:
            group = self.find_one_by_line_group_id(current)
            if group is None or not group.merged_into or group.merged_into in seen:
                return current
            current = group.merged_into
            seen.add(current)

    def get_effective_line_group_ids(self, line_group_id: str) -> List[str]:
        """指定グループへ直接・間接を問わず統合されたグループを含む実効ID一覧を返す。

        A→B、B→C のように統合が連鎖した場合、Cを起点にすると1階層先のBしか
        拾えずAが漏れてしまうため、統合チェーンを世代ごとに再帰的に辿る。
        """
        effective_ids = [line_group_id]
        frontier = [line_group_id]
        while frontier:
            merged = group_repository.find({"merged_into": {"$in": frontier}})
            frontier = [
                g.line_group_id
                for g in merged
                if g.line_group_id not in effective_ids
            ]
            effective_ids.extend(frontier)
        return effective_ids

    def delete_by_line_group_id(self, line_group_id: str) -> None:
        group_repository.delete(
            {"line_group_id": line_group_id},
        )
