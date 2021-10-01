from services.ReplyService import ReplyService
from tests.dummies import generate_dummy_points


def test_success():
    # Arrange
    reply_service = ReplyService()
    dummy_points = generate_dummy_points()

    # Act
    reply_service.add_submit_results_by_ocr_menu(
        results=dummy_points,
    )

    # Assert
    assert len(reply_service.buttons) == 1
