from domain_model.entities.group import Group, GroupMode
from domain_service import (
    group_service,
)
from repositories import group_repository


def _group(line_group_id: str, merged_into: str = None) -> Group:
    return Group(
        line_group_id=line_group_id,
        mode=GroupMode.wait.value,
        merged_into=merged_into,
    )


def test_no_merged_groups(mocker):
    # Arrange
    mock_find = mocker.patch.object(
        group_repository,
        "find",
        return_value=[],
    )

    # Act
    result = group_service.get_effective_line_group_ids("C")

    # Assert
    assert result == ["C"]
    mock_find.assert_called_once_with({"merged_into": {"$in": ["C"]}})


def test_single_level_merge(mocker):
    # Arrange: B が C に統合されている
    mocker.patch.object(
        group_repository,
        "find",
        side_effect=[
            [_group("B", merged_into="C")],
            [],
        ],
    )

    # Act
    result = group_service.get_effective_line_group_ids("C")

    # Assert
    assert result == ["C", "B"]


def test_chained_merge_includes_grandparent(mocker):
    """A→B→C と連鎖統合された場合、Cから見てAも含まれることを確認する(FEZ-58)"""
    # Arrange: A が B に、B が C に統合されている
    mocker.patch.object(
        group_repository,
        "find",
        side_effect=[
            [_group("B", merged_into="C")],
            [_group("A", merged_into="B")],
            [],
        ],
    )

    # Act
    result = group_service.get_effective_line_group_ids("C")

    # Assert
    assert result == ["C", "B", "A"]


def test_multiple_groups_merged_into_same_target(mocker):
    # Arrange: B と D がどちらも C に統合されている
    mocker.patch.object(
        group_repository,
        "find",
        side_effect=[
            [_group("B", merged_into="C"), _group("D", merged_into="C")],
            [],
        ],
    )

    # Act
    result = group_service.get_effective_line_group_ids("C")

    # Assert
    assert result == ["C", "B", "D"]


def test_does_not_loop_forever_on_corrupt_cycle(mocker):
    """merged_into が循環しているような不整合データがあっても無限ループしないことを確認する"""
    # Arrange: データ不整合により A が B に、B が A に統合されている(本来起こり得ない)
    mocker.patch.object(
        group_repository,
        "find",
        side_effect=[
            [_group("B", merged_into="A")],
            [_group("A", merged_into="B")],
        ],
    )

    # Act
    result = group_service.get_effective_line_group_ids("A")

    # Assert
    assert result == ["A", "B"]
