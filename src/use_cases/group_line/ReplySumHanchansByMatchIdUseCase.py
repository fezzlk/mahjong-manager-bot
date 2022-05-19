from DomainService import (
    user_service,
)
from ApplicationService import (
    reply_service,
)
from repositories import session_scope, match_repository, hanchan_repository


class ReplySumHanchansByMatchIdUseCase:

    def execute(self, match_id: int) -> None:
        with session_scope() as session:
            match = match_repository.find_by_ids(
                session=session,
                ids=[match_id],
            )

        ids = match.hanchan_ids
        date = match.created_at.strftime('%Y-%m-%d') + '\n',
        with session_scope() as session:
            hanchans = hanchan_repository.find_by_ids(
                session, ids)

        hanchans_list = []
        sum_hanchans = {}

        for i in range(len(ids)):
            converted_scores = hanchans[i].converted_scores
            detail = []
            for r in sorted(
                converted_scores.items(),
                key=lambda x: x[1],
                reverse=True
            ):
                name = user_service.get_name_by_line_user_id(r[0])
                if name is None:
                    continue
                detail.append(f'{name}: {"+" if r[1] > 0 else ""}{r[1]}')
            hanchans_list.append(
                f'第{i+1}回\n' + '\n'.join(detail)
            )

            for line_user_id, converted_score in converted_scores.items():
                if line_user_id not in sum_hanchans.keys():
                    sum_hanchans[line_user_id] = 0

                sum_hanchans[line_user_id] += converted_score

        reply_service.add_message(
            '友達登録しているユーザーのみ表示しています。\n' +
            '\n\n'.join(hanchans_list))

        detail = []
        for r in sorted(
            sum_hanchans.items(),
            key=lambda x: x[1],
            reverse=True
        ):
            name = user_service.get_name_by_line_user_id(r[0])
            if name is None:
                continue
            detail.append(
                f'{name}: {"+" if r[1] > 0 else ""}{r[1]}')

        reply_service.add_message(
            '総計\n' + date + '\n'.join(detail)
        )
