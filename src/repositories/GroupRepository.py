from typing import List
from models import GroupSchema
from domains.Group import Group, GroupMode
from sqlalchemy.orm.session import Session as BaseSession


class GroupRepository:

    def create(
        self,
        session: BaseSession,
        new_group: Group,
    ) -> Group:
        record = GroupSchema(
            line_group_id=new_group.line_group_id,
            mode=new_group.mode.value,
            zoom_url=new_group.zoom_url,
        )
        session.add(record)
        session.commit()
        new_group._id = record.id
        return new_group

    def delete_by_ids(
        self,
        session: BaseSession,
        ids: List[str],
    ) -> int:
        delete_count = session\
            .query(GroupSchema)\
            .filter(GroupSchema.id.in_(ids))\
            .delete(synchronize_session=False)

        return delete_count

    def find_all(
        self,
        session: BaseSession,
    ) -> List[Group]:
        records = session\
            .query(GroupSchema)\
            .order_by(GroupSchema.id)\
            .all()

        return [
            self._mapping_record_to_group_domain(record)
            for record in records
        ]

    def find_by_ids(
        self,
        session: BaseSession,
        ids: List[str],
    ) -> List[Group]:
        records = session\
            .query(GroupSchema)\
            .filter(GroupSchema.id.in_(ids))\
            .order_by(GroupSchema.id)\
            .all()

        return [
            self._mapping_record_to_group_domain(record)
            for record in records
        ]

    def find_one_by_line_group_id(
        self,
        session: BaseSession,
        line_group_id: int,
    ) -> Group:
        record = session\
            .query(GroupSchema)\
            .filter(GroupSchema.line_group_id == line_group_id)\
            .first()

        if record is None:
            return None

        return self._mapping_record_to_group_domain(record)

    def update_one_mode_by_line_group_id(
        self,
        session: BaseSession,
        line_group_id: str,
        mode: GroupMode,
    ) -> Group:
        if line_group_id is None:
            raise ValueError

        record = session\
            .query(GroupSchema)\
            .filter(GroupSchema.line_group_id == line_group_id)\
            .first()

        if record is None:
            return None

        record.mode = mode.value

        return self._mapping_record_to_group_domain(record)

    def update_one_zoom_url_by_line_group_id(
        self,
        session: BaseSession,
        line_group_id: str,
        zoom_url: str,
    ) -> Group:
        record = session\
            .query(GroupSchema)\
            .filter(GroupSchema.line_group_id == line_group_id)\
            .first()

        if record is None:
            return None

        record.zoom_url = zoom_url

        return self._mapping_record_to_group_domain(record)

    def _mapping_record_to_group_domain(self, record: GroupSchema) -> Group:
        return Group(
            line_group_id=record.line_group_id,
            zoom_url=record.zoom_url,
            mode=GroupMode[record.mode],
            _id=record.id,
        )
