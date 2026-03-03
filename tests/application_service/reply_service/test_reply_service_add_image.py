from application_service.reply_service import ReplyService


def test_success_a_message():
    # Arrange
    reply_service = ReplyService()
    dummy_image_url = "dummy_image_url"

    # Act
    reply_service.add_image(dummy_image_url)

    # Assert
    assert len(reply_service.images) == 1
    assert reply_service.images[0].type == "image"
    assert reply_service.images[0].original_content_url == dummy_image_url
    assert reply_service.images[0].preview_image_url == dummy_image_url


def test_success_messages():
    # Arrange
    reply_service = ReplyService()
    dummy_image_urls = [
        "dummy_image_url1",
        "dummy_image_url2",
        "dummy_image_url3",
    ]

    # Act
    for url in dummy_image_urls:
        reply_service.add_image(url)

    # Assert
    assert len(reply_service.images) == len(dummy_image_urls)
    for img, url in zip(reply_service.images, dummy_image_urls):
        assert img.type == "image"
        assert img.original_content_url == url
        assert img.preview_image_url == url
