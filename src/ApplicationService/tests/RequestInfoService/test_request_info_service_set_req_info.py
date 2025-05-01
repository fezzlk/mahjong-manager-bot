from ApplicationService.RequestInfoService import RequestInfoService
from tests.dummies import (
    generate_dummy_follow_event,
)
from line_models.Event import Event


def test_follow_event():
    # Arrange
    request_info_service = RequestInfoService()
    follow_event = generate_dummy_follow_event()

    # Act
    request_info_service.set_req_info(follow_event)

    # Assert
    assert request_info_service.req_line_user_id == follow_event.source.user_id


def test_message_event_from_user():
    # Arrange
    request_info_service = RequestInfoService()
    message_event = Event(
        type='message',
        source_type='user',
        user_id='U0123456789abcdefghijklmnopqrstu1',
        message_type='text',
        text='dummy_text',
    )

    # Act
    request_info_service.set_req_info(message_event)

    # Assert
    assert request_info_service.req_line_user_id == message_event.source.user_id
    assert request_info_service.req_line_group_id is None
    assert request_info_service.mention_line_ids == []
    assert request_info_service.message == 'dummy_text'
    assert request_info_service.method is None
    assert request_info_service.params == {}
    assert request_info_service.body is None


def test_postback_event_from_user():
    # Arrange
    request_info_service = RequestInfoService()
    message_event = Event(
        type='postback',
        source_type='user',
        user_id='U0123456789abcdefghijklmnopqrstu1',
        message_type='text',
        text='dummy_text',
        postback_data='dummy_postback',
    )

    # Act
    request_info_service.set_req_info(message_event)

    # Assert
    assert request_info_service.req_line_user_id == message_event.source.user_id
    assert request_info_service.req_line_group_id is None
    assert request_info_service.mention_line_ids == []
    assert request_info_service.message == 'dummy_postback'
    assert request_info_service.method is None
    assert request_info_service.params == {}
    assert request_info_service.body is None


def test_message_event_from_room(mocker):
    # Arrange
    from ApplicationService import reply_service
    mock = mocker.patch.object(reply_service, 'push_a_message')
    request_info_service = RequestInfoService()
    message_event = Event(
        type='message',
        source_type='room',
        user_id='U0123456789abcdefghijklmnopqrstu1',
        group_id='G0123456789abcdefghijklmnopqrstu1',
        message_type='text',
        text='dummy_text',
    )
    # Act
    request_info_service.set_req_info(message_event)

    # Assert
    assert request_info_service.req_line_user_id == message_event.source.user_id
    assert request_info_service.req_line_group_id == message_event.source.room_id
    assert request_info_service.mention_line_ids == []
    assert request_info_service.message == 'dummy_text'
    assert request_info_service.method is None
    assert request_info_service.params == {}
    assert request_info_service.body is None
    mock.assert_called_once()


def test_message_event_from_group():
    # Arrange
    request_info_service = RequestInfoService()
    message_event = Event(
        type='message',
        source_type='group',
        user_id='U0123456789abcdefghijklmnopqrstu1',
        group_id='G0123456789abcdefghijklmnopqrstu1',
        message_type='text',
        text='dummy_text',
    )
    # Act
    request_info_service.set_req_info(message_event)

    # Assert
    assert request_info_service.req_line_user_id == message_event.source.user_id
    assert request_info_service.req_line_group_id == message_event.source.group_id
    assert request_info_service.mention_line_ids == []
    assert request_info_service.message == 'dummy_text'
    assert request_info_service.method is None
    assert request_info_service.params == {}
    assert request_info_service.body is None


def test_postback_event_from_group():
    # Arrange
    request_info_service = RequestInfoService()
    message_event = Event(
        type='postback',
        source_type='group',
        user_id='U0123456789abcdefghijklmnopqrstu1',
        group_id='G0123456789abcdefghijklmnopqrstu1',
        message_type='text',
        text='dummy_text',
        postback_data='dummy_postback',
    )

    # Act
    request_info_service.set_req_info(message_event)
    # Assert
    assert request_info_service.req_line_user_id == message_event.source.user_id
    assert request_info_service.req_line_group_id == message_event.source.group_id
    assert request_info_service.mention_line_ids == []
    assert request_info_service.message == 'dummy_postback'
    assert request_info_service.method is None
    assert request_info_service.params == {}
    assert request_info_service.body is None


# def test_message_event_from_group_with_mention():
#     # Arrange
#     request_info_service = RequestInfoService()
#     message_event = Event(
#         type='message',
#         source_type='group',
#         user_id='U0123456789abcdefghijklmnopqrstu1',
#         group_id='G0123456789abcdefghijklmnopqrstu1',
#         message_type='text',
#         text='dummy_text',
#         mention_ids=['U0123456789abcdefghijklmnopqrstu2', 'U0123456789abcdefghijklmnopqrstu3']
#     )
#     # Act
#     request_info_service.set_req_info(message_event)

#     # Assert
#     assert request_info_service.req_line_user_id == message_event.source.user_id
#     assert request_info_service.req_line_group_id == message_event.source.group_id
#     assert request_info_service.mention_line_ids ==
#     ['U0123456789abcdefghijklmnopqrstu2', 'U0123456789abcdefghijklmnopqrstu3']
#     assert request_info_service.message == 'dummy_text'
#     assert request_info_service.method is None
#     assert request_info_service.params == {}
#     assert request_info_service.body is None
