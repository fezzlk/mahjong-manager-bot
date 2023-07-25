from tests.dummies import (
    generate_dummy_join_event,
)
from use_cases.common_line.ReplyGitHubUrlUseCase import ReplyGitHubUrlUseCase
from ApplicationService import (
    request_info_service,
    reply_service
)


def test_execute():
    # Arrange
    dummy_event = generate_dummy_join_event()
    request_info_service.set_req_info(event=dummy_event)

    use_case = ReplyGitHubUrlUseCase()

    # Act
    use_case.execute()

    # Assert
    assert len(reply_service.texts) == 1
    assert reply_service.texts[0].text == 'https://github.com/bbladr/mahjong-manager-bot'
