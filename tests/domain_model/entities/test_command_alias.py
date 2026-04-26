from datetime import datetime

from bson.objectid import ObjectId

from domain_model.entities.command_alias import CommandAlias


def test_success():
    # Arrange
    oid = ObjectId()

    # Act
    alias = CommandAlias(
        line_user_id="U_test_user_001",
        line_group_id="G_test_group_001",
        alias="test_alias",
        command="test_command",
        mentionees=["U_mention_001", "U_mention_002"],
        _id=oid,
        created_at=datetime(2022, 1, 2, 3, 4, 5),
        updated_at=datetime(2023, 1, 2, 3, 4, 5),
    )

    # Assert
    assert alias._id == oid
    assert alias.line_user_id == "U_test_user_001"
    assert alias.line_group_id == "G_test_group_001"
    assert alias.alias == "test_alias"
    assert alias.command == "test_command"
    assert alias.mentionees == ["U_mention_001", "U_mention_002"]
    assert alias.created_at == datetime(2022, 1, 2, 3, 4, 5)
    assert alias.updated_at == datetime(2023, 1, 2, 3, 4, 5)


def test_success_default():
    # Act
    alias = CommandAlias(line_user_id="U_test_user_002")

    # Assert
    assert alias._id is None
    assert alias.line_user_id == "U_test_user_002"
    assert alias.line_group_id is None
    assert alias.alias is None
    assert alias.command is None
    assert alias.mentionees == []
    assert alias.created_at.date() == datetime.now().date()
    assert alias.updated_at.date() == datetime.now().date()


def test_success_none_timestamps_filled_by_post_init():
    """__post_init__ が None の created_at/updated_at を datetime.now() で補完する"""
    alias = CommandAlias(
        line_user_id="U_test_user_003",
        created_at=None,
        updated_at=None,
    )

    assert alias.created_at is not None
    assert alias.updated_at is not None
    assert alias.created_at.date() == datetime.now().date()
    assert alias.updated_at.date() == datetime.now().date()
