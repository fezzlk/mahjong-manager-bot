from ApplicationService.ReplyService import ReplyService


def test_success():
    # Arrange
    reply_service = ReplyService()
    dummy_player_id_and_names = [
        {"name": "dummy_player1", "_id": "dummy_id1"},
        {"name": "dummy_player2", "_id": "dummy_id2"},
        {"name": "dummy_player3", "_id": "dummy_id3"},
        {"name": "dummy_player4", "_id": "dummy_id4"},
    ]

    # Act
    reply_service.add_tobi_menu(
        player_id_and_names=dummy_player_id_and_names,
    )

    # Assert
    assert len(reply_service.buttons) == 1
