from application_service import (
    reply_service,
    request_info_service,
)
from domain_model.entities.group import GroupMode
from domain_service import (
    group_service,
    hanchan_service,
    match_service,
)


class ExitUseCase:

    def execute(self) -> None:
        line_group_id = request_info_service.req_line_group_id
        group = group_service.find_one_by_line_group_id(line_group_id=line_group_id)
        if group is None:
            reply_service.add_message(
                "グループが登録されていません。招待し直してください。",
            )
            return

        # simモード中断時はsim専用サンドボックス、それ以外は実系列の
        # current_input_match_idを対象にクリーンアップする(両者は独立している)。
        was_sim = group.mode == GroupMode.sim.value
        was_badai = group.mode == GroupMode.badai_input.value

        group.mode = GroupMode.wait.value
        if was_badai:
            # 場代入力は精算済みの対戦を指しているだけで、破棄する半荘はない
            group.current_input_match_id = None
        group_service.update(group)

        reply_service.add_message(
            "始める時は「_start」と入力してください。")

        if was_badai:
            return

        target_match_id = group.sim_match_id if was_sim else group.current_input_match_id
        target_match = match_service.find_one_by_id(target_match_id)

        if target_match is None:
            return

        # Active な半荘がある場合は削除
        active_hanchan = hanchan_service.find_one_by_id(target_match.active_hanchan_id)
        target_match.active_hanchan_id = None
        match_service.update(target_match)

        if active_hanchan is None:
            return

        active_hanchan.is_deleted = True
        hanchan_service.update(active_hanchan)
