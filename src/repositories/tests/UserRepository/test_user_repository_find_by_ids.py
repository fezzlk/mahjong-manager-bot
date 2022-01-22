from tests.dummies import generate_dummy_user_list
from Repositories import session_scope, user_repository
from Domains.Entities.User import User


def test_hit_with_ids():
    # Arrange
    with session_scope() as session:
        dummy_users = generate_dummy_user_list()[:3]
        for dummy_user in dummy_users:
            user_repository.create(
                session,
                dummy_user,
            )
    target_users = generate_dummy_user_list()[1:3]
    ids = [target_user._id for target_user in target_users]

    # Act
    with session_scope() as session:
        result = user_repository.find_by_ids(
            session,
            ids,
        )

    # Assert
        assert len(result) == len(target_users)
        for i in range(len(result)):
            assert isinstance(result[i], User)
            assert result[i]._id == target_users[i]._id
            assert result[i].line_user_name == target_users[i].line_user_name
            assert result[i].line_user_id == target_users[i].line_user_id
            assert result[i].zoom_url == target_users[i].zoom_url
            assert result[i].mode == target_users[i].mode
            assert result[i].jantama_name == target_users[i].jantama_name


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
        result = user_repository.find_by_ids(
            session,
            ids,
        )

    # Assert
        assert len(result) == 0
