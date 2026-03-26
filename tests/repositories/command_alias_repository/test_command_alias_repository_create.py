from bson.objectid import ObjectId

from domain_model.entities.command_alias import CommandAlias
from repositories import command_alias_repository


def _make_alias(suffix: str = "001") -> CommandAlias:
    return CommandAlias(
        line_user_id=f"U_test_user_{suffix}",
        line_group_id=f"G_test_group_{suffix}",
        alias=f"alias_{suffix}",
        command=f"command_{suffix}",
        mentionees=[],
    )


def test_success():
    # Arrange
    alias = _make_alias("001")

    # Act
    result = command_alias_repository.create(alias)

    # Assert
    assert isinstance(result, CommandAlias)
    assert type(result._id) is ObjectId
    assert result.line_user_id == alias.line_user_id
    assert result.alias == alias.alias

    records = command_alias_repository.find()
    assert len(records) == 1
    assert records[0].line_user_id == alias.line_user_id


def test_success_with_id():
    """_id 指定時はその ObjectId で作成される"""
    oid = ObjectId("644c838186bbd9e20a91b783")
    alias = _make_alias("002")
    alias._id = oid

    result = command_alias_repository.create(alias)

    assert result._id == oid
    records = command_alias_repository.find()
    assert len(records) == 1
    assert records[0]._id == oid


def test_success_duplicate_allowed():
    """command_alias_repository は重複チェックなし — 同一 alias を2件 insert できる"""
    alias1 = _make_alias("003")
    alias2 = _make_alias("003")  # 同じ alias でも重複エラーにならない

    command_alias_repository.create(alias1)
    command_alias_repository.create(alias2)

    records = command_alias_repository.find()
    assert len(records) == 2
