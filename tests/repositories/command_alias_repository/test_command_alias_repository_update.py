from domain_model.entities.command_alias import CommandAlias
from repositories import command_alias_repository


def _make_alias(alias_str: str = "test_alias") -> CommandAlias:
    return CommandAlias(
        line_user_id="U_test_user_001",
        line_group_id="G_test_group_001",
        alias=alias_str,
        command="test_command",
        mentionees=[],
    )


def test_hit_1_record():
    # Arrange
    alias = _make_alias("before_alias")
    command_alias_repository.create(alias)

    # Act
    result = command_alias_repository.update(
        query={"alias": "before_alias"},
        new_values={"alias": "after_alias"},
    )

    # Assert
    assert result == 1
    records = command_alias_repository.find()
    assert len(records) == 1
    assert records[0].alias == "after_alias"


def test_hit_0_record():
    # Arrange (DB is empty)

    # Act
    result = command_alias_repository.update(
        query={"alias": "nonexistent_alias"},
        new_values={"alias": "new_alias"},
    )

    # Assert
    assert result == 0
    records = command_alias_repository.find()
    assert len(records) == 0
