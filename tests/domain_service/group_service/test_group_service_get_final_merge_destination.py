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


def test_not_merged_returns_itself(mocker):
    # Arrange
    mocker.patch.object(
        group_repository,
        "find",
        return_value=[_group("A", merged_into=None)],
    )

    # Act
    result = group_service.get_final_merge_destination("A")

    # Assert
    assert result == "A"


def test_single_merge_returns_destination(mocker):
    # Arrange: A→B
    mocker.patch.object(
        group_repository,
        "find",
        side_effect=[
            [_group("A", merged_into="B")],
            [_group("B", merged_into=None)],
        ],
    )

    # Act
    result = group_service.get_final_merge_destination("A")

    # Assert
    assert result == "B"


def test_chained_merge_returns_final_destination(mocker):
    """A→B→C と連鎖統合されている場合、Aを起点にすると最終到達点のCを返す(FEZ-58)"""
    # Arrange
    mocker.patch.object(
        group_repository,
        "find",
        side_effect=[
            [_group("A", merged_into="B")],
            [_group("B", merged_into="C")],
            [_group("C", merged_into=None)],
        ],
    )

    # Act
    result = group_service.get_final_merge_destination("A")

    # Assert
    assert result == "C"


def test_group_not_found_returns_itself(mocker):
    # Arrange
    mocker.patch.object(
        group_repository,
        "find",
        return_value=[],
    )

    # Act
    result = group_service.get_final_merge_destination("unknown")

    # Assert
    assert result == "unknown"


def test_does_not_loop_forever_on_corrupt_cycle(mocker):
    """merged_into が循環しているような不整合データがあっても無限ループしないことを確認する"""
    # Arrange: データ不整合により A が B に、B が A に統合されている(本来起こり得ない)
    mocker.patch.object(
        group_repository,
        "find",
        side_effect=[
            [_group("A", merged_into="B")],
            [_group("B", merged_into="A")],
        ],
    )

    # Act
    result = group_service.get_final_merge_destination("A")

    # Assert
    assert result == "B"
