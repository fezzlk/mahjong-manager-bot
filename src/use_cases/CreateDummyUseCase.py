from tests.dummies import (
    generate_dummy_user_list,
    generate_dummy_group_list,
    generate_dummy_hanchan_list,
    generate_dummy_match_list,
    generate_dummy_group_setting_list,
)
from repositories import (
    group_setting_repository,
    user_repository,
    hanchan_repository,
    group_repository,
    match_repository,
)


class CreateDummyUseCase:
    def execute(self) -> None:
        
        users = generate_dummy_user_list()[:5]
        groups = generate_dummy_group_list()[:3]
        group_settings = generate_dummy_group_setting_list()[:2]
        hanchans = generate_dummy_hanchan_list()[:5]
        matches = generate_dummy_match_list()[:5]

        for user in users:
            user_repository.create(user)
        for group in groups:
            group_repository.create(group)
        for group_setting in group_settings:
            group_setting_repository.create(group_setting)
        for match in matches:
            match_repository.create(match)
        for hanchan in hanchans:
            hanchan_repository.create(hanchan)
