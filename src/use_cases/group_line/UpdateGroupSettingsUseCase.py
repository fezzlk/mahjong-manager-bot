from ApplicationService import (
    reply_service,
    request_info_service,
)
from DomainModel.entities.GroupSetting import ROUNDING_METHOD_LIST
from repositories import group_setting_repository


class UpdateGroupSettingsUseCase:
    def execute(self, key: str, value: str):
        """リクエスト元のルームの設定更新"""
        target_id = request_info_service.req_line_group_id

        if key == "レート":
            column = "rate"
            db_value = int(value)
            if db_value not in [0, 1, 2, 3, 4, 5, 10]:
                reply_service.add_message(f"[{key}]を[{value}]に変更できません")
                return
            display_value = "点" + value
        elif key == "順位点":
            column = "ranking_prize"
            db_value = list(map(int, value.split(",")))
            if len(db_value) != 4:
                reply_service.add_message(f"[{key}]を[{value}]に変更できません")
                return
            display_value = f"1着 {db_value[0]}/2着 {db_value[1]}/3着 {db_value[2]}/4着 {db_value[3]}"
        elif key == "チップ":
            column = "chip_rate"
            db_value = int(value)
            if db_value not in [0, 10, 30, 50, 100, 500]:
                reply_service.add_message(f"[{key}]を[{value}]に変更できません")
                return
            display_value = f"1枚{value}円"
        elif key == "飛び賞":
            column = "tobi_prize"
            db_value = int(value)
            if db_value not in [0, 10, 20, 30]:
                reply_service.add_message(f"[{key}]を[{value}]に変更できません")
                return
            display_value = value
        elif key == "人数":
            column = "num_of_players"
            db_value = int(value)
            if db_value not in [3, 4]:
                reply_service.add_message(f"[{key}]を[{value}]に変更できません")
                return
            display_value = value + "人"
        elif key == "端数計算方法":
            column = "rounding_method"
            db_value = int(value)
            if db_value not in list(range(len(ROUNDING_METHOD_LIST))):
                reply_service.add_message(f"[{key}]を[{value}]に変更できません")
                return
            display_value = ROUNDING_METHOD_LIST[db_value]
        else:
            reply_service.add_message(
                f"項目[{key}]は未知の項目のため、[{key}]を[{value}]に変更できません",
            )
            return

        group_setting_repository.update(
            {"line_group_id": target_id},
            {column: db_value},
        )
        reply_service.add_message(f"[{key}]を[{display_value}]に変更しました。")
