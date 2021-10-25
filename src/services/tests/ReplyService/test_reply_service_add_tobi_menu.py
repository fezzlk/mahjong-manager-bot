from services.ReplyService import ReplyService


def test_success():
    # Arrange
    reply_service = ReplyService()
    dummy_player_id_and_names = [
        {'line_name': 'dummy_player1', 'id': 'dummy_id1'},
        {'line_name': 'dummy_player2', 'id': 'dummy_id2'},
        {'line_name': 'dummy_player3', 'id': 'dummy_id3'},
        {'line_name': 'dummy_player4', 'id': 'dummy_id4'},
    ]

    # Act
    reply_service.add_tobi_menu(
        player_id_and_names=dummy_player_id_and_names,
    )

    # Assert
    assert len(reply_service.buttons) == 1
