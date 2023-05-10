from tests.dummies import (
    generate_dummy_user_list,
    generate_dummy_group_list,
    generate_dummy_hanchan_list,
    generate_dummy_match_list,
)
# from repositories import (
#     group_setting_repository,
#     user_repository,
#     hanchan_repository,
#     group_repository,
#     match_repository,
#     session_scope,
# )
from mongo_client import mongo_client


class CreateDummyUseCase:
    def execute(self) -> None:
        
        users = generate_dummy_user_list()[:5]
        groups = generate_dummy_group_list()[:3]
        hanchans = generate_dummy_hanchan_list()[:7]
        matches = generate_dummy_match_list()[:5]
        for user in users:
            line_user_dict = user.__dict__.copy()
            if line_user_dict['_id'] is None:
                line_user_dict.pop('_id')
            mongo_client.db.line_users.insert_one(line_user_dict)


        # with session_scope() as session:
        #     for user in users:
        #         user_repository.create(session, user)
        #     for group in groups:
        #         group_repository.create(session, group)
        #     for config in configs:
        #         group_setting_repository.create(session, config)
        #     for match in matches:
        #         match_repository.create(session, match)
        #     for hanchan in hanchans:
        #         hanchan_repository.create(session, hanchan)
