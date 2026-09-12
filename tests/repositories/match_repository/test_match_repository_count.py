from dummies import generate_dummy_match_list

from repositories import match_repository


def test_counts_only_non_deleted_records():
    # Arrange
    dummy_matches = generate_dummy_match_list()
    for dummy_match in dummy_matches:
        match_repository.create(dummy_match)

    # Act
    result = match_repository.count()

    # Assert: dummy_matches[1]はis_deleted=Trueのため除外される
    assert result == 2


def test_count_with_query():
    # Arrange
    dummy_matches = generate_dummy_match_list()
    for dummy_match in dummy_matches:
        match_repository.create(dummy_match)

    # Act
    result = match_repository.count(
        query={"line_group_id": dummy_matches[0].line_group_id},
    )

    # Assert
    assert result == 2


def test_count_0_with_no_match():
    # Arrange
    # Do nothing

    # Act
    result = match_repository.count()

    # Assert
    assert result == 0
