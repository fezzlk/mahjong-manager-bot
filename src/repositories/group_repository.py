import copy
from datetime import datetime
from typing import Dict, List, Tuple

from pymongo import ASCENDING, ReturnDocument

from domain_model.entities.group import Group
from domain_model.entities.group_setting import EmbeddedGroupSettings
from domain_model.i_repositories.i_group_repository import IGroupRepository
from mongo_client import groups_collection


class GroupRepository(IGroupRepository):

    def create(
        self,
        new_record: Group,
    ) -> Group:
        if len(self.find(query={"line_group_id": new_record.line_group_id})) != 0:
            raise Exception(f"LINE Group ID: {new_record.line_group_id} のGroupはすでに存在しています。")

        new_dict = self.domain_dict_to_mongo(copy.deepcopy(new_record.__dict__))
        if new_record._id is None:
            new_dict.pop("_id")
        result = groups_collection.insert_one(new_dict)
        new_record._id = result.inserted_id
        return new_record

    def find_or_create(self, new_record: Group) -> Group:
        """TOCTOU レースフリーな upsert による find-or-create"""
        new_dict = self.domain_dict_to_mongo(
            {k: v for k, v in new_record.__dict__.items() if k != "_id"},
        )
        result = groups_collection.find_one_and_update(
            filter={"line_group_id": new_record.line_group_id},
            update={"$setOnInsert": new_dict},
            upsert=True,
            return_document=ReturnDocument.AFTER,
        )
        return self._mapping_record_to_domain(result)

    @staticmethod
    def domain_dict_to_mongo(d: Dict[str, any]) -> Dict[str, any]:
        """current_input_match_id属性をMongoの既存フィールド名active_match_idへ戻す。

        Python属性名とMongoフィールド名を意図的に乖離させている(FEZ-66 Phase D、
        データマイグレーション不要にするため)ので、Group.__dict__由来の書き込みは
        すべてこの変換を経由する必要がある(group_service.update()からも呼ばれる)。
        """
        if "current_input_match_id" in d:
            d["active_match_id"] = d.pop("current_input_match_id")
        return d

    def update(
        self,
        query: Dict[str, any],
        new_values: Dict[str, any],
    ) -> int:
        new_values["updated_at"] = datetime.now()
        result = groups_collection.update_one(query, {"$set": new_values})
        return result.matched_count

    def find(
        self,
        query: Dict[str, any] = None,
        sort: List[Tuple[str, any]] = [("_id", ASCENDING)],
        limit: int = 0,
    ) -> List[Group]:
        records = groups_collection\
            .find(filter=dict(query) if query is not None else {})\
            .sort(sort)\
            .limit(limit)
        return [self._mapping_record_to_domain(record) for record in records]

    def delete(
        self,
        query: Dict[str, any] = None,
    ) -> int:
        if not query:
            raise ValueError("delete() requires a non-empty query to prevent accidental full-collection deletion")
        result = groups_collection.delete_many(filter=query)
        return result.deleted_count

    def update_settings(self, line_group_id: str, settings: EmbeddedGroupSettings) -> int:
        return self.update(
            query={"line_group_id": line_group_id},
            new_values={"settings": settings.to_dict()},
        )

    def _mapping_record_to_domain(self, record: Dict[str, any]) -> Group:
        raw_settings = record.get("settings")
        settings = EmbeddedGroupSettings.from_dict(raw_settings) if raw_settings else None
        return Group(
            line_group_id=record.get("line_group_id"),
            mode=record.get("mode"),
            # Mongoのフィールド名はactive_match_idのまま(FEZ-66 Phase Dでの意図的な
            # 命名乖離、詳細はGroupエンティティのコメント参照)。
            current_input_match_id=record.get("active_match_id"),
            sim_match_id=record.get("sim_match_id"),
            settings=settings,
            last_command=record.get("last_command"),
            group_name=record.get("group_name"),
            group_picture_url=record.get("group_picture_url"),
            last_command_at=record.get("last_command_at"),
            merged_into=record.get("merged_into"),
            created_at=record.get("created_at"),
            updated_at=record.get("updated_at"),
            _id=record.get("_id"),
        )
