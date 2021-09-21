import pytest
from tests.dummies import generate_dummy_user_list
from db_setting import Session
from repositories import session_scope
from repositories.UserRepository import UserRepository
from domains.User import User

session = Session()


def test_hit_1_record():
    # Arrange
    dummy_users = generate_dummy_user_list()[:3]
    with session_scope() as session:
        for dummy_user in dummy_users:
            UserRepository.create(
                session,
                dummy_user,
            )
    target_user = dummy_users[0]

    # Act
    with session_scope() as session:
        result = UserRepository.find_one_by_name(
            session,
            target_user.name,
        )

    # Assert
        assert isinstance(result, User)
        assert result.name == target_user.name
        assert result.line_user_id == target_user.line_user_id
        assert result.zoom_url == target_user.zoom_url
        assert result.mode == target_user.mode
        assert result.jantama_name == target_user.jantama_name


def test_hit_some_records():
    # Arrange
    dummy_users = generate_dummy_user_list()[:4]
    with session_scope() as session:
        for dummy_user in dummy_users:
            UserRepository.create(
                session,
                dummy_user,
            )
    target_user = dummy_users[2]

    # Act
    with session_scope() as session:
        result = UserRepository.find_one_by_name(
            session,
            target_user.name,
        )

    # Assert
        assert isinstance(result, User)
        assert result.name == target_user.name
        assert result.line_user_id == target_user.line_user_id
        assert result.zoom_url == target_user.zoom_url
        assert result.mode == target_user.mode
        assert result.jantama_name == target_user.jantama_name


def test_hit_0_record():
    # Arrange
    with session_scope() as session:
        dummy_users = generate_dummy_user_list()[:2]
        for dummy_user in dummy_users:
            UserRepository.create(
                session,
                dummy_user,
            )
    target_user = generate_dummy_user_list()[2]

    # Act
    with session_scope() as session:
        result = UserRepository.find_one_by_name(
            session,
            target_user.name,
        )

    # Assert
        assert result is None


def test_NG_with_line_user_id_none():
    with pytest.raises(ValueError):
        # Arrange
        # Do nothing

        # Act
        with session_scope() as session:
            UserRepository.find_one_by_name(
                session,
                None,
            )

        # Assert
        # Do nothing
