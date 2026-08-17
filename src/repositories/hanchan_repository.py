import copy
from datetime import datetime
from typing import Dict, List, Optional, Tuple

from pymongo import ASCENDING, ReturnDocument

from domain_model.entities.hanchan import Hanchan
from domain_model.entities.user_hanchan import UserHanchanResult
from domain_model.i_repositories.i_hanchan_repository import IHanchanRepository
from mongo_client import hanchans_collection


def _results_to_list(results) -> list:
    """UserHanchanResult リスト → MongoDB 用 dict リストに変換"""
    if not results:
        return []
    return [r.to_dict() if hasattr(r, "to_dict") else r for r in results]


class HanchanRepository(IHanchanRepository):

    def create(
        self,
        new_record: Hanchan,
    ) -> Hanchan:
        new_dict = copy.deepcopy(new_record.__dict__)
        if new_record._id is None:
            new_dict.pop("_id")
        new_dict["results"] = _results_to_list(new_dict.get("results", []))
        result = hanchans_collection.insert_one(new_dict)
        new_record._id = result.inserted_id
        return new_record

    def update(
        self,
        query: Dict[str, any],
        new_values: Dict[str, any],
    ) -> int:
        filter_query = {**query, "is_deleted": {"$ne": True}}
        new_values["updated_at"] = datetime.now()
        if "results" in new_values:
            new_values["results"] = _results_to_list(new_values["results"])
        result = hanchans_collection.update_one(filter_query, {"$set": new_values})
        return result.matched_count

    def update_field(
        self,
        query: Dict[str, any],
        set_values: Dict[str, any] = None,
        unset_fields: List[str] = None,
    ) -> Optional[Hanchan]:
        """指定フィールドのみをアトミックに$set/$unset更新し、更新後のレコードを返す。

        update()は対象フィールド全体を読み込み→メモリ上で変更→丸ごと書き戻すため、
        同時実行時に他の更新を上書きして消してしまう(read-modify-write競合)。
        raw_scores.<line_user_id>のようなフィールドパス単位で更新することでこれを避ける。
        """
        filter_query = {**query, "is_deleted": {"$ne": True}}
        update_ops: Dict[str, any] = {}
        values = dict(set_values or {})
        values["updated_at"] = datetime.now()
        update_ops["$set"] = values
        if unset_fields:
            update_ops["$unset"] = dict.fromkeys(unset_fields, "")

        # ドット区切りパス(例: raw_scores.<uid>)の親フィールドがnullの場合、
        # MongoDBはnullの子要素を作成できずエラーになる。事前にnullなら{}へ
        # 自己修復しておく(通常は親が既にdictなので何もマッチせず無視される)。
        dotted_paths = list(values.keys()) + list(unset_fields or [])
        parent_fields = {p.split(".", 1)[0] for p in dotted_paths if "." in p}
        for parent in parent_fields:
            hanchans_collection.update_one(
                {**filter_query, parent: None},
                {"$set": {parent: {}}},
            )

        # update_one() + find(query) の二段構えだと、queryに含めたフィールド自体を
        # このupdateで書き換える場合、更新後のfind(query)がもう一致せずNoneを返して
        # しまう。find_one_and_update()で更新後のドキュメントを直接受け取ることで避ける。
        result = hanchans_collection.find_one_and_update(
            filter_query,
            update_ops,
            return_document=ReturnDocument.AFTER,
        )
        if result is None:
            return None
        return self._mapping_record_to_domain(result)

    def update_many(
        self,
        query: Dict[str, any],
        new_values: Dict[str, any],
    ) -> int:
        """複数ドキュメントを一括更新する(bulk archive 等の用途専用)"""
        filter_query = {**query, "is_deleted": {"$ne": True}}
        new_values["updated_at"] = datetime.now()
        result = hanchans_collection.update_many(filter_query, {"$set": new_values})
        return result.matched_count

    def find(
        self,
        query: Dict[str, any] = None,
        sort: List[Tuple[str, any]] = [("_id", ASCENDING)],
        limit: int = 0,
    ) -> List[Hanchan]:
        filter_query = {**(query or {}), "is_deleted": {"$ne": True}}
        records = hanchans_collection\
            .find(filter=filter_query)\
            .sort(sort)\
            .limit(limit)
        return [self._mapping_record_to_domain(record) for record in records]

    def delete(
        self,
        query: Dict[str, any] = None,
    ) -> int:
        if not query:
            raise ValueError("delete() requires a non-empty query to prevent accidental full-collection deletion")
        result = hanchans_collection.delete_many(filter=query)
        return result.deleted_count

    def _mapping_record_to_domain(self, record: Dict[str, any]) -> Hanchan:
        raw_results = record.get("results") or []
        return Hanchan(
            line_group_id=record.get("line_group_id"),
            match_id=record.get("match_id"),
            is_deleted=record.get("is_deleted", False),
            raw_scores=record.get("raw_scores"),
            converted_scores=record.get("converted_scores"),
            results=[UserHanchanResult.from_dict(r) for r in raw_results],
            created_at=record.get("created_at"),
            updated_at=record.get("updated_at"),
            _id=record.get("_id"),
        )
