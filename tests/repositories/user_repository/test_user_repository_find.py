from bson.objectid import ObjectId
from dummies import generate_dummy_user_list

from domain_model.entities.user import User
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
    for i, _item in enumerate(result):
        assert isinstance(_item, User)
        assert type(_item._id) is ObjectId
        assert _item.line_user_name == dummy_users[i].line_user_name
        assert _item.line_user_id == dummy_users[i].line_user_id
        assert _item.mode == dummy_users[i].mode
        assert _item.jantama_name == dummy_users[i].jantama_name


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
