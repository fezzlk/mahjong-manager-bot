import logging
from typing import Dict

from application_service import (
    message_service,
    reply_service,
    request_info_service,
)
from domain_model.entities.group import GroupMode
from domain_model.entities.match import MatchStatus
from domain_service import (
    group_service,
    group_setting_service,
    hanchan_service,
    match_service,
)
from use_cases.group_line.create_match_detail_graph_use_case import (
    CreateMatchDetailGraphUseCase,
)

logger = logging.getLogger(__name__)


class FinishMatchUseCase:
    def execute(self) -> None:
        line_group_id = request_info_service.req_line_group_id
        group = group_service.find_one_by_line_group_id(line_group_id=line_group_id)
        if group is None:
            reply_service.add_message(
                "グループが登録されていません。招待し直してください。",
            )
            return

        active_match = match_service.find_one_by_id(group.current_input_match_id)
        if active_match is None:
            reply_service.add_message(
                "計算対象の試合が見つかりません。",
            )
            return

        hanchans = hanchan_service.find_all_archived_by_match_id(active_match._id)

        if len(hanchans) == 0:
            reply_service.add_message("まだ対戦結果がありません。")
            return

        # 対戦作成時のレート等を使う(グループの現在の設定ではなく)。
        # 異なるレートの対戦が同時に進行していても、それぞれ自分自身の設定で
        # 精算されるようにするため(FEZ-66 Phase D)。settings未設定(旧データ)は
        # グループの現在の設定にフォールバックする。
        settings = active_match.settings or group_setting_service.find_or_create(
            request_info_service.req_line_group_id,
        )
        chip_rate = settings.chip_rate
        if (
            chip_rate != 0
            and group_service.get_mode(line_group_id) != GroupMode.chip_ok.value
        ):
            group.mode = GroupMode.chip_input.value
            group_service.update(group)
            reply_service.add_chip_complete_button()
            return

        # 精算
        rate = settings.rate * 10
        sum_scores = active_match.sum_scores
        chip_scores = active_match.chip_scores

        sum_prices: Dict[str, int] = {}
        sum_prices_with_chip: Dict[str, int] = {}
        for line_user_id, converted_score in sum_scores.items():
            # チップ設定が有効な場合のみチップを加算
            chip_score = chip_scores.get(line_user_id, 0) if chip_rate != 0 else 0
            # チップを累計ポイントに加算してからレートを掛ける
            total_score = converted_score + chip_score
            price = total_score * rate
            sum_prices[line_user_id] = converted_score * rate
            sum_prices_with_chip[line_user_id] = price

        # 試合のアーカイブ
        active_match.chip_prices = {}
        active_match.sum_prices = sum_prices
        active_match.sum_prices_with_chip = sum_prices_with_chip
        active_match.status = MatchStatus.settled.value
        match_service.update(active_match)
        group.mode = GroupMode.wait.value
        group.current_input_match_id = None
        group_service.update(group)
        logger.info("finish match: group=%s match=%s hanchans=%d", line_group_id, active_match._id, len(hanchans))

        # 応答メッセージ作成
        reply_service.add_message(
            "【対戦結果】 \n"
            + message_service.create_show_match_result(match=active_match, unit=settings.unit),
        )

        image_url = CreateMatchDetailGraphUseCase().execute(active_match._id)
        if image_url is not None:
            reply_service.add_image(image_url)
