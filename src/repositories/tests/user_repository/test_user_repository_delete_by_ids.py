from tests.dummies import generate_dummy_user_list
from db_setting import Session
from repositories import session_scope
from repositories.user_repository import UserRepository
from domains.user import User

session = Session()


def test_hit_with_ids():
    # Arrange
    dummy_users = generate_dummy_user_list()[:3]
    with session_scope() as session:
        for dummy_user in dummy_users:
            UserRepository.create(
                session,
                dummy_user,
            )
    other_users = dummy_users[:1]
    target_users = dummy_users[1:3]
    ids = [target_user._id for target_user in target_users]

    # Act
    with session_scope() as session:
        UserRepository.delete_by_ids(
            session,
            ids,
        )

    # Assert
    with session_scope() as session:
        result = UserRepository.find_all(
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


def test_hit_with_an_id_as_not_list():
    # Arrange
    dummy_users = generate_dummy_user_list()[:3]
    with session_scope() as session:
        for dummy_user in dummy_users:
            UserRepository.create(
                session,
                dummy_user,
            )
    other_users = dummy_users[:2]
    target_user = dummy_users[2]
    target_user_id = target_user._id

    # Act
    with session_scope() as session:
        result = UserRepository.delete_by_ids(
            session,
            target_user_id,
        )

    # Assert
    with session_scope() as session:
        result = UserRepository.find_all(
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
            UserRepository.create(
                session,
                dummy_user,
            )
    target_users = generate_dummy_user_list()[3:6]
    ids = [target_user._id for target_user in target_users]

    # Act
    with session_scope() as session:
        result = UserRepository.delete_by_ids(
            session,
            ids,
        )

    # Assert
    with session_scope() as session:
        result = UserRepository.find_all(
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
