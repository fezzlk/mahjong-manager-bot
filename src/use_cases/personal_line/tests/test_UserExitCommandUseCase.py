# from use_cases.personal_line.UserExitCommandUseCase import (
#     UserExitCommandUseCase,
# )
# from DomainModel.entities.User import User, UserMode
# from ApplicationService import (
#     reply_service,
# )
# from repositories import (
#     session_scope,
#     user_repository,
# )

# dummy_user = User(
#     line_user_name="test_user1",
#     line_user_id="U0123456789abcdefghijklmnopqrstu1",
#     mode=UserMode.wait.value,
#     jantama_name="jantama_user1",
#     matches=[],
#     _id=1,
# )


# def test_execute():
#     # Arrage
#     with session_scope() as session:
#         user_repository.create(session, dummy_user)

#     use_case = UserExitCommandUseCase()

#     # Act
#     use_case.execute(line_user_id=dummy_user.line_user_id)

#     # Assert
#     with session_scope() as session:
#         user = user_repository.find(session)[0]
#         assert user.mode == UserMode.wait.value

#     assert len(reply_service.texts) == 1
