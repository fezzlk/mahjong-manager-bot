from bson.errors import InvalidId
from bson.objectid import ObjectId

from application_service import (
    message_service,
    reply_service,
    request_info_service,
)
from domain_model.entities.match import Match, MatchStatus
from domain_service import (
    group_setting_service,
    hanchan_service,
    match_service,
)
from use_cases.group_line.create_match_detail_graph_use_case import (
    CreateMatchDetailGraphUseCase,
)


class ReplyMatchByIndexUseCase:
    def execute(self, str_index: str) -> None:
        """_match N: 位置インデックス指定(後方互換用)。"""
        line_group_id = request_info_service.req_line_group_id
        archived_matches = match_service.find_all_archived_by_line_group_id(line_group_id=line_group_id)
        if not str_index.isdigit():
            reply_service.add_message(
                "引数は整数で指定してください。",
            )
            return

        index = int(str_index)
        if index < 1 or len(archived_matches) < index:
            reply_service.add_message(
                f"このトークルームには全{len(archived_matches)}回までしか登録されていないため第{index}回はありません。",
            )
            return

        match = archived_matches[index - 1]
        self._show(line_group_id, match, index)

    def select(self) -> None:
        """_match_select?to=<match_id>: ボタン選択で指定された対戦の詳細を表示する。"""
        line_group_id = request_info_service.req_line_group_id
        match_id = request_info_service.params.get("to")

        if not match_id:
            reply_service.add_message("表示する対戦が指定されていません。")
            return

        try:
            target_match = match_service.find_one_by_id(ObjectId(match_id))
        except InvalidId:
            target_match = None
        if (
            target_match is None
            or target_match.line_group_id != line_group_id
            or target_match.status != MatchStatus.settled.value
        ):
            reply_service.add_message("指定された対戦が見つかりません。")
            return

        # 全件リスト内での「第N回」番号を算出する
        archived_matches = match_service.find_all_archived_by_line_group_id(line_group_id=line_group_id)
        index = next(
            (i + 1 for i, m in enumerate(archived_matches) if m._id == target_match._id),
            None,
        )
        if index is None:
            reply_service.add_message("指定された対戦が見つかりません。")
            return

        self._show(line_group_id, target_match, index)

    def _show(self, line_group_id: str, match: Match, index: int) -> None:
        # 精算された時点の設定を優先する(グループの現在の設定ではなく)。
        # settings未設定(旧データ)はグループの現在の設定にフォールバックする。
        # FEZ-66 Phase D
        setting = match.settings or group_setting_service.find_or_create(line_group_id)
        # 複数系列を実際に使ったことがあるグループのみ対戦名を表示する
        # (単一系列グループでは無用な表示になるため。FEZ-66 Phase F)
        show_name = match_service.count_non_sim_by_line_group_id(line_group_id) > 1
        result = message_service.create_show_match_result(
            match=match, unit=setting.unit, show_name=show_name,
        )

        reply_service.add_message(f'第{index}回\n{match.created_at.strftime("%Y年%m月%d日")}\n{result}')

        # 半荘情報
        hanchans = hanchan_service.find_all_archived_by_match_id(match._id)
        results_view_list = []
        sum_scores = {}
        for i, hanchan in enumerate(hanchans):
            for u, s in hanchan.converted_scores.items():
                if u in sum_scores:
                    sum_scores[u] += s
                else:
                    sum_scores[u] = s
            results_view_list.append(
                f"第{i+1}回\n{message_service.create_show_converted_scores(hanchan.converted_scores, sum_scores)}",
            )

        reply_service.add_message("【半荘情報】\n\n" + "\n\n".join(results_view_list))

        # グラフ描画。再オープン・削除ボタンのQuick Replyは最後に送信される
        # 画像メッセージへ付与する(reply_service.build_drop_target_quick_replyの
        # docstring参照)。
        reply_service.add_image(
            CreateMatchDetailGraphUseCase().execute(match._id),
            quick_reply=reply_service.build_match_detail_quick_reply(match),
        )
