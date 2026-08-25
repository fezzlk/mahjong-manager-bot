from application_service import (
    reply_service,
    request_info_service,
)
from domain_model.entities.group_setting import (
    RETURN_POINTS_MARGIN,
    ROUNDING_METHOD_LIST,
)
from domain_service import group_service, group_setting_service


class UpdateGroupSettingsUseCase:
    def execute(self, key: str, value: str):
        """リクエスト元のルームの設定更新"""
        target_id = request_info_service.req_line_group_id

        def _parse_int(v: str) -> int:
            try:
                return int(v)
            except (ValueError, TypeError):
                raise ValueError(f"[{v}] は整数として解釈できません") from None

        try:
            if key == "レート":
                column = "rate"
                db_value = _parse_int(value)
                if db_value not in [0, 1, 2, 3, 4, 5, 10]:
                    reply_service.add_message(f"[{key}]を[{value}]に変更できません")
                    return
                display_value = "点" + value
            elif key == "順位点":
                current_settings = group_setting_service.find_or_create(target_id)
                num_of_players = current_settings.num_of_players
                column = "ranking_prize_3" if num_of_players == 3 else "ranking_prize_4"
                db_value = list(map(int, value.split(",")))
                if len(db_value) != num_of_players:
                    reply_service.add_message(
                        f"[{key}]を[{value}]に変更できません（現在{num_of_players}人麻雀設定のため{num_of_players}個の値が必要です）",
                    )
                    return
                display_value = "/".join(
                    f"{i + 1}着 {v}" for i, v in enumerate(db_value)
                )
            elif key == "持ち点":
                current_settings = group_setting_service.find_or_create(target_id)
                num_of_players = current_settings.num_of_players
                column = "starting_points_3" if num_of_players == 3 else "starting_points_4"
                db_value = _parse_int(value)
                if db_value <= 0:
                    reply_service.add_message(f"[{key}]を[{value}]に変更できません")
                    return
                display_value = f"{db_value}点（返し点 {db_value + RETURN_POINTS_MARGIN}点）"
            elif key == "チップ":
                column = "chip_rate"
                db_value = _parse_int(value)
                if db_value not in [0, 1]:
                    reply_service.add_message(f"[{key}]を[{value}]に変更できません")
                    return
                display_value = "なし" if db_value == 0 else "あり(1枚=1点)"
            elif key == "飛び賞":
                column = "tobi_prize"
                db_value = _parse_int(value)
                if db_value not in [0, 10, 20, 30]:
                    reply_service.add_message(f"[{key}]を[{value}]に変更できません")
                    return
                display_value = value
            elif key == "人数":
                column = "num_of_players"
                db_value = _parse_int(value)
                if db_value not in [3, 4]:
                    reply_service.add_message(f"[{key}]を[{value}]に変更できません")
                    return
                display_value = value + "人"
            elif key == "端数計算方法":
                column = "rounding_method"
                db_value = _parse_int(value)
                if db_value not in list(range(len(ROUNDING_METHOD_LIST))):
                    reply_service.add_message(f"[{key}]を[{value}]に変更できません")
                    return
                display_value = ROUNDING_METHOD_LIST[db_value]
            elif key == "単位":
                column = "unit"
                db_value = value.strip()
                if not db_value or len(db_value) > 10:
                    reply_service.add_message(f"[{key}]を[{value}]に変更できません（10文字以内）")
                    return
                display_value = db_value
            else:
                reply_service.add_message(
                    f"項目[{key}]は未知の項目のため、[{key}]を[{value}]に変更できません",
                )
                return
        except ValueError as e:
            reply_service.add_message(str(e))
            return

        group_service.update_settings(target_id, column, db_value)
        reply_service.add_message(f"[{key}]を[{display_value}]に変更しました。")
