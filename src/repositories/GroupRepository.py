from models import GroupSchema
from domains.Group import Group, GroupMode
from sqlalchemy.orm.session import Session as BaseSession


class GroupRepository:

    def find_one_by_group_id(
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

        return Group(
            line_group_id=record.line_group_id,
            zoom_url=record.zoom_url,
            mode=GroupMode[record.mode],
            _id=record.id,
        )

    def find_by_ids(
        self,
        session: BaseSession,
        ids: list,
    ) -> list:
        records = session\
            .query(GroupSchema)\
            .filter(GroupSchema.id.in_(ids))\
            .order_by(GroupSchema.id)\
            .all()

        return [
            Group(
                line_group_id=record.line_group_id,
                zoom_url=record.zoom_url,
                mode=GroupMode[record.mode],
                _id=record.id,
            )
            for record in records
        ]

    def find_all(
        self,
        session: BaseSession,
    ) -> list:
        records = session\
            .query(GroupSchema)\
            .order_by(GroupSchema.id)\
            .all()

        return [
            Group(
                line_group_id=record.line_group_id,
                zoom_url=record.zoom_url,
                mode=GroupMode[record.mode],
                _id=record.id,
            )
            for record in records
        ]

    def create(
        self,
        session: BaseSession,
        new_group: Group,
    ) -> None:
        record = GroupSchema(
            line_group_id=new_group.line_group_id,
            mode=new_group.mode.value,
            zoom_url=new_group.zoom_url,
        )
        session.add(record)

    def delete_by_ids(
        self,
        session: BaseSession,
        ids: list,
    ) -> None:
        session\
            .query(GroupSchema)\
            .filter(GroupSchema.id.in_(ids))\
            .delete(synchronize_session=False)

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

        return Group(
            line_group_id=record.line_group_id,
            zoom_url=record.zoom_url,
            mode=GroupMode[record.mode],
            _id=record.id,
        )

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

        return Group(
            line_group_id=record.line_group_id,
            zoom_url=record.zoom_url,
            mode=GroupMode[record.mode],
            _id=record.id,
        )
