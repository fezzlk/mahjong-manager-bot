import pytest
from tests.dummies import generate_dummy_user_list
from db_setting import Session
from repositories import session_scope
from repositories.user_repository import UserRepository
from domains.user import User

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
    other_users = dummy_users[:2]
    target_line_user_id = dummy_users[2].line_user_id

    # Act
    with session_scope() as session:
        UserRepository.delete_one_by_line_user_id(
            session,
            target_line_user_id,
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
        dummy_users = generate_dummy_user_list()[:2]
        for dummy_user in dummy_users:
            UserRepository.create(
                session,
                dummy_user,
            )
    target_line_user_id = generate_dummy_user_list()[2].line_user_id

    # Act
    with session_scope() as session:
        result = UserRepository.delete_one_by_line_user_id(
            session,
            target_line_user_id,
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


def test_NG_with_line_user_id_none():
    with pytest.raises(ValueError):
        # Arrange
        # Do nothing

        # Act
        with session_scope() as session:
            UserRepository.delete_one_by_line_user_id(
                session,
                None,
            )

        # Assert
        # Do nothing
