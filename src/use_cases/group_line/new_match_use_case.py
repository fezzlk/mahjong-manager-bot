from application_service import (
    reply_service,
    request_info_service,
)
from domain_model.entities.group import GroupMode
from domain_service import (
    group_service,
    match_service,
)
from use_cases.group_line.start_input_use_case import StartInputUseCase


class NewMatchUseCase:
    """_new_match: 新しい対戦(系列)を明示的に開始する(FEZ-66 Phase E)。

    グループの現在の設定をコピーした確認メッセージを提示し、確定後に
    新規Matchを作成して入力を開始する。既存のopen対戦がいくつあっても
    (0件でも複数件でも)常に新規対戦を1件追加する。
    """

    def execute(self) -> None:
        line_group_id = request_info_service.req_line_group_id
        group = group_service.find_one_by_line_group_id(line_group_id=line_group_id)
        if group is None:
            reply_service.add_message(
                "グループが登録されていません。招待し直してください。",
            )
            return
        if group.mode == GroupMode.input.value:
            reply_service.add_message("すでに入力モードです。")
            return

        settings = group_service.get_settings_or_create(line_group_id)
        reply_service.add_new_match_confirm_menu(settings)

    def confirm(self) -> None:
        """_new_match_confirm: 新規対戦の作成を確定する。"""
        line_group_id = request_info_service.req_line_group_id
        group = group_service.find_one_by_line_group_id(line_group_id=line_group_id)
        if group is None:
            reply_service.add_message(
                "グループが登録されていません。招待し直してください。",
            )
            return
        if group.mode == GroupMode.input.value:
            reply_service.add_message("すでに入力モードです。")
            return

        new_match = match_service.create_with_line_group_id(
            line_group_id,
            settings=group_service.get_settings_or_create(line_group_id),
        )
        StartInputUseCase().enter_match(group, new_match)
