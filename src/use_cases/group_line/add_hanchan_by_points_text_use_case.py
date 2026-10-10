import re
from typing import List, Optional, Tuple

from application_service import reply_service, request_info_service
from domain_model.entities.group import GroupMode
from domain_model.entities.group_setting import EmbeddedGroupSettings
from domain_model.entities.hanchan import Hanchan
from domain_model.entities.match import MatchStatus
from domain_service import group_service, hanchan_service, match_service, user_service
from repositories import group_repository, hanchan_repository, match_repository
from use_cases.group_line.submit_hanchan_use_case import SubmitHanchanUseCase


class AddHanchanByPointsTextUseCase:
    """Import the raw-score reply emitted by AddPointByTextUseCase."""

    @staticmethod
    def parse_reply(text) -> Optional[List[Tuple[str, int]]]:
        if not isinstance(text, str):
            return None
        rows = text.strip().splitlines()
        # One name:number is too ambiguous to recognize as a pasted reply.
        if len(rows) < 2:
            return None
        parsed = []
        for row in rows:
            match = re.fullmatch(r"(.+): (-?(?:0|[1-9][0-9]{0,8}))", row)
            if match is None:
                return None
            parsed.append((match[1], int(match[2])))
        return parsed

    def execute(self, text) -> None:
        rows = self.parse_reply(text)
        if rows is None:
            reply_service.add_message(
                "Botが返信した全員分の素点一覧を、そのまま貼り付けてください。",
            )
            return
        line_group_id = request_info_service.req_line_group_id
        group = group_service.find_one_by_line_group_id(line_group_id)
        if group is None:
            reply_service.add_message(
                "グループが登録されていません。招待し直してください。",
            )
            return
        if group.mode not in (GroupMode.wait.value, GroupMode.input.value):
            reply_service.add_message(
                "現在の入力を終了してから、素点一覧を貼り付けてください。",
            )
            return
        target = match_service.find_one_by_id(group.current_input_match_id)
        if target is not None and (
            target.line_group_id != line_group_id
            or target.status != MatchStatus.open.value
        ):
            reply_service.add_message("入力開始から登録先の対戦を選び直してください。")
            return
        if target is None:
            matches = match_service.find_all_open_by_line_group_id(line_group_id)
            if len(matches) > 1:
                reply_service.add_message(
                    "入力開始から登録先の対戦を選び、素点一覧をもう一度貼り付けてください。",
                )
                return
            target = matches[0] if matches else None

        # Validate before creating or modifying matches/half-games.
        setting = (
            (target.settings if target else None)
            or group.settings
            or EmbeddedGroupSettings()
        )
        if len(rows) != setting.num_of_players:
            reply_service.add_message(
                f"{setting.num_of_players}人分の素点一覧を貼り付けてください。登録していません。",
            )
            return
        points = {}
        for name, point in rows:
            user_id = user_service.get_line_user_id_by_name(name)
            if user_id is None or name == "友達未登録" or user_id in points:
                reply_service.add_message(
                    "名前が未登録・同名・重複のため特定できません。通常の点数入力を使ってください。登録していません。",
                )
                return
            points[user_id] = point
        expected_total = setting.starting_points * setting.num_of_players
        if not expected_total <= sum(points.values()) <= expected_total + 99:
            reply_service.add_message(
                f"点数の合計が{sum(points.values())}点です。合計{expected_total}点+αを確認してください。登録していません。",
            )
            return
        if len(set(points.values())) != setting.num_of_players:
            reply_service.add_message(
                "同点のユーザーがいます。上家が高くなるよう修正してください。登録していません。",
            )
            return
        existing = (
            hanchan_service.find_one_by_id(target.active_hanchan_id) if target else None
        )
        if (
            target
            and target.active_hanchan_id is not None
            and (
                existing is None
                or existing.raw_scores
                or existing.converted_scores
                or existing.match_id != target._id
                or existing.line_group_id != line_group_id
            )
        ):
            reply_service.add_message(
                "入力途中の半荘があります。先に現在の入力を完了してください。上書きしていません。",
            )
            return

        if target is None:
            target = match_service.create_with_line_group_id(
                line_group_id, settings=setting,
            )
        claimed = group_repository.update(
            {
                "_id": group._id,
                "active_match_id": group.current_input_match_id,
                "mode": group.mode,
            },
            {"active_match_id": target._id, "mode": GroupMode.input.value},
        )
        if not claimed:
            reply_service.add_message(
                "入力先が変わりました。登録先を確認して貼り付け直してください。",
            )
            return
        if existing is not None:
            # Fill only an empty half-game; a concurrent score must not be lost.
            hanchan = hanchan_repository.update_field(
                {"_id": existing._id, "raw_scores": {}, "converted_scores": {}},
                set_values={"raw_scores": points},
            )
            if hanchan is None:
                reply_service.add_message(
                    "別の点数入力が始まりました。上書きしていません。",
                )
                return
        else:
            hanchan = hanchan_repository.create(
                Hanchan(
                    line_group_id=line_group_id,
                    match_id=target._id,
                    raw_scores=points,
                ),
            )
            attached = match_repository.update_field(
                {
                    "_id": target._id,
                    "status": MatchStatus.open.value,
                    "active_hanchan_id": None,
                },
                set_values={"active_hanchan_id": hanchan._id},
            )
            if attached is None:
                hanchan_repository.update_field(
                    {"_id": hanchan._id}, set_values={"is_deleted": True},
                )
                reply_service.add_message(
                    "別の半荘入力が始まりました。貼り付けた半荘は登録していません。",
                )
                return
        SubmitHanchanUseCase().execute(
            expected_match_id=target._id,
            expected_hanchan_id=hanchan._id,
        )
