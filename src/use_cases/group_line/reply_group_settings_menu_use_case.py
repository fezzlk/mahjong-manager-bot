from application_service import (
    reply_service,
    request_info_service,
)
from domain_model.entities.group_setting import ROUNDING_METHOD_LIST
from domain_service import (
    group_setting_service,
    guest_service,
)


class ReplyGroupSettingsMenuUseCase:
    def execute(self, body) -> None:
        line_group_id = request_info_service.req_line_group_id

        if body == "ゲスト":
            reply_service.add_guest_menu(guest_service.list_by_group(line_group_id))
            return
        if body == "ゲスト削除":
            reply_service.add_guest_remove_quick_reply(
                guest_service.list_by_group(line_group_id),
            )
            return

        settings = group_setting_service.find_or_create(line_group_id)

        if body == "":
            r = settings.ranking_prize

            s = ["[設定]"]
            s.append(f"{settings.num_of_players}人麻雀")
            s.append(f"レート: 点{settings.rate}")
            s.append(f"順位点: 1着{r[0]}/2着{r[1]}/3着{r[2]}/4着{r[3]}")
            s.append(f"飛び賞: {settings.tobi_prize}点")
            chip_display = "なし" if settings.chip_rate == 0 else "あり(1枚=1点)"
            s.append(f"チップ: {chip_display}")
            s.append(f"計算方法: {ROUNDING_METHOD_LIST[settings.rounding_method]}")
            s.append(f"単位: {settings.unit}")
            reply_service.add_message("\n".join(s))
        reply_service.add_settings_menu(body)
