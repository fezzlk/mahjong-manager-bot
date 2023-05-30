from use_cases.CreateDummyUseCase import CreateDummyUseCase
from repositories import (
    group_setting_repository,
    user_repository,
    web_user_repository,
    hanchan_repository,
    group_repository,
    match_repository,
)


def test_create_dummy_use_case():
    # Act
    CreateDummyUseCase().execute()

    # Assert
    users = user_repository.find()
    web_users = web_user_repository.find()
    groups = group_repository.find()
    groups_settings = group_setting_repository.find()
    matches = match_repository.find()
    hanchans = hanchan_repository.find()

    assert len(users) == 10
    assert len(web_users) == 4
    assert len(groups) == 5
    assert len(groups_settings) == 3
    assert len(hanchans) == 7
    assert len(matches) == 6
