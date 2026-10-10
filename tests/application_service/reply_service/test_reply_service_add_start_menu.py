from application_service.reply_service import ReplyService


def test_success():
    # Arrange
    reply_service = ReplyService()

    # Act
    reply_service.add_start_menu()

    # Assert
    assert len(reply_service.buttons) == 1
    actions = reply_service.buttons[0].template.actions
    assert [(a.label, a.data) for a in actions] == [
        ("結果を入力", "_input"),
        ("精算", "_finish_confirm"),
        ("対戦管理", "_others"),
        ("設定", "_setting"),
    ]
