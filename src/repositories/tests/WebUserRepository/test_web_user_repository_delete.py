from tests.dummies import generate_dummy_web_user_list
from repositories import web_user_repository
from DomainModel.entities.WebUser import WebUser


def test_hit_1_record():
    # Arrange
    dummy_web_users = generate_dummy_web_user_list()[:3]
    for dummy_web_user in dummy_web_users:
        web_user_repository.create(
            dummy_web_user,
        )
    other_users = dummy_web_users[:2]

    # Act
    result = web_user_repository.delete(
        query={'user_code': dummy_web_users[2].user_code},
    )

    # Assert
    assert result == 1
    record_on_db = web_user_repository.find()
    assert len(record_on_db) == len(other_users)
    for i in range(len(record_on_db)):
        assert isinstance(record_on_db[i], WebUser)
        assert record_on_db[i].user_code == dummy_web_users[i].user_code
        assert record_on_db[i].name == dummy_web_users[i].name
        assert record_on_db[i].email == dummy_web_users[i].email
        assert record_on_db[i].linked_line_user_id == dummy_web_users[i].linked_line_user_id
        assert record_on_db[i].is_approved_line_user == dummy_web_users[i].is_approved_line_user


def test_hit_0_record():
    # Arrange
    dummy_web_users = generate_dummy_web_user_list()[:3]
    for dummy_web_user in dummy_web_users:
        web_user_repository.create(
            dummy_web_user,
        )
    target_web_users = generate_dummy_web_user_list()[3:6]
    user_codes = [target_web_user.user_code for target_web_user in target_web_users]

    # Act
    result = web_user_repository.delete(
        query={'user_code': {'$in': user_codes}},
    )

    # Assert
    assert result == 0
    record_on_db = web_user_repository.find()
    assert len(record_on_db) == len(dummy_web_users)
    for i in range(len(record_on_db)):
        assert isinstance(record_on_db[i], WebUser)
        assert record_on_db[i].user_code == dummy_web_users[i].user_code
        assert record_on_db[i].name == dummy_web_users[i].name
        assert record_on_db[i].email == dummy_web_users[i].email
        assert record_on_db[i].linked_line_user_id == dummy_web_users[i].linked_line_user_id
        assert record_on_db[i].is_approved_line_user == dummy_web_users[i].is_approved_line_user
