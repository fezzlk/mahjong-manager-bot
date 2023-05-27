from use_cases.CreateDummyUseCase import CreateDummyUseCase
from repositories import (
    group_setting_repository,
    user_repository,
    hanchan_repository,
    group_repository,
    match_repository,
)


def test_create_dummy_use_case():
    # Act
    CreateDummyUseCase().execute()

    # Assert
    users = user_repository.find()
    groups = group_repository.find()
    groups_settings = group_setting_repository.find()
    matches = match_repository.find()
    hanchans = hanchan_repository.find()

    assert len(users) == 5
    assert len(groups) == 3
    assert len(groups_settings) == 2
    assert len(matches) == 5
    assert len(hanchans) == 5
