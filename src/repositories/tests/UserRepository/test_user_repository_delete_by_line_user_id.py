from tests.dummies import generate_dummy_user_list
from repositories import session_scope, user_repository
from domains.entities.User import User


def test_hit_1_record():
    # Arrange
    dummy_users = generate_dummy_user_list()[:3]
    with session_scope() as session:
        for dummy_user in dummy_users:
            user_repository.create(
                session,
                dummy_user,
            )
    other_users = dummy_users[:2]
    target_line_user_id = dummy_users[2].line_user_id

    # Act
    with session_scope() as session:
        result = user_repository.delete_by_line_user_id(
            session,
            target_line_user_id,
        )

    # Assert
    assert result == 1
    with session_scope() as session:
        record_on_db = user_repository.find_all(
            session,
        )
        assert len(record_on_db) == len(other_users)
        for i in range(len(record_on_db)):
            assert isinstance(record_on_db[i], User)
            assert record_on_db[i]._id == other_users[i]._id
            assert record_on_db[i].line_user_name == other_users[i].line_user_name
            assert record_on_db[i].line_user_id == other_users[i].line_user_id
            assert record_on_db[i].zoom_url == other_users[i].zoom_url
            assert record_on_db[i].mode == other_users[i].mode
            assert record_on_db[i].jantama_name == other_users[i].jantama_name


def test_hit_0_record():
    # Arrange
    with session_scope() as session:
        dummy_users = generate_dummy_user_list()[:2]
        for dummy_user in dummy_users:
            user_repository.create(
                session,
                dummy_user,
            )
    target_line_user_id = generate_dummy_user_list()[2].line_user_id

    # Act
    with session_scope() as session:
        result = user_repository.delete_by_line_user_id(
            session,
            target_line_user_id,
        )

    # Assert
    assert result == 0
    with session_scope() as session:
        record_on_db = user_repository.find_all(
            session,
        )
        assert len(record_on_db) == len(dummy_users)
        for i in range(len(record_on_db)):
            assert isinstance(record_on_db[i], User)
            assert record_on_db[i]._id == dummy_users[i]._id
            assert record_on_db[i].line_user_name == dummy_users[i].line_user_name
            assert record_on_db[i].line_user_id == dummy_users[i].line_user_id
            assert record_on_db[i].zoom_url == dummy_users[i].zoom_url
            assert record_on_db[i].mode == dummy_users[i].mode
            assert record_on_db[i].jantama_name == dummy_users[i].jantama_name
