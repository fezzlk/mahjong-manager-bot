from repositories import hanchan_repository
from DomainModel.entities.Hanchan import Hanchan
from .interfaces.IHanchanService import IHanchanService
from typing import Optional

STATUS_LIST = ['disabled', 'active', 'archived']


class HanchanService(IHanchanService):

    # def disabled_by_id(
    #     self,
    #     line_group_id: str,
    #     hanchan_id: int,
    # ) -> Hanchan:
    #     """disabled target hanchan"""
    #     with session_scope() as session:
    #         target = hanchan_repository.find_one_by_id_and_line_group_id(
    #             session=session,
    #             hanchan_id=hanchan_id,
    #             line_group_id=line_group_id,
    #         )

    #         if target is None:
    #             raise ValueError('Not found hanchan')

    #         updated_hanchan = hanchan_repository.update_one_status_by_id(
    #             session,
    #             hanchan_id=target._id,
    #             status=0,
    #         )

    #         print(
    #             f'disabled: _id={updated_hanchan._id}'
    #         )

    #         return updated_hanchan

    def add_or_drop_raw_score(
        self,
        line_group_id: str,
        line_user_id: str,
        raw_score: Optional[int],
    ) -> Hanchan:
        if line_user_id is None:
            raise ValueError('fail to add_or_drop_raw_score: line_user_id is required')

        result = hanchan_repository.find({
            'line_group_id': line_group_id,
            'status': 1,
        })

        if len(result) == 0:
            raise ValueError('fail to add_or_drop_raw_score: Not found hanchan')

        target = result[0]
        raw_scores = target.raw_scores

        if raw_score is None:
            raw_scores.pop(line_user_id, None)
        else:
            raw_scores[line_user_id] = raw_score

        hanchan_repository.update(
            {'_id': target._id},
            {'raw_scores': raw_scores},
        )

        target.raw_scores = raw_scores
        return target

    # def update_current_converted_score(
    #     self,
    #     line_group_id: str,
    #     converted_scores: Dict[str, int],
    # ) -> Hanchan:
    #     with session_scope() as session:
    #         target = hanchan_repository.find_and_status(
    #             session=session,
    #             line_group_id=line_group_id,
    #             status=1,
    #         )

    #         if target is None:
    #             raise ValueError('Not found hanchan')

    #         updated_hanchan = hanchan_repository.update_one_converted_scores_by_id(
    #             session=session, hanchan_id=target._id, converted_scores=converted_scores)

    #         print(
    #             f'update hanchan: _id={updated_hanchan._id}'
    #         )

    #     return updated_hanchan

    def update_status_active_hanchan(
        self,
        line_group_id: str,
        status: int,
    ) -> Hanchan:
        current = self.get_current(line_group_id=line_group_id)

        if current is None:
            return None
        
        update_count = hanchan_repository.update(
            {'_id': current._id},
            {'status': status},
        )

        if update_count == 1:
            print(
                f'{STATUS_LIST[status]} hanchan: _id={current._id}'
            )

        return current

    def archive(self, line_group_id: str) -> Hanchan:
        return self.update_status_active_hanchan(line_group_id, 2)

    def disable(self, line_group_id: str) -> Hanchan:
        return self.update_status_active_hanchan(line_group_id, 0)

    # # def get_point_and_name_from_text(
    # #     self,
    # #     text: str,
    # # ) -> Tuple[str, str]:
    # #     s = text.split()
    # #     if len(s) >= 2:
    # #         # ユーザー名に空白がある場合を考慮し、最後の要素をポイント、そのほかをユーザー名として判断する
    # #         return s[-1], ' '.join(s[:-1])
    # #     # fixme: ユーザー名「taro 100」の点数を削除しようとした場合に上の条件にひっかかる
    # #     # 名前のみによるメッセージでの削除機能自体をやめるか(更新できるから削除は需要ない)
    # #     elif len(s) == 1:
    # #         return 'delete', s[0]

    # def find_or_create_current(self, line_group_id: str) -> Hanchan:
    #     current = self.get_current(line_group_id)

    #     if current is None:
    #         new_hanchan = Hanchan(
    #             line_group_id=line_group_id,
    #             status=1,
    #         )
    #         hanchan_repository.create(new_hanchan)

    #         print(f'create hanchan: group "{line_group_id}"')
    #         current = new_hanchan

    #     return current

    def get_current(self, line_group_id: str) -> Hanchan:
        hanchans = hanchan_repository.find({
            '$and': [
                {'line_group_id': line_group_id},
                {'status': 1},
            ]
        })
        
        if len(hanchans) == 0:
            return None
        return hanchans[0]
