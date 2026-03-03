import copy
from datetime import datetime
from typing import Dict, List, Tuple

from pymongo import ASCENDING

from domain_model.entities.match import Match
from domain_model.i_repositories.i_match_repository import IMatchRepository
from mongo_client import matches_collection


def _sum_scores_to_list(scores: Dict[str, int]) -> List[dict]:
    """Python Dict → MongoDB list 形式に変換する"""
    if not scores:
        return []
    return [{"line_user_id": uid, "score": s} for uid, s in scores.items()]


def _sum_scores_to_dict(scores) -> Dict[str, int]:
    """MongoDB list 形式 → Python Dict に変換する（後方互換: dict 形式もそのまま受け入れる）"""
    if scores is None:
        return {}
    if isinstance(scores, list):
        return {item["line_user_id"]: item["score"] for item in scores}
    # 旧 dict 形式
    return scores


class MatchRepository(IMatchRepository):
    def create(
        self,
        new_record: Match,
    ) -> Match:
        new_dict = copy.deepcopy(new_record.__dict__)
        if new_record._id is None:
            new_dict.pop("_id")
        # sum_scores を list 形式で保存
        if "sum_scores" in new_dict:
            new_dict["sum_scores"] = _sum_scores_to_list(new_dict["sum_scores"])
        result = matches_collection.insert_one(new_dict)
        new_record._id = result.inserted_id
        return new_record

    def update(
        self,
        query: Dict[str, any],
        new_values: Dict[str, any],
    ) -> int:
        filter_query = {**query, "is_deleted": {"$ne": True}}
        new_values["updated_at"] = datetime.now()
        # sum_scores を list 形式で保存
        if "sum_scores" in new_values:
            new_values["sum_scores"] = _sum_scores_to_list(new_values["sum_scores"])
        result = matches_collection.update_one(filter_query, {"$set": new_values})
        return result.matched_count

    def find(
        self,
        query: Dict[str, any] = None,
        sort: List[Tuple[str, any]] = [("_id", ASCENDING)],
        limit: int = 0,
    ) -> List[Match]:
        filter_query = {**(query or {}), "is_deleted": {"$ne": True}}
        records = matches_collection.find(filter=filter_query).sort(sort).limit(limit)
        return [self._mapping_record_to_domain(record) for record in records]

    def delete(
        self,
        query: Dict[str, any] = None,
    ) -> int:
        if not query:
            raise ValueError("delete() requires a non-empty query to prevent accidental full-collection deletion")
        result = matches_collection.delete_many(filter=query)
        return result.deleted_count

    def _mapping_record_to_domain(self, record: Dict[str, any]) -> Match:
        return Match(
            line_group_id=record.get("line_group_id"),
            is_deleted=record.get("is_deleted", False),
            created_at=record.get("created_at"),
            updated_at=record.get("updated_at"),
            chip_scores=record.get("chip_scores"),
            chip_prices=record.get("chip_prices"),
            active_hanchan_id=record.get("active_hanchan_id"),
            sum_scores=_sum_scores_to_dict(record.get("sum_scores")),
            sum_prices=record.get("sum_prices"),
            sum_prices_with_chip=record.get("sum_prices_with_chip"),
            _id=record.get("_id"),
            original_id=record.get("original_id"),
        )
