from typing import Dict, List
from repositories import session_scope, hanchan_repository
from domains.Hanchan import Hanchan
from domains.Match import Match
from .interfaces.IHanchanService import IHanchanService

STATUS_LIST = ['disabled', 'active', 'archived']


class HanchanService(IHanchanService):
    def create(
        self,
        raw_scores: Dict[str, int],
        line_room_id: str,
        related_match: Match,
    ) -> Hanchan:
        new_hanchan = Hanchan(
            line_room_id=line_room_id,
            raw_scores=raw_scores,
            converted_scores='',
            match_id=related_match._id,
            status=1,
        )
        with session_scope() as session:
            hanchan_repository.create(
                session,
                new_hanchan,
            )

        print(
            f'create hanchan: to room "{line_room_id}"'
        )

        return new_hanchan

    def disabled_by_id(
        self,
        line_room_id: str,
        hanchan_id: int,
    ) -> Hanchan:
        """disabled target hanchan"""
        with session_scope() as session:
            new_hanchan = hanchan_repository.update_status_by_id_and_line_room_id(
                session,
                hanchan_id=hanchan_id,
                line_room_id=line_room_id,
                status=0,
            )

            print(
                f'disabled: id={hanchan_id}'
            )

            return new_hanchan

    def find_by_ids(
        self,
        ids: List[str],
    ) -> List[Hanchan]:
        with session_scope() as session:
            return hanchan_repository.find_by_ids(session, ids)

    def get_current(self, line_room_id):
        with session_scope() as session:
            return hanchan_repository.find_one_by_line_room_id_and_status(
                session,
                line_room_id,
                1
            )

    def add_raw_score(
        self,
        line_room_id: str,
        line_user_id: str,
        raw_score: int,
    ) -> Hanchan:
        with session_scope() as session:
            hanchan = hanchan_repository.update_raw_score_of_user_by_room_id(
                session=session,
                line_room_id=line_room_id,
                line_user_id=line_user_id,
                raw_score=raw_score,
            )

            return hanchan

    def drop_raw_score(
        self,
        line_room_id: str,
        line_user_id: str,
    ) -> Hanchan:
        with session_scope() as session:
            hanchan = hanchan_repository.update_raw_score_of_user_by_room_id(
                session=session,
                line_room_id=line_room_id,
                line_user_id=line_user_id,
                raw_score=None,
            )

            return hanchan

    def update_converted_score(
        self,
        line_room_id: str,
        converted_scores: Dict[str, int],
    ) -> Hanchan:
        with session_scope() as session:
            hanchan = hanchan_repository.update_one_converted_score_by_line_room_id(
                session=session,
                line_room_id=line_room_id,
                converted_scores=converted_scores,
            )

            print(
                f'update hanchan: id={hanchan._id}'
            )

            return hanchan

    def update_status(
        self,
        line_room_id: str,
        status: int,
    ) -> Hanchan:
        with session_scope() as session:
            hanchan = hanchan_repository.update_status_by_line_room_id(
                session,
                line_room_id,
                status,
            )

            if hanchan is None:
                return None

            print(
                f'{STATUS_LIST[status]} hanchan: id={hanchan._id}'
            )

            return hanchan

    def archive(self, line_room_id: str) -> Hanchan:
        return self.update_status(line_room_id, 2)

    def disable(self, line_room_id: str) -> Hanchan:
        return self.update_status(line_room_id, 0)

    def get(self, ids: List[int] = None) -> List[Hanchan]:
        with session_scope() as session:
            if ids is None:
                targets = hanchan_repository.find_all(session)
            else:
                targets = hanchan_repository.find_by_ids(session, ids)

            return targets

    def delete(self, ids: List[int]) -> List[Hanchan]:
        with session_scope() as session:
            targets = hanchan_repository.find_by_ids(session, ids)
            for target in targets:
                session.delete(target)

            print(f'delete: id={ids}')
            return targets

    def run_calculate(
        self,
        points: Dict[str, int],
        ranking_prize: List[int],
        tobi_prize: int = 0,
        rounding_method: str = None,
        tobashita_player_id: str = None,
    ) -> Dict[str, int]:
        # 準備
        sorted_points = sorted(
            points.items(), key=lambda x: x[1], reverse=True)
        # TODO:ソートしない（高順位が高得点前提にしない）
        sorted_prize = sorted(
            ranking_prize,
            reverse=True,
        )

        # 素点計算
        result = {}
        tobasare_players = []
        isTobi = not(tobashita_player_id is None or
                     tobashita_player_id == '')

        # 計算方法に合わせて点数調整用の adjuster(丸めの境界値の調整) と padding(端数調整) を設定
        padding = 0
        adjuster = 100000
        if rounding_method == '五捨六入':
            padding = 400
        elif rounding_method == '四捨五入':
            padding = 500
        elif rounding_method == '切り捨て':
            padding = 0
        elif rounding_method == '切り上げ':
            padding = 900
        else:
            adjuster = -30000

        # 2~4位
        for t in sorted_points[1:]:
            player = t[0]
            point = t[1]
            # 点数がマイナスの場合、飛ばされたプレイヤーリストに追加する
            if (point < 0):
                tobasare_players.append(player)

            # 3万点切り上げ切り捨ての場合、一時的に30000点を引き、int の丸めを利用する
            # ex. 切り上げ: int(-10100/1000) -> -10000, 切り捨て: int(10100/1000) -> 10000
            # その他の場合、マイナス点の場合の丸め方をプラスの丸め方に合わせるため、一時的に100000足す
            result[player] = int((point + adjuster + padding) / 1000) - 30 - (adjuster // 1000)

        # 1位(他プレイヤーの点数合計×(-1))
        result[sorted_points[0][0]] = -1 * sum(result.values())

        # 順位点、飛び賞加算
        for i, t in enumerate(sorted_points):
            # 順位点
            result[t[0]] += sorted_prize[i]
            # 飛び賞
            if isTobi:
                if t[0] in tobasare_players:
                    result[t[0]] -= tobi_prize
                if t[0] == tobashita_player_id:
                    result[t[0]] += tobi_prize * len(tobasare_players)
                else:
                    print(
                        'tobashita_player_id is not matching'
                    )
        return result
