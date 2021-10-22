from tests.dummies import generate_dummy_user_list
from repositories import session_scope, user_repository
from domains.User import User


def test_hit_with_ids():
    # Arrange
    dummy_users = generate_dummy_user_list()[:3]
    with session_scope() as session:
        for dummy_user in dummy_users:
            user_repository.create(
                session,
                dummy_user,
            )
    other_users = dummy_users[:1]
    target_users = dummy_users[1:3]
    ids = [target_user._id for target_user in target_users]

    # Act
    with session_scope() as session:
        user_repository.delete_by_ids(
            session,
            ids,
        )

    # Assert
    with session_scope() as session:
        result = user_repository.find_all(
            session,
        )
        assert len(result) == len(other_users)
        for i in range(len(result)):
            assert isinstance(result[i], User)
            assert result[i].name == other_users[i].name
            assert result[i].line_user_id == other_users[i].line_user_id
            assert result[i].zoom_url == other_users[i].zoom_url
            assert result[i].mode == other_users[i].mode
            assert result[i].jantama_name == other_users[i].jantama_name


def test_hit_0_record():
    # Arrange
    with session_scope() as session:
        dummy_users = generate_dummy_user_list()[:3]
        for dummy_user in dummy_users:
            user_repository.create(
                session,
                dummy_user,
            )
    target_users = generate_dummy_user_list()[3:6]
    ids = [target_user._id for target_user in target_users]

    # Act
    with session_scope() as session:
        result = user_repository.delete_by_ids(
            session,
            ids,
        )

    # Assert
    with session_scope() as session:
        result = user_repository.find_all(
            session,
        )
        assert len(result) == len(dummy_users)
        for i in range(len(result)):
            assert isinstance(result[i], User)
            assert result[i].name == dummy_users[i].name
            assert result[i].line_user_id == dummy_users[i].line_user_id
            assert result[i].zoom_url == dummy_users[i].zoom_url
            assert result[i].mode == dummy_users[i].mode
            assert result[i].jantama_name == dummy_users[i].jantama_name