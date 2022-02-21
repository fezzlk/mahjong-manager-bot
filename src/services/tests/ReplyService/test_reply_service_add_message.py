from services.ReplyService import ReplyService


def test_success_a_message():
    # Arrange
    reply_service = ReplyService()
    dummy_text = 'dummy_text'

    # Act
    reply_service.add_message(dummy_text)

    # Assert
    assert len(reply_service.texts) == 1
    assert reply_service.texts[0].type == 'text'
    assert reply_service.texts[0].text == dummy_text


def test_success_messages():
    # Arrange
    reply_service = ReplyService()
    dummy_texts = [
        'dummy_text1',
        'dummy_text2',
        'dummy_text3',
    ]

    # Act
    for i in range(len(dummy_texts)):
        reply_service.add_message(dummy_texts[i])

    # Assert
    assert len(reply_service.texts) == len(dummy_texts)
    for i in range(len(reply_service.texts)):
        assert reply_service.texts[i].type == 'text'
        assert reply_service.texts[i].text == dummy_texts[i]
