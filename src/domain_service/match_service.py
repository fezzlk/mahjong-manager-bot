import copy
import logging
from typing import Dict, List, Optional

from bson.objectid import ObjectId
from pymongo import ASCENDING, DESCENDING

from domain_model.entities.match import Match
from repositories import match_repository

from .interfaces.i_match_service import IMatchService

logger = logging.getLogger(__name__)

class MatchService(IMatchService):
    def add_or_drop_chip_score(
        self,
        match_id: ObjectId,
        line_user_id: str,
        chip_score: Optional[int],
    ) -> Match:
        if line_user_id is None:
            raise ValueError("fail to add_or_drop_chip_score: line_user_id is required")

        field = f"chip_scores.{line_user_id}"
        if chip_score is None:
            target = match_repository.update_field(
                {"_id": match_id},
                unset_fields=[field],
            )
        else:
            target = match_repository.update_field(
                {"_id": match_id},
                set_values={field: chip_score},
            )

        if target is None:
            raise ValueError("Not found match")

        return target

    def try_clear_active_hanchan(
        self,
        match_id: ObjectId,
        hanchan_id: ObjectId,
    ) -> bool:
        """指定した hanchan が現在も active_hanchan である場合のみアトミックにクリアする(CAS)。

        4人分の得点がほぼ同時に揃うと、複数リクエストが並行して半荘確定処理
        (SubmitHanchanUseCase)に入りうる。この所有権確定を通った1件だけが後続の
        精算・UserGroup/UserMatch作成・完了メッセージ送信を行うことで、重複実行を防ぐ。
        """
        target = match_repository.update_field(
            {"_id": match_id, "active_hanchan_id": hanchan_id},
            set_values={"active_hanchan_id": None},
        )
        return target is not None

    def restore_active_hanchan(
        self,
        match_id: ObjectId,
        hanchan_id: ObjectId,
    ) -> None:
        """try_clear_active_hanchan()後にDBエラーが起きた場合、半荘を再試行可能な状態へ戻す。

        クリアしたまま復元しないと、対局はactive_hanchanを失ったまま宙に浮き、
        次の得点入力を受け付けられなくなってしまう。ただし、復元は
        active_hanchan_idが依然Noneのまま(他の処理が割り込んでいない)場合の
        みに限定するCAS操作とし、その間に別の対局が新たに開始されていた場合は
        その状態を上書きしないようにする(ベストエフォート)。
        """
        match_repository.update_field(
            {"_id": match_id, "active_hanchan_id": None},
            set_values={"active_hanchan_id": hanchan_id},
        )

    def update_sum_scores(
        self,
        match_id: ObjectId,
        sum_scores: Dict[str, int],
    ) -> None:
        """半荘確定処理の完了時、対局全体の累計スコアのみを更新する。

        この時点でactive_hanchan_idは既にtry_clear_active_hanchan()で
        クリア済み。ここでMatchエンティティ全体をupdate()すると、確定処理の
        実行中に別の対局(_sim等)が新たにactive_hanchan_idを割り当てていた
        場合、その状態を古いローカルの値(None)で上書きし孤立させてしまう。
        sum_scoresのみをフィールド単位で更新することでこれを避ける。
        """
        match_repository.update_field(
            {"_id": match_id},
            set_values={"sum_scores": sum_scores},
        )

    def find_one_by_id(self, _id: ObjectId) -> Optional[Match]:
        matches = match_repository.find(
            {"_id": _id},
        )
        if len(matches) == 0:
            return None
        return matches[0]

    def create_with_line_group_id(self, line_group_id: str) -> Match:
        new_match = Match(
            line_group_id=line_group_id,
        )
        match_repository.create(new_match)

        logger.info('create match: group "%s"', line_group_id)
        return new_match

    def update(self, target: Match) -> None:
        # UC-11: use copy to avoid mutating entity.__dict__ during dict comprehension
        entity_dict = copy.copy(target).__dict__
        match_repository.update(
            {"_id": target._id},
            {k: v for k, v in entity_dict.items() if k != "_id"},
        )

    def find_all_for_graph(self, ids: List[ObjectId]) -> List[Match]:
        return match_repository.find(
            query={"_id": {"$in": ids}},
            sort=[("created_at", ASCENDING)],
        )

    def find_all_by_ids_and_line_group_ids(
        self, ids: List[ObjectId], line_group_ids: List[str],
    ) -> List[Match]:
        return match_repository.find(
            query={"_id": {"$in": ids}, "line_group_id": {"$in": line_group_ids}},
            sort=[("created_at", ASCENDING)],
        )

    def find_latest_one(self, line_group_id: str) -> Optional[Match]:
        matches = match_repository.find(
            query={"line_group_id": line_group_id},
            sort=[("created_at", DESCENDING)],
        )
        if len(matches) == 0:
            return None
        return matches[0]

    def find_all_archived_by_line_group_id(self, line_group_id: str) -> List[Match]:
        # 将来的にはGroupに含まれるメンバーの半荘のみを対象とする
        return match_repository.find(
            query={
                "line_group_id": line_group_id,
                "sum_prices_with_chip": {"$ne": {}},
            },
            sort=[("created_at", ASCENDING)],
        )
