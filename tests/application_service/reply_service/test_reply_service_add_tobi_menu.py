from application_service.reply_service import ReplyService


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
        match_id="dummy_match_id",
        hanchan_id="dummy_hanchan_id",
    )

    # Assert
    assert len(reply_service.buttons) == 1
    # どの半荘に対するボタンかが data に埋め込まれている(FEZ-225)
    actions = reply_service.buttons[0].template.actions
    assert actions[0].data == "_tobi?m=dummy_match_id&h=dummy_hanchan_id dummy_id1"
    assert actions[-1].data == "_tobi?m=dummy_match_id&h=dummy_hanchan_id"
