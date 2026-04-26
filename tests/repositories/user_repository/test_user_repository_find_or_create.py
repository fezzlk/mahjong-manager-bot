from bson.objectid import ObjectId
from dummies import generate_dummy_user_list

from domain_model.entities.user import User, UserMode
from repositories import user_repository


def test_create_new_record():
    # Arrange: DB は空
    dummy_user = generate_dummy_user_list()[0]

    # Act
    result = user_repository.find_or_create(dummy_user)

    # Assert: 新規作成されて返る
    assert isinstance(result, User)
    assert type(result._id) is ObjectId
    assert result.line_user_id == dummy_user.line_user_id
    assert result.line_user_name == dummy_user.line_user_name

    record_on_db = user_repository.find()
    assert len(record_on_db) == 1
    assert record_on_db[0].line_user_id == dummy_user.line_user_id


def test_return_existing_record():
    # Arrange: 既存レコードを作成しておく
    dummy_user = generate_dummy_user_list()[1]
    created = user_repository.create(dummy_user)

    # Act: 同じ line_user_id で find_or_create を呼ぶ
    new_user = User(
        line_user_id=dummy_user.line_user_id,
        line_user_name="updated_name",
        mode=UserMode.wait.value,
    )
    result = user_repository.find_or_create(new_user)

    # Assert: 既存が返り、重複レコードが作られない
    assert isinstance(result, User)
    assert result._id == created._id
    assert result.line_user_id == dummy_user.line_user_id
    assert result.line_user_name == dummy_user.line_user_name  # 元の名前のまま (setOnInsert)

    record_on_db = user_repository.find()
    assert len(record_on_db) == 1
