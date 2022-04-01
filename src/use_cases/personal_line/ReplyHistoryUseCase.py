from ApplicationService import request_info_service, reply_service
from repositories import (
    user_match_repository,
    user_repository,
    match_repository,
    hanchan_repository,
    session_scope,
)
import itertools


class ReplyHistoryUseCase:

    def execute(self) -> None:
        req_line_id = request_info_service.req_line_user_id

        with session_scope() as session:
            user = user_repository.find_one_by_line_user_id(
                session,
                req_line_id,
            )

            if user is None:
                reply_service.add_message(
                    'ユーザーが登録されていません。友達追加してください。'
                )
                reply_service.add_message(
                    '既に友達の場合は一度ブロックして、ブロック解除を行ってください。'
                )
                return

            umList = user_match_repository.find_by_user_ids(
                session,
                [user._id],
            )
            matches = match_repository.find_archived_by_ids(
                session,
                [um.match_id for um in umList]
            )

            if len(matches) == 0:
                reply_service.add_message(
                    '対局履歴がありません。'
                )
                return

            all_hanchan_ids = list(
                itertools.chain.from_iterable(
                    [m.hanchan_ids for m in matches]
                )
            )

            all_hanchans = hanchan_repository.find_archived_by_ids(
                session,
                all_hanchan_ids,
            )

            if len(all_hanchans) == 0:
                raise ValueError('半荘情報を取得できませんでした。')

            dict_c_results = {h._id: h.converted_scores for h in all_hanchans}

            message = ''
            total = 0
            for match in matches:
                score = 0
                for hanchan_id in match.hanchan_ids:
                    score += dict_c_results[hanchan_id][req_line_id]
                total += score
                strScore = ('+' + str(score)) if score > 0 else str(score)
                message += match.created_at.strftime(
                    "%Y/%m/%d") + ': ' + strScore + '\n'

            reply_service.add_message(
                message
            )

            strTotal = ('+' + str(total)) if total > 0 else str(total)
            reply_service.add_message(
                '累計: ' + strTotal
            )
