from db_models import UserMatchModel
from DomainService import (
    user_service,
    hanchan_service,
    config_service,
    match_service,
    group_service,
)
from ApplicationService import (
    request_info_service,
    reply_service,
    message_service,
)
from DomainModel.entities.Group import GroupMode
from repositories import (
    session_scope,
    hanchan_repository,
    user_match_repository,
)

from line_models.Profile import Profile


class CalculateUseCase:

    def execute(
        self,
        tobashita_player_id: str = None,
    ) -> None:
        # 得点計算の準備および結果の格納
        line_group_id = request_info_service.req_line_group_id

        # 現在 active な result (current)のポイントを計算対象にする
        with session_scope() as session:
            current = hanchan_repository.find_one_by_line_group_id_and_status(
                session,
                line_group_id,
                1
            )
            if current is None:
                print(
                    'current points is not found.'
                )
                reply_service.add_message(
                    '計算対象の半荘が見つかりません。'
                )
                return
            points = current.raw_scores

            # 計算可能な points かチェック
            # 4人分の点数がない、または超えている場合中断する
            if len(points) != 4:
                reply_service.add_message(
                    '四人分の点数を入力してください。点数を取り消したい場合は @[ユーザー名] と送ってください。'
                )
                return

            # 点数合計が 100000~100099 の範囲になければ中断する
            if int(sum(points.values()) / 100) != 1000:
                reply_service.add_message(
                    f'点数の合計が{sum(points.values())}点です。合計100000点+αになるように修正してください。'
                )
                return

            # 点数が全て異なっているかチェックし、同点があったら中断する
            if len(set(points.values())) != 4:
                reply_service.add_message(
                    '同点のユーザーがいます。上家が1点でも高くなるよう修正してください。'
                )
                return

            # 飛び賞が発生した場合、飛び賞を受け取るプレイヤーを指定するメニューを返す
            if any(x < 0 for x in points.values()
                   ) and tobashita_player_id is None:
                reply_service.add_tobi_menu([
                    {'id': p_id, 'name': user_service.get_name_by_line_user_id(p_id), }
                    for p_id in points.keys() if points[p_id] > 0
                ])
                return

            # config の取得
            ranking_prize = config_service.get_value_by_key(
                line_group_id, '順位点')
            rounding_method = config_service.get_value_by_key(
                line_group_id, '端数計算方法')
            tobi_prize = config_service.get_value_by_key(
                line_group_id, '飛び賞')

            # 計算の実行
            calculate_result = hanchan_service.run_calculate(
                points=points,
                ranking_prize=[
                    int(s) for s in ranking_prize.split(',')
                ],
                tobi_prize=int(tobi_prize),
                rounding_method=rounding_method,
                tobashita_player_id=tobashita_player_id,
            )

            # その半荘の結果を更新
            updated_hanchan = hanchan_service.update_current_converted_score(
                line_group_id, calculate_result)

            # user_match の作成
            user_ids_in_hanchan = []
            for user_line_id in updated_hanchan.converted_scores:
                profile = Profile(display_name='', user_id=user_line_id)
                user = user_service.find_or_create_by_profile(profile)
                if user is not None:
                    user_ids_in_hanchan.append(user._id)

            user_matches = session\
                .query(UserMatchModel)\
                .filter(
                    UserMatchModel.match_id == updated_hanchan.match_id,
                )\
                .all()
            linked_user_ids = [um.user_id for um in user_matches]
            target_user_ids = set(user_ids_in_hanchan) - set(linked_user_ids)
            with session_scope() as session:
                for user_id in target_user_ids:
                    user_match = UserMatchModel(
                        user_id=user_id,
                        match_id=updated_hanchan.match_id,
                    )
                    user_match_repository.create(session, user_match)

            # 総合結果に半荘結果を追加
            current_match = match_service.add_hanchan_id(
                line_group_id, updated_hanchan._id)

            # 結果の表示
            converted_scores = updated_hanchan.converted_scores
            with session_scope() as session:
                hanchans = hanchan_repository.find_by_ids(
                    session, current_match.hanchan_ids)

            sum_hanchans = {}
            for r in hanchans:
                converted_scores = r.converted_scores
                for line_user_id, converted_score in converted_scores.items():
                    if line_user_id not in sum_hanchans.keys():
                        sum_hanchans[line_user_id] = 0
                    sum_hanchans[line_user_id] += converted_score

            reply_service.add_message(
                '一半荘お疲れ様でした。結果を表示します。'
            )

            score_text_list = []
            for r in sorted(
                converted_scores.items(),
                key=lambda x: x[1],
                reverse=True
            ):
                name = user_service.get_name_by_line_user_id(r[0])
                score = ("+" if r[1] > 0 else "") + str(r[1])
                sum_score = (
                    "+" if sum_hanchans[r[0]] > 0 else "") + str(sum_hanchans[r[0]])
                score_text_list.append(
                    f'{name}: {score} ({sum_score})'
                )
            reply_service.add_message(
                '\n'.join(score_text_list)
            )

            reply_service.add_message(
                message_service.get_finish_hanchan_message()
            )

            # 一半荘の結果をアーカイブ
            hanchan_service.archive(line_group_id)

            # ルームを待機モードにする
            group_service.chmod(line_group_id, GroupMode.wait)

            reply_service.add_message(
                '始める時は「_start」と入力してください。'
            )

            return
