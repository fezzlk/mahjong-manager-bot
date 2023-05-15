from tests.dummies import generate_dummy_web_user_list
from repositories import web_user_repository
from DomainModel.entities.WebUser import WebUser
from bson.objectid import ObjectId


def test_success_find_records():
    # Arrange
    dummy_web_users = generate_dummy_web_user_list()
    for dummy_web_user in dummy_web_users:
        web_user_repository.create(
            dummy_web_user,
        )

    # Act
    result = web_user_repository.find()

    # Assert
    assert len(result) == len(dummy_web_users)
    for i in range(len(result)):
        assert isinstance(result[i], WebUser)
        assert type(result[i]._id) == ObjectId
        assert result[i].user_code == dummy_web_users[i].user_code
        assert result[i].name == dummy_web_users[i].name
        assert result[i].email == dummy_web_users[i].email
        assert result[i].linked_line_user_id == dummy_web_users[i].linked_line_user_id
        assert result[i].is_approved_line_user == dummy_web_users[i].is_approved_line_user


def test_success_find_0_record():
    # Arrange
    # Do nothing

    # Act
    result = web_user_repository.find()

    # Assert
    assert len(result) == 0


def test_hit_1_record():
    # Arrange
    dummy_web_users = generate_dummy_web_user_list()[:3]
    for dummy_web_user in dummy_web_users:
        web_user_repository.create(
            dummy_web_user,
        )
    target_web_user = dummy_web_users[0]

    # Act
    result = web_user_repository.find(
        query={'user_code': target_web_user.user_code},
    )

    # Assert
    assert len(result) == 1
    assert isinstance(result[0], WebUser)
    assert type(result[0]._id) == ObjectId
    assert result[0].user_code == dummy_web_users[0].user_code
    assert result[0].name == dummy_web_users[0].name
    assert result[0].email == dummy_web_users[0].email
    assert result[0].linked_line_user_id == dummy_web_users[0].linked_line_user_id
    assert result[0].is_approved_line_user == dummy_web_users[0].is_approved_line_user
