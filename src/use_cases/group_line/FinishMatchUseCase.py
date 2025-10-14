from typing import Dict

from ApplicationService import (
    message_service,
    reply_service,
    request_info_service,
)
from DomainModel.entities.Group import GroupMode
from DomainService import (
    group_service,
    group_setting_service,
    hanchan_service,
    match_service,
)
from use_cases.group_line.CreateMatchDetailGraphUseCase import (
    CreateMatchDetailGraphUseCase,
)


class FinishMatchUseCase:
    def execute(self) -> None:
        line_group_id = request_info_service.req_line_group_id
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

        hanchans = hanchan_service.find_all_archived_by_match_id(active_match._id)

        if len(hanchans) == 0:
            reply_service.add_message("まだ対戦結果がありません。")
            return

        settings = group_setting_service.find_or_create(
            request_info_service.req_line_group_id
        )
        chip_rate = settings.chip_rate
        if (
            chip_rate != 0
            and group_service.get_mode(line_group_id) != GroupMode.chip_ok.value
        ):
            group.mode = GroupMode.chip_input.value
            group_service.update(group)
            reply_service.add_message(
                "チップの増減数を入力してください。完了したら「_chip_ok」と入力してください。"
            )
            return

        # 精算
        rate = settings.rate * 10
        sum_scores = active_match.sum_scores
        chip_scores = active_match.chip_scores

        chip_prices: Dict[str, int] = {}
        sum_prices: Dict[str, int] = {}
        sum_prices_with_chip: Dict[str, int] = {}
        for line_user_id, converted_score in sum_scores.items():
            if chip_scores.get(line_user_id) is None:
                chip_score = 0
                chip_scores[line_user_id] = 0
            else:
                chip_score = chip_scores.get(line_user_id)

            chip_price = chip_score * chip_rate
            chip_prices[line_user_id] = chip_price

            price = converted_score * rate
            sum_prices[line_user_id] = price

            sum_prices_with_chip[line_user_id] = price + chip_price

        # 試合のアーカイブ
        active_match.chip_prices = chip_prices
        active_match.sum_prices = sum_prices
        active_match.sum_prices_with_chip = sum_prices_with_chip
        match_service.update(active_match)
        group.mode = GroupMode.wait.value
        group.active_match_id = None
        group_service.update(group)

        # 応答メッセージ作成
        reply_service.add_message(
            "【対戦結果】 \n"
            + message_service.create_show_match_result(match=active_match),
        )

        reply_service.add_image(
            CreateMatchDetailGraphUseCase().execute(active_match._id)
        )
