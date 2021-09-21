from tests.dummies import generate_dummy_user_list
from db_setting import Session
from repositories import session_scope
from repositories.UserRepository import UserRepository
from domains.User import User

session = Session()


def test_hit_with_ids():
    # Arrange
    with session_scope() as session:
        dummy_users = generate_dummy_user_list()[:3]
        for dummy_user in dummy_users:
            UserRepository.create(
                session,
                dummy_user,
            )
    target_users = generate_dummy_user_list()[1:3]
    ids = [target_user._id for target_user in target_users]

    # Act
    with session_scope() as session:
        result = UserRepository.find_by_ids(
            session,
            ids,
        )

    # Assert
        assert len(result) == len(target_users)
        for i in range(len(result)):
            assert isinstance(result[i], User)
            assert result[i].name == target_users[i].name
            assert result[i].line_user_id == target_users[i].line_user_id
            assert result[i].zoom_url == target_users[i].zoom_url
            assert result[i].mode == target_users[i].mode
            assert result[i].jantama_name == target_users[i].jantama_name


def test_hit_with_an_id_as_not_list():
    # Arrange
    with session_scope() as session:
        dummy_users = generate_dummy_user_list()[:3]
        for dummy_user in dummy_users:
            UserRepository.create(
                session,
                dummy_user,
            )
    target_user = generate_dummy_user_list()[2]
    target_line_user_id = target_user._id

    # Act
    with session_scope() as session:
        result = UserRepository.find_by_ids(
            session,
            target_line_user_id,
        )

    # Assert
        assert len(result) == 1
        assert result[0].name == target_user.name
        assert result[0].line_user_id == target_user.line_user_id
        assert result[0].zoom_url == target_user.zoom_url
        assert result[0].mode == target_user.mode
        assert result[0].jantama_name == target_user.jantama_name


def test_hit_0_record():
    # Arrange
    with session_scope() as session:
        dummy_users = generate_dummy_user_list()[:3]
        for dummy_user in dummy_users:
            UserRepository.create(
                session,
                dummy_user,
            )
    target_users = generate_dummy_user_list()[3:6]
    ids = [target_user._id for target_user in target_users]

    # Act
    with session_scope() as session:
        result = UserRepository.find_by_ids(
            session,
            ids,
        )

    # Assert
        assert len(result) == 0
