from bson.objectid import ObjectId
from dummies import generate_dummy_group_list

from domain_model.entities.group import Group, GroupMode
from repositories import group_repository


def test_create_new_record():
    # Arrange: DB は空
    dummy_group = generate_dummy_group_list()[0]

    # Act
    result = group_repository.find_or_create(dummy_group)

    # Assert: 新規作成されて返る
    assert isinstance(result, Group)
    assert type(result._id) is ObjectId
    assert result.line_group_id == dummy_group.line_group_id
    assert result.mode == dummy_group.mode

    record_on_db = group_repository.find()
    assert len(record_on_db) == 1
    assert record_on_db[0].line_group_id == dummy_group.line_group_id


def test_return_existing_record():
    # Arrange: 既存レコードを作成しておく
    dummy_group = generate_dummy_group_list()[1]
    created = group_repository.create(dummy_group)

    # Act: 同じ line_group_id で find_or_create を呼ぶ
    new_group = Group(
        line_group_id=dummy_group.line_group_id,
        mode=GroupMode.input.value,
    )
    result = group_repository.find_or_create(new_group)

    # Assert: 既存が返り、重複レコードが作られない
    assert isinstance(result, Group)
    assert result._id == created._id
    assert result.line_group_id == dummy_group.line_group_id
    assert result.mode == dummy_group.mode  # 元のモードのまま (setOnInsert)

    record_on_db = group_repository.find()
    assert len(record_on_db) == 1
