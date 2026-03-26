from bson.objectid import ObjectId
from dummies import generate_dummy_group_setting_list

from domain_model.entities.group_setting import GroupSetting
from repositories import group_setting_repository


def test_create_new_record():
    # Arrange: DB は空
    dummy_setting = generate_dummy_group_setting_list()[0]

    # Act
    result = group_setting_repository.find_or_create(dummy_setting)

    # Assert: 新規作成されて返る
    assert isinstance(result, GroupSetting)
    assert type(result._id) is ObjectId
    assert result.line_group_id == dummy_setting.line_group_id
    assert result.rate == dummy_setting.rate

    record_on_db = group_setting_repository.find()
    assert len(record_on_db) == 1
    assert record_on_db[0].line_group_id == dummy_setting.line_group_id


def test_return_existing_record():
    # Arrange: 既存レコードを作成しておく
    dummy_setting = generate_dummy_group_setting_list()[1]
    created = group_setting_repository.create(dummy_setting)

    # Act: 同じ line_group_id で find_or_create を呼ぶ
    new_setting = GroupSetting(
        line_group_id=dummy_setting.line_group_id,
        rate=99,
    )
    result = group_setting_repository.find_or_create(new_setting)

    # Assert: 既存が返り、重複レコードが作られない
    assert isinstance(result, GroupSetting)
    assert result._id == created._id
    assert result.line_group_id == dummy_setting.line_group_id
    assert result.rate == dummy_setting.rate  # 元のレートのまま (setOnInsert)

    record_on_db = group_setting_repository.find()
    assert len(record_on_db) == 1
