from bson.objectid import ObjectId
from dummies import generate_dummy_user_list

from DomainModel.entities.User import User
from repositories import user_repository


def test_success_find_records():
    # Arrange
    dummy_users = generate_dummy_user_list()
    for dummy_user in dummy_users:
        user_repository.create(
            dummy_user,
        )

    # Act
    result = user_repository.find()

    # Assert
    assert len(result) == len(dummy_users)
    for i in range(len(result)):
        assert isinstance(result[i], User)
        assert type(result[i]._id) is ObjectId
        assert result[i].line_user_name == dummy_users[i].line_user_name
        assert result[i].line_user_id == dummy_users[i].line_user_id
        assert result[i].mode == dummy_users[i].mode
        assert result[i].jantama_name == dummy_users[i].jantama_name


def test_success_find_0_record():
    # Arrange
    # Do nothing

    # Act
    result = user_repository.find()

    # Assert
    assert len(result) == 0


def test_hit_1_record():
    # Arrange
    dummy_users = generate_dummy_user_list()[:3]
    for dummy_user in dummy_users:
        user_repository.create(
            dummy_user,
        )
    target_user = dummy_users[0]

    # Act
    result = user_repository.find(
        query={"line_user_id": target_user.line_user_id},
    )

    # Assert
    assert len(result) == 1
    assert isinstance(result[0], User)
    assert type(result[0]._id) is ObjectId
    assert result[0].line_user_name == target_user.line_user_name
    assert result[0].line_user_id == target_user.line_user_id
    assert result[0].mode == target_user.mode
    assert result[0].jantama_name == target_user.jantama_name
