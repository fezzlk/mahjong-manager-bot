from DomainModel.entities.Group import Group, GroupMode
from repositories import session_scope, group_repository

dummy_groups = [
    Group(
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
        zoom_url="https://us01web.zoom.us/j/01234567891?pwd=abcdefghijklmnopqrstuvwxyz",
        mode=GroupMode.wait.value,
        _id=1,
    ),
    Group(
        line_group_id="G0123456789abcdefghijklmnopqrstu2",
        zoom_url="https://us01web.zoom.us/j/01234567892?pwd=abcdefghijklmnopqrstuvwxyz",
        mode=GroupMode.wait.value,
        _id=1,
    ),
]


def test_hit_1_record():
    # Arrange
    with session_scope() as session:
        group_repository.create(session, dummy_groups[0])

    # Act
    with session_scope() as session:
        result = group_repository.update(
            session=session,
            target=dummy_groups[1],
        )

    # Assert
    assert result == 1

    with session_scope() as session:
        record_on_db = group_repository.find_all(
            session,
        )

        assert len(record_on_db) == 1
        assert record_on_db[0]._id == dummy_groups[1]._id
        assert record_on_db[0].line_group_id == dummy_groups[1].line_group_id
        assert record_on_db[0].zoom_url == dummy_groups[1].zoom_url
        assert record_on_db[0].mode == dummy_groups[1].mode


def test_hit_0_record():
    # Arrange

    # Act
    with session_scope() as session:
        result = group_repository.update(
            session,
            dummy_groups[0],
        )

    # Assert
    assert result == 0
