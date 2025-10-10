from DomainModel.entities.User import User
from repositories import user_repository
from tests.dummies import generate_dummy_user_list


def test_hit_1_record():
    # Arrange
    dummy_users = generate_dummy_user_list()[:3]
    for dummy_user in dummy_users:
        user_repository.create(
            dummy_user,
        )
    other_users = dummy_users[:2]
    target_line_user_id = dummy_users[2].line_user_id

    # Act
    result = user_repository.delete(
        query={"line_user_id": target_line_user_id},
    )

    # Assert
    assert result == 1
    record_on_db = user_repository.find()
    assert len(record_on_db) == len(other_users)
    for i in range(len(record_on_db)):
        assert isinstance(record_on_db[i], User)
        assert record_on_db[i]._id == other_users[i]._id
        assert record_on_db[i].line_user_name == other_users[i].line_user_name
        assert record_on_db[i].line_user_id == other_users[i].line_user_id
        assert record_on_db[i].mode == other_users[i].mode
        assert record_on_db[i].jantama_name == other_users[i].jantama_name


def test_hit_0_record():
    # Arrange
    dummy_users = generate_dummy_user_list()[:3]
    for dummy_user in dummy_users:
        user_repository.create(
            dummy_user,
        )
    target_groups = generate_dummy_user_list()[3:6]
    ids = [target_group._id for target_group in target_groups]

    # Act
    result = user_repository.delete(
        query={"_id": {"$in": ids}},
    )

    # Assert
    assert result == 0
    record_on_db = user_repository.find()
    assert len(record_on_db) == len(dummy_users)
    for i in range(len(record_on_db)):
        assert isinstance(record_on_db[i], User)
        assert record_on_db[i].line_user_name == dummy_users[i].line_user_name
        assert record_on_db[i].line_user_id == dummy_users[i].line_user_id
        assert record_on_db[i].mode == dummy_users[i].mode
        assert record_on_db[i].jantama_name == dummy_users[i].jantama_name
