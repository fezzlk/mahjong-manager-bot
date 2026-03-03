from application_service.reply_service import ReplyService


def test_success_a_message():
    # Arrange
    reply_service = ReplyService()
    dummy_text = "dummy_text"

    # Act
    reply_service.add_message(dummy_text)

    # Assert
    assert len(reply_service.texts) == 1
    assert reply_service.texts[0].type == "text"
    assert reply_service.texts[0].text == dummy_text


def test_success_messages():
    # Arrange
    reply_service = ReplyService()
    dummy_texts = [
        "dummy_text1",
        "dummy_text2",
        "dummy_text3",
    ]

    # Act
    for text in dummy_texts:
        reply_service.add_message(text)

    # Assert
    assert len(reply_service.texts) == len(dummy_texts)
    for msg, expected_text in zip(reply_service.texts, dummy_texts):
        assert msg.type == "text"
        assert msg.text == expected_text
