import pytest

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


def test_hit_1_record():
    # Arrange
    aliases = [_make_alias(str(i)) for i in range(3)]
    for a in aliases:
        command_alias_repository.create(a)
    target = aliases[0]

    # Act
    result = command_alias_repository.delete(
        query={"alias": target.alias},
    )

    # Assert
    assert result == 1
    records = command_alias_repository.find()
    assert len(records) == 2
    remaining_aliases = [r.alias for r in records]
    assert target.alias not in remaining_aliases


def test_hit_0_record():
    # Arrange
    aliases = [_make_alias(str(i)) for i in range(2)]
    for a in aliases:
        command_alias_repository.create(a)

    # Act
    result = command_alias_repository.delete(
        query={"alias": "nonexistent_alias"},
    )

    # Assert
    assert result == 0
    records = command_alias_repository.find()
    assert len(records) == 2


def test_fail_empty_query():
    """空クエリは ValueError を発生させる"""
    with pytest.raises(ValueError):
        command_alias_repository.delete(query={})


def test_fail_none_query():
    """None クエリは ValueError を発生させる"""
    with pytest.raises(ValueError):
        command_alias_repository.delete(query=None)
