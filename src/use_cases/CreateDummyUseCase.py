from tests.dummies import (
    generate_dummy_user_list,
    generate_dummy_web_user_list,
    generate_dummy_group_list,
    generate_dummy_hanchan_list,
    generate_dummy_match_list,
    generate_dummy_group_setting_list,
)
from repositories import (
    group_setting_repository,
    user_repository,
    web_user_repository,
    hanchan_repository,
    group_repository,
    match_repository,
)


class CreateDummyUseCase:
    def execute(self) -> None:
        
        users = generate_dummy_user_list()[:10]
        web_users = generate_dummy_web_user_list()[:4]
        groups = generate_dummy_group_list()[:5]
        group_settings = generate_dummy_group_setting_list()[:3]
        hanchans = generate_dummy_hanchan_list()[:7]
        matches = generate_dummy_match_list()[:6]

        for user in users:
            user_repository.create(user)
        for web_user in web_users:
            web_user_repository.create(web_user)
        for group in groups:
            group_repository.create(group)
        for group_setting in group_settings:
            group_setting_repository.create(group_setting)
        for match in matches:
            match_repository.create(match)
        for hanchan in hanchans:
            hanchan_repository.create(hanchan)
