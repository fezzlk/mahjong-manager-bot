from dummies import (
    generate_dummy_unfollow_event,
    generate_dummy_user_list,
)

from application_service import (
    request_info_service,
)
from repositories import UserRepository
from use_cases.personal_line.unfollow_use_case import UnfollowUseCase


def test_execute():
    # 目的: test_execute の挙動を検証する。
    # 入力: なし
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: result の件数が 0 件
    # reply_service: なし
    # DB操作: user_repository.create(dummy_user); result = user_repository.find()
    # Arrange
    dummy_event = generate_dummy_unfollow_event()
    request_info_service.set_req_info(event=dummy_event)

    dummy_user = generate_dummy_user_list()[0]
    user_repository = UserRepository()
    user_repository.create(dummy_user)

    use_case = UnfollowUseCase()

    # Act
    use_case.execute()

    # Assert
    result = user_repository.find()
    assert len(result) == 0
