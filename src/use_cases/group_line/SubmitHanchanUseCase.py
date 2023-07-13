from DomainService import (
    user_service,
    hanchan_service,
    group_service,
    group_setting_service,
)
from ApplicationService import (
    request_info_service,
    reply_service,
    message_service,
    calculate_service,
)
from DomainModel.entities.Group import GroupMode
from DomainModel.entities.UserMatch import UserMatch
from DomainModel.entities.UserGroup import UserGroup
from repositories import (
    hanchan_repository,
    user_match_repository,
    user_group_repository,
)

from line_models.Profile import Profile


class SubmitHanchanUseCase:

    def execute(
        self,
        tobashita_player_id: str = None,
    ) -> None:
        # 得点計算の準備および結果の格納
        line_group_id = request_info_service.req_line_group_id

        # 現在 active な result (current)のポイントを計算対象にする
        current = hanchan_service.get_current(line_group_id)
        if current is None:
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
        if any(x < 0 for x in points.values()) and tobashita_player_id is None:
            reply_service.add_tobi_menu([
                {'_id': p_id, 'name': user_service.get_name_by_line_user_id(p_id), }
                for p_id in points.keys() if points[p_id] > 0
            ])
            return

        # config の取得
        setting = group_setting_service.find_or_create(line_group_id)

        # 計算の実行
        calculate_result = calculate_service.run(
            points=points,
            ranking_prize=setting.ranking_prize,
            tobi_prize=setting.tobi_prize,
            rounding_method=setting.rounding_method,
            tobashita_player_id=tobashita_player_id,
        )

        # その半荘の結果を更新
        hanchan_repository.update(
            query={'line_group_id': line_group_id},
            new_values={'converted_scores': calculate_result}
        )

        # user_match, user_group の作成
        user_ids_in_hanchan = []
        user_groups = user_group_repository.find({'line_group_id': line_group_id})
        line_user_ids_in_group = [ug.line_user_id for ug in user_groups]

        for user_line_id in calculate_result:
            if user_line_id not in line_user_ids_in_group:
                user_group_repository.create(
                    UserGroup(
                        line_group_id=line_group_id,
                        line_user_id=user_line_id,
                    )
                )
            profile = Profile(display_name='', user_id=user_line_id)
            user = user_service.find_or_create_by_profile(profile)
            if user is not None:
                user_ids_in_hanchan.append(user._id)

        user_matches = user_match_repository.find(
            {'match_id': current.match_id}
        )
        linked_user_ids = [um.user_id for um in user_matches]
        target_user_ids = set(user_ids_in_hanchan) - set(linked_user_ids)
        for user_id in target_user_ids:
            user_match = UserMatch(
                user_id=user_id,
                match_id=current.match_id,
            )
            user_match_repository.create(user_match)

        # # 総合結果に半荘結果を追加
        # current_match = match_service.add_hanchan_id(
        #     line_group_id, updated_hanchan._id)

        # 結果の表示
        hanchans = hanchan_repository.find({'match_id': current.match_id})

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
            calculate_result.items(),
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
