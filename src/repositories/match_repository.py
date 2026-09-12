import copy
from datetime import datetime
from typing import Dict, List, Optional, Tuple

from pymongo import ASCENDING, ReturnDocument

from domain_model.entities.group_setting import EmbeddedGroupSettings
from domain_model.entities.match import Match, MatchStatus
from domain_model.i_repositories.i_match_repository import IMatchRepository
from mongo_client import matches_collection


def _sum_scores_to_list(scores: Dict[str, int]) -> List[dict]:
    """Python Dict → MongoDB list 形式に変換する"""
    if not scores:
        return []
    return [{"line_user_id": uid, "score": s} for uid, s in scores.items()]


def _sum_scores_to_dict(scores) -> Dict[str, int]:
    """MongoDB list 形式 → Python Dict に変換する(後方互換: dict 形式もそのまま受け入れる)"""
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
        if new_dict.get("settings") is not None:
            new_dict["settings"] = new_dict["settings"].to_dict()
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
        if new_values.get("settings") is not None:
            new_values["settings"] = new_values["settings"].to_dict()
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

    def count(self, query: Dict[str, any] = None) -> int:
        """条件に一致する件数のみを返す。

        件数が閾値を超えるかの判定用に、find()して長さを取るより安価。
        """
        filter_query = {**(query or {}), "is_deleted": {"$ne": True}}
        return matches_collection.count_documents(filter_query)

    def update_field(
        self,
        query: Dict[str, any],
        set_values: Dict[str, any] = None,
        unset_fields: List[str] = None,
    ) -> Optional[Match]:
        """指定フィールドのみをアトミックに$set/$unset更新し、更新後のレコードを返す。

        update()は対象フィールド全体を読み込み→メモリ上で変更→丸ごと書き戻すため、
        同時実行時に他の更新を上書きして消してしまう(read-modify-write競合)。
        chip_scores.<line_user_id>のようなフィールドパス単位で更新することでこれを避ける。
        """
        filter_query = {**query, "is_deleted": {"$ne": True}}
        update_ops: Dict[str, any] = {}
        values = dict(set_values or {})
        if "sum_scores" in values:
            values["sum_scores"] = _sum_scores_to_list(values["sum_scores"])
        values["updated_at"] = datetime.now()
        update_ops["$set"] = values
        if unset_fields:
            update_ops["$unset"] = dict.fromkeys(unset_fields, "")

        # ドット区切りパス(例: chip_scores.<uid>)の親フィールドがnullの場合、
        # MongoDBはnullの子要素を作成できずエラーになる。事前にnullなら{}へ
        # 自己修復しておく(通常は親が既にdictなので何もマッチせず無視される)。
        dotted_paths = list(values.keys()) + list(unset_fields or [])
        parent_fields = {p.split(".", 1)[0] for p in dotted_paths if "." in p}
        for parent in parent_fields:
            matches_collection.update_one(
                {**filter_query, parent: None},
                {"$set": {parent: {}}},
            )

        # update_one() + find(query) の二段構えだと、queryに含めたフィールド自体を
        # このupdateで書き換える場合(例: active_hanchan_idを条件にして同じ値をクリアする
        # CAS操作)、更新後のfind(query)がもう一致せずNoneを返してしまう。
        # find_one_and_update()で更新後のドキュメントを直接受け取ることでこれを避ける。
        result = matches_collection.find_one_and_update(
            filter_query,
            update_ops,
            return_document=ReturnDocument.AFTER,
        )
        if result is None:
            return None
        return self._mapping_record_to_domain(result)

    def delete(
        self,
        query: Dict[str, any] = None,
    ) -> int:
        if not query:
            raise ValueError("delete() requires a non-empty query to prevent accidental full-collection deletion")
        result = matches_collection.delete_many(filter=query)
        return result.deleted_count

    def _mapping_record_to_domain(self, record: Dict[str, any]) -> Match:
        raw_settings = record.get("settings")
        settings = EmbeddedGroupSettings.from_dict(raw_settings) if raw_settings else None
        return Match(
            line_group_id=record.get("line_group_id"),
            is_deleted=record.get("is_deleted", False),
            # 未マイグレーションの既存レコードは大半が精算済みのため、
            # status欠落時は安全側(settled)にフォールバックする。
            # 新規作成時は常に明示的にopenを書き込むため、この既定値は
            # 未マイグレーションの古いレコードを読んだ時にのみ効く。
            status=record.get("status", MatchStatus.settled.value),
            name=record.get("name"),
            settings=settings,
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
