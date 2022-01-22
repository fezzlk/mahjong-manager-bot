from Services.ReplyService import ReplyService


def test_success_a_message():
    # Arrange
    reply_service = ReplyService()
    dummy_image_url = 'dummy_image_url'

    # Act
    reply_service.add_image(dummy_image_url)

    # Assert
    assert len(reply_service.images) == 1
    assert reply_service.images[0].type == 'image'
    assert reply_service.images[0].original_content_url == dummy_image_url
    assert reply_service.images[0].preview_image_url == dummy_image_url


def test_success_messages():
    # Arrange
    reply_service = ReplyService()
    dummy_image_urls = [
        'dummy_image_url1',
        'dummy_image_url2',
        'dummy_image_url3',
    ]

    # Act
    for i in range(len(dummy_image_urls)):
        reply_service.add_image(dummy_image_urls[i])

    # Assert
    assert len(reply_service.images) == len(dummy_image_urls)
    for i in range(len(reply_service.images)):
        assert reply_service.images[i].type == 'image'
        assert reply_service.images[i].original_content_url == dummy_image_urls[i]
        assert reply_service.images[i].preview_image_url == dummy_image_urls[i]
