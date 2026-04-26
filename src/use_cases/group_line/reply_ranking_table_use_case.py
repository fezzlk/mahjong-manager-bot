import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Tuple

import certifi
import urllib3

import env_var
from application_service import (
    message_service,
    ranking_table_image_builder,
    reply_service,
    request_info_service,
)
from domain_service import (
    hanchan_service,
    match_service,
    user_hanchan_service,
    user_match_service,
    user_service,
)
from messaging_api_setting import line_bot_api

logger = logging.getLogger(__name__)


@dataclass
class _RankingStats:
    sorted_total_dict: list = field(default_factory=list)
    point_dict: dict = field(default_factory=dict)
    max_score_dict: dict = field(default_factory=dict)
    sorted_ave_rank_dict: list = field(default_factory=list)
    ave_rank_str_dict: dict = field(default_factory=dict)
    rank_dict: dict = field(default_factory=dict)


class ReplyRankingTableUseCase:
    def execute(self) -> None:
        # 1. ユーザー解決
        target_user_ids, active_user_line_ids = self._resolve_users()

        # 2. 日付範囲解析
        from_dt, to_dt, is_valid = message_service.parse_date_range_from_params(
            request_info_service.params,
        )
        if not is_valid:
            for msg in message_service.DATE_FORMAT_ERROR_MESSAGES:
                reply_service.add_message(msg)
            return

        # 3. DB取得
        matches, hanchans, user_hanchans = self._fetch_data(
            target_user_ids, active_user_line_ids, from_dt, to_dt,
        )

        # 4. 範囲メッセージ
        range_message = message_service.create_range_message(from_dt, to_dt)
        if range_message is not None:
            reply_service.add_message(range_message)

        # 5. プロフィール画像取得
        display_name_dict = self._fetch_profile_images(active_user_line_ids)

        # 6. データ集計
        stats = self._aggregate_stats(matches, hanchans, user_hanchans, active_user_line_ids)

        # 7. 累計得点表 画像生成・送信
        req_line_user_id = request_info_service.req_line_user_id
        try:
            url = ranking_table_image_builder.build_score_table(
                stats.sorted_total_dict,
                display_name_dict,
                stats.point_dict,
                stats.max_score_dict,
                req_line_user_id,
            )
            reply_service.add_image(url)
        except FileNotFoundError:
            self._handle_image_save_error()
            return

        # 8. 順位表 画像生成・送信
        try:
            url = ranking_table_image_builder.build_rank_table(
                stats.sorted_ave_rank_dict,
                display_name_dict,
                stats.ave_rank_str_dict,
                stats.rank_dict,
                req_line_user_id,
            )
            reply_service.add_image(url)
        except FileNotFoundError:
            self._handle_image_save_error()

    def _resolve_users(self) -> Tuple[List[int], List[str]]:
        req_line_user_id = request_info_service.req_line_user_id
        mention_line_user_ids = request_info_service.mention_line_ids
        target_user_ids: List[int] = []
        active_user_line_ids: List[str] = []
        contain_not_friend_user = False

        mention_line_user_ids.append(req_line_user_id)

        for mention_line_user_id in set(mention_line_user_ids):
            user = user_service.find_one_by_line_user_id(mention_line_user_id)
            if user is None:
                contain_not_friend_user = True
                continue
            active_user_line_ids.append(user.line_user_id)
            target_user_ids.append(user._id)

        if contain_not_friend_user:
            reply_service.add_message("友達登録されていないユーザは表示されません。")

        if request_info_service.is_mention_all:
            reply_service.add_message(
                "@Allによるメンションでは、このグループでの対戦に参加したことのある全ユーザを対象とします。",
            )

        return target_user_ids, active_user_line_ids

    def _fetch_data(self, target_user_ids, active_user_line_ids, from_dt, to_dt):
        um_list = user_match_service.find_all_by_user_id_list(
            target_user_ids,
            from_dt=from_dt,
            to_dt=to_dt,
        )
        matches = match_service.find_all_by_ids_and_line_group_ids(
            ids=[um.match_id for um in um_list],
            line_group_ids=[request_info_service.req_line_group_id],
        )
        hanchans = hanchan_service.find_all_archived_by_match_ids(
            match_ids=[m._id for m in matches],
        )
        user_hanchans = user_hanchan_service.find_all_with_line_user_ids_and_hanchan_ids(
            line_user_ids=active_user_line_ids,
            hanchan_ids=[h._id for h in hanchans],
            from_dt=from_dt,
            to_dt=to_dt,
        )
        return matches, hanchans, user_hanchans

    def _fetch_profile_images(self, active_user_line_ids: List[str]) -> Dict[str, str]:
        display_name_dict = {}
        Path("src/uploads/profile_image").mkdir(parents=True, exist_ok=True)
        for line_id in active_user_line_ids:
            profile = line_bot_api.get_profile(line_id)
            display_name_dict[line_id] = profile.display_name
            if not profile.picture_url:
                continue
            request_methods = urllib3.PoolManager(
                cert_reqs="CERT_REQUIRED", ca_certs=certifi.where(),
            )
            response = request_methods.request("GET", profile.picture_url)
            with open(f"src/uploads/profile_image/{line_id}.jpeg", "wb") as f:
                f.write(response.data)
        return display_name_dict

    def _aggregate_stats(self, matches, hanchans, user_hanchans, active_user_line_ids) -> _RankingStats:
        # 累計スコア
        total_dict = dict.fromkeys(active_user_line_ids, 0)
        for match in matches:
            for line_id, score in match.sum_scores.items():
                if line_id in active_user_line_ids:
                    total_dict[line_id] += score

        point_dict = {line_id: [] for line_id in active_user_line_ids}
        rank_dict = {
            line_id: {1: 0, 2: 0, 3: 0, 4: 0, 0: 0} for line_id in active_user_line_ids
        }
        for uh in user_hanchans:
            point_dict[uh.line_user_id].append(uh.point)
            rank_dict[uh.line_user_id][uh.rank] += 1
            if uh.point < 0:
                rank_dict[uh.line_user_id][0] += 1

        dummy_min_score = ranking_table_image_builder.DUMMY_MIN_SCORE
        max_score_dict = dict.fromkeys(active_user_line_ids, dummy_min_score)
        for h in hanchans:
            for u, c in h.converted_scores.items():
                if u in max_score_dict:
                    max_score_dict[u] = max(max_score_dict[u], c)

        ave_rank_str_dict = {}
        ave_rank_dict = {}
        for line_id in rank_dict:
            h_count = sum([rank_dict[line_id][i] for i in range(1, 5)])
            if h_count == 0:
                ave_rank_str_dict[line_id] = "-"
                ave_rank_dict[line_id] = 5
            else:
                ave_rank_str_dict[line_id] = (
                    f"{sum([rank_dict[line_id][i] * i for i in range(1, 5)]) / h_count:.2f}"
                )
                ave_rank_dict[line_id] = (
                    sum([rank_dict[line_id][i] * i for i in range(1, 5)]) / h_count
                )

        sorted_total_dict = sorted(total_dict.items(), key=lambda x: x[1], reverse=True)
        sorted_ave_rank_dict = sorted(ave_rank_dict.items(), key=lambda x: x[1], reverse=False)

        return _RankingStats(
            sorted_total_dict=sorted_total_dict,
            point_dict=point_dict,
            max_score_dict=max_score_dict,
            sorted_ave_rank_dict=sorted_ave_rank_dict,
            ave_rank_str_dict=ave_rank_str_dict,
            rank_dict=rank_dict,
        )

    def _handle_image_save_error(self) -> None:
        logger.error("ranking table image save failed: group=%s", request_info_service.req_line_group_id)
        reply_service.reset()
        reply_service.add_message(text="システムエラーが発生しました。")
        messages = [
            "ランキングの画像アップロードに失敗しました",
            "送信者: "
            + (
                user_service.get_name_by_line_user_id(
                    request_info_service.req_line_user_id,
                )
                or request_info_service.req_line_user_id
            ),
        ]
        reply_service.push_a_message(
            to=env_var.SERVER_ADMIN_LINE_USER_ID,
            message="\n".join(messages),
        )
