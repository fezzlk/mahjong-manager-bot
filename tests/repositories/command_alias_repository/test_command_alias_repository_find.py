from bson.objectid import ObjectId

from domain_model.entities.command_alias import CommandAlias
from repositories import command_alias_repository


def _make_alias(suffix: str) -> CommandAlias:
    return CommandAlias(
        line_user_id=f"U_test_user_{suffix}",
        line_group_id="G_test_group_001",
        alias=f"alias_{suffix}",
        command=f"command_{suffix}",
        mentionees=[],
    )


def test_success_find_all():
    # Arrange
    aliases = [_make_alias(str(i)) for i in range(3)]
    for a in aliases:
        command_alias_repository.create(a)

    # Act
    result = command_alias_repository.find()

    # Assert
    assert len(result) == 3
    for r in result:
        assert isinstance(r, CommandAlias)
        assert type(r._id) is ObjectId


def test_hit_0_record():
    # Arrange
    aliases = [_make_alias(str(i)) for i in range(2)]
    for a in aliases:
        command_alias_repository.create(a)

    # Act
    result = command_alias_repository.find(query={"line_user_id": "U_nonexistent"})

    # Assert
    assert len(result) == 0


def test_hit_1_record():
    # Arrange
    aliases = [_make_alias(str(i)) for i in range(3)]
    for a in aliases:
        command_alias_repository.create(a)
    target = aliases[0]

    # Act
    result = command_alias_repository.find(query={"alias": target.alias})

    # Assert
    assert len(result) == 1
    assert isinstance(result[0], CommandAlias)
    assert result[0].alias == target.alias
    assert result[0].line_user_id == target.line_user_id


def test_find_empty_collection():
    # Act
    result = command_alias_repository.find()

    # Assert
    assert result == []
