from typing import Dict

from ApplicationService import (
    calculate_service,
    message_service,
    reply_service,
    request_info_service,
)
from DomainModel.entities.Group import GroupMode
from DomainModel.entities.UserGroup import UserGroup
from DomainModel.entities.UserHanchan import UserHanchan
from DomainModel.entities.UserMatch import UserMatch
from DomainService import (
    group_service,
    group_setting_service,
    hanchan_service,
    match_service,
    user_group_service,
    user_service,
)
from line_models.Profile import Profile
from repositories import (
    user_group_repository,
    user_hanchan_repository,
    user_match_repository,
)


class SubmitHanchanUseCase:

    def execute(
        self,
        tobashita_player_id: str = None,
    ) -> None:
        # 得点計算の準備および結果の格納
        line_group_id = request_info_service.req_line_group_id

        # active 半荘を取得
        group = group_service.find_one_by_line_group_id(line_group_id=line_group_id)
        if group is None:
            reply_service.add_message(
                "グループが登録されていません。招待し直してください。",
            )
            return
        active_match = match_service.find_one_by_id(group.active_match_id)
        if active_match is None:
            reply_service.add_message(
                "計算対象の試合が見つかりません。",
            )
            return
        active_hanchan = hanchan_service.find_one_by_id(active_match.active_hanchan_id)
        if active_hanchan is None:
            reply_service.add_message(
                "計算対象の半荘が見つかりません。",
            )
            return
        points = active_hanchan.raw_scores

        # 計算可能な points かチェック
        # 4人分の点数がない、または超えている場合中断する
        if len(points) != 4:
            reply_service.add_message(
                "四人分の点数を入力してください。点数を取り消したい場合は @[ユーザー名] と送ってください。",
            )
            return

        # 点数合計が 100000~100099 の範囲になければ中断する
        if int(sum(points.values()) / 100) != 1000:
            reply_service.add_message(
                f"点数の合計が{sum(points.values())}点です。合計100000点+αになるように修正してください。",
            )
            return

        # 点数が全て異なっているかチェックし、同点があったら中断する
        if len(set(points.values())) != 4:
            reply_service.add_message(
                "同点のユーザーがいます。上家が1点でも高くなるよう修正してください。",
            )
            return

        # 飛び賞が発生した場合、飛び賞を受け取るプレイヤーを指定するメニューを返す
        if any(x < 0 for x in points.values()) and tobashita_player_id is None:
            reply_service.add_tobi_menu([
                {"_id": p_id, "name": user_service.get_name_by_line_user_id(p_id) or "友達未登録" }
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
        active_hanchan.converted_scores = calculate_result
        hanchan_service.update(active_hanchan)

        # user_match, user_group の作成
        user_ids_in_hanchan = []
        user_groups = user_group_service.find_all_by_line_group_id(line_group_id)
        line_user_ids_in_group = [ug.line_user_id for ug in user_groups]

        for user_line_id in calculate_result:
            if user_line_id not in line_user_ids_in_group:
                user_group_repository.create(
                    UserGroup(
                        line_group_id=line_group_id,
                        line_user_id=user_line_id,
                    ),
                )
            profile = Profile(display_name="", user_id=user_line_id)
            user = user_service.find_or_create_by_profile(profile)
            if user is not None:
                user_ids_in_hanchan.append(user._id)

        user_matches = user_match_repository.find(
            {"match_id": active_hanchan.match_id},
        )
        linked_user_ids = [um.user_id for um in user_matches]
        target_user_ids = set(user_ids_in_hanchan) - set(linked_user_ids)
        for user_id in target_user_ids:
            user_match = UserMatch(
                user_id=user_id,
                match_id=active_hanchan.match_id,
            )
            user_match_repository.create(user_match)

        # 半荘合計の更新
        hanchans = hanchan_service.find_all_archived_by_match_id(active_hanchan.match_id)

        sum_scores: Dict[str, int] = {}
        for h in hanchans:
            for line_user_id, converted_score in h.converted_scores.items():
                if line_user_id not in sum_scores:
                    sum_scores[line_user_id] = 0
                sum_scores[line_user_id] += converted_score

        # 一半荘の結果をアーカイブ
        active_match.active_hanchan_id = None
        active_match.sum_scores = sum_scores
        match_service.update(active_match)

        # UserHanchan の作成
        sorted_points: list[tuple[str, int]] = sorted(
            active_hanchan.raw_scores.items(), key=lambda x: x[1], reverse=True)
        for i in range(len(sorted_points)):
            line_id, point = sorted_points[i]
            user_hanchan_repository.create(UserHanchan(
                line_user_id=line_id,
                hanchan_id=active_hanchan._id,
                point=point,
                rank=i+1,
            ))

        # 結果の表示
        reply_service.add_message("一半荘お疲れ様でした。結果を表示します。")
        reply_service.add_message(
            message_service.create_show_converted_scores(
                calculate_result,
                sum_scores=sum_scores,
            ),
        )
        reply_service.add_message(
            message_service.get_finish_hanchan_message(),
        )

        # ルームを待機モードにする
        group_service.chmod(line_group_id, GroupMode.wait)

        reply_service.add_start_menu()

        return
