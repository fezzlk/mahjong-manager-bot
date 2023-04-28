from tests.dummies import (
    generate_dummy_hanchan_list,
    generate_dummy_match_list,
)
from repositories import hanchan_repository, match_repository


def test_hit_with_ids():
    # Arrange
    dummy_matches = generate_dummy_match_list()[:3]
    for dummy_match in dummy_matches:
        match_repository.create(
            dummy_match,
        )
    dummy_hanchans = generate_dummy_hanchan_list()[:3]
    for dummy_hanchan in dummy_hanchans:
        hanchan_repository.create(
            dummy_hanchan,
        )
    target_hanchans = dummy_hanchans[1:3]
    ids = [target_hanchan._id for target_hanchan in target_hanchans]

    # Act
    result = hanchan_repository.delete(
        query={'_id': {'$in': ids}},
    )

    # Assert
    assert result == len(ids)


def test_hit_0_record():
    # Arrange
    dummy_matches = generate_dummy_match_list()[:3]
    for dummy_match in dummy_matches:
        match_repository.create(
            dummy_match,
        )
    dummy_hanchans = generate_dummy_hanchan_list()[:3]
    for dummy_hanchan in dummy_hanchans:
        hanchan_repository.create(
            dummy_hanchan,
        )

    # Act
    result = hanchan_repository.delete(
        query={'_id': {'$in': [4, 5]}},
    )

    # Assert
    assert result == 0
