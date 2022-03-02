from typing import Dict, List, Optional, Tuple

from repositories import session_scope, hanchan_repository
from DomainModel.entities.Hanchan import Hanchan
from db_models import UserMatchModel
from .interfaces.IHanchanService import IHanchanService

STATUS_LIST = ['disabled', 'active', 'archived']


class HanchanService(IHanchanService):

    def disabled_by_id(
        self,
        line_group_id: str,
        hanchan_id: int,
    ) -> Hanchan:
        """disabled target hanchan"""
        with session_scope() as session:
            target = hanchan_repository.find_one_by_id_and_line_group_id(
                session=session,
                hanchan_id=hanchan_id,
                line_group_id=line_group_id,
            )

            if target is None:
                raise ValueError('Not found hanchan')

            updated_hanchan = hanchan_repository.update_one_status_by_id(
                session,
                hanchan_id=target._id,
                status=0,
            )

            print(
                f'disabled: id={updated_hanchan._id}'
            )

            return updated_hanchan

    def add_or_drop_raw_score(
        self,
        line_group_id: str,
        line_user_id: str,
        raw_score: Optional[int],
    ) -> Hanchan:
        with session_scope() as session:
            if line_user_id is None:
                raise ValueError('line_user_id is required')

            target = hanchan_repository.find_one_by_line_group_id_and_status(
                session=session,
                line_group_id=line_group_id,
                status=1,
            )

            if target is None:
                raise ValueError('Not found hanchan')

            raw_scores = target.raw_scores

            if raw_score is None:
                raw_scores.pop(line_user_id, None)
            else:
                raw_scores[line_user_id] = raw_score

            updated_hanchan = hanchan_repository.update_one_raw_scores_by_id(
                session=session,
                hanchan_id=target._id,
                raw_scores=raw_scores,
            )

            return updated_hanchan

    def update_converted_score(
        self,
        line_group_id: str,
        converted_scores: Dict[str, int],
    ) -> Hanchan:
        with session_scope() as session:
            target = hanchan_repository.find_one_by_line_group_id_and_status(
                session=session,
                line_group_id=line_group_id,
                status=1,
            )

            if target is None:
                return None

            updated_hanchan = hanchan_repository.update_one_converted_scores_by_id(
                session=session, hanchan_id=target._id, converted_scores=converted_scores)

            print(
                f'update hanchan: id={updated_hanchan._id}'
            )
            from line_models.Profile import Profile
            from DomainService.UserService import UserService
            service = UserService()

            user_ids_in_hanchan = []
            for user_line_id in updated_hanchan.converted_scores:
                profile = Profile(display_name='', user_id=user_line_id)
                user = service.find_or_create_by_profile(profile)
                if user is not None:
                    user_ids_in_hanchan.append(user._id)

            # user_match の作成
            user_matches = session\
                .query(UserMatchModel)\
                .filter(
                    UserMatchModel.match_id == updated_hanchan.match_id,
                )\
                .all()
            linked_user_ids = [um.user_id for um in user_matches]
            target_user_ids = set(user_ids_in_hanchan) - set(linked_user_ids)
            for user_id in target_user_ids:
                user_match = UserMatchModel(
                    user_id=user_id,
                    match_id=updated_hanchan.match_id,
                )
                session.add(user_match)
        return updated_hanchan

    def update_status_active_hanchan(
        self,
        line_group_id: str,
        status: int,
    ) -> Hanchan:
        with session_scope() as session:
            target = hanchan_repository.find_one_by_line_group_id_and_status(
                session=session,
                line_group_id=line_group_id,
                status=1,
            )

            if target is None:
                raise ValueError('Not found hanchan')

            updated_hanchan = hanchan_repository.update_one_status_by_id(
                session=session,
                hanchan_id=target._id,
                status=status,
            )

            print(
                f'{STATUS_LIST[updated_hanchan.status]} hanchan: id={updated_hanchan._id}'
            )

            return updated_hanchan

    def archive(self, line_group_id: str) -> Hanchan:
        return self.update_status_active_hanchan(line_group_id, 2)

    def disable(self, line_group_id: str) -> Hanchan:
        return self.update_status_active_hanchan(line_group_id, 0)

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
            result[player] = int(
                (point + adjuster + padding) / 1000) - 30 - (adjuster // 1000)

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

    def get_point_and_name_from_text(
        self,
        text: str,
    ) -> Tuple[str, str]:
        s = text.split()
        if len(s) >= 2:
            # ユーザー名に空白がある場合を考慮し、最後の要素をポイント、そのほかをユーザー名として判断する
            return s[-1], ' '.join(s[:-1])
        # fixme: ユーザー名「taro 100」の点数を削除しようとした場合に上の条件にひっかかる
        # 名前のみによるメッセージでの削除機能自体をやめるか
        elif len(s) == 1:
            return 'delete', s[0]
