from application_service import (
    calculate_service,
    reply_service,
    request_info_service,
)
from domain_model.entities.group import GroupMode
from domain_service import (
    group_service,
    group_setting_service,
    hanchan_service,
    match_service,
    user_service,
)
from use_cases.utility.input_point_use_case import InputPointUseCase


class SimulateScoreUseCase:
    """sim モードで点数を収集し、4人揃ったらシミュレーション結果を表示する。"""

    def execute(self, text: str) -> None:
        line_group_id = request_info_service.req_line_group_id

        # メッセージから対象ユーザと点数の取得
        target_line_user_id, point = InputPointUseCase().execute(text)
        if point is None and target_line_user_id is None:
            return

        # 現在入力中の半荘を取得し点数を追加
        group = group_service.find_one_by_line_group_id(line_group_id=line_group_id)
        if group is None:
            reply_service.add_message("グループが登録されていません。招待し直してください。")
            return
        active_match = match_service.find_one_by_id(group.active_match_id)
        if active_match is None or active_match.active_hanchan_id is None:
            return
        hanchan = hanchan_service.add_or_drop_raw_score(
            hanchan_id=active_match.active_hanchan_id,
            line_user_id=target_line_user_id,
            raw_score=point,
        )

        raw_scores = hanchan.raw_scores

        # 応答メッセージ作成
        if len(raw_scores) == 0:
            reply_service.add_message("点数を入力してください。")
            return

        res = [
            f'{user_service.get_name_by_line_user_id(line_user_id) or "友達未登録"}: {raw_score}'
            for line_user_id, raw_score in raw_scores.items()
        ]

        reply_service.add_message("\n".join(res))

        if len(raw_scores) == 4:
            self._calculate_and_show(line_group_id, raw_scores, hanchan._id, active_match)
        elif len(raw_scores) > 4:
            reply_service.add_message(
                "5人以上入力されています。@[ユーザー名] で不要な入力を消してください。",
            )

    def _calculate_and_show(self, line_group_id, raw_scores, hanchan_id, active_match):
        """4人分の点数でシミュレーション計算し、結果表示後にクリーンアップする。"""
        points = raw_scores

        # 合計チェック
        total = sum(points.values())
        if int(total / 100) != 1000:
            reply_service.add_message(
                f"点数の合計が{total}点です。合計100000点+αになるように修正してください。",
            )
            return

        # 同点チェック
        if len(set(points.values())) != 4:
            reply_service.add_message(
                "同点のユーザーがいます。上家が1点でも高くなるよう修正してください。",
            )
            return

        # グループ設定を取得して計算
        setting = group_setting_service.find_or_create(line_group_id)

        # トビ（マイナス点）がある場合、1位を tobashita_player_id とする
        tobashita_player_id = None
        if setting.tobi_prize and any(v < 0 for v in points.values()):
            sorted_by_score = sorted(points.items(), key=lambda x: x[1], reverse=True)
            tobashita_player_id = sorted_by_score[0][0]

        result = calculate_service.run(
            points=points,
            ranking_prize=setting.ranking_prize,
            tobi_prize=setting.tobi_prize,
            rounding_method=setting.rounding_method,
            tobashita_player_id=tobashita_player_id,
        )

        # 結果を順位順に表示
        sorted_result = sorted(result.items(), key=lambda x: x[1], reverse=True)
        lines = []
        for rank, (line_user_id, score) in enumerate(sorted_result, 1):
            name = user_service.get_name_by_line_user_id(line_user_id) or "友達未登録"
            raw = points[line_user_id]
            sign = "+" if score >= 0 else ""
            lines.append(f"{rank}位 {name}({raw}点): {sign}{score}")

        header = "[シミュレーション結果]"
        if tobashita_player_id is not None:
            tobi_name = user_service.get_name_by_line_user_id(tobashita_player_id) or "友達未登録"
            header += f"\n※飛び賞: {tobi_name}(1位)"

        reply_service.add_message(
            header + "\n" + "\n".join(lines),
        )

        # クリーンアップ: 半荘を無効化してモードを戻す
        hanchan = hanchan_service.find_one_by_id(hanchan_id)
        if hanchan is not None:
            hanchan.is_deleted = True
            hanchan_service.update(hanchan)
        active_match.active_hanchan_id = None
        match_service.update(active_match)
        group = group_service.find_one_by_line_group_id(line_group_id)
        group.mode = GroupMode.wait.value
        group_service.update(group)
