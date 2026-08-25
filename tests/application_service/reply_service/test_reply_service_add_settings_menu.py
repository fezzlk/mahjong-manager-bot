from application_service.reply_service import ReplyService


def test_success():
    # Arrange
    reply_service = ReplyService()

    # Act
    reply_service.add_settings_menu()

    # Assert
    assert len(reply_service.buttons) == 1


def test_success_menu2():
    # Arrange
    reply_service = ReplyService()

    # Act
    reply_service.add_settings_menu("メニュー2")

    # Assert
    assert len(reply_service.buttons) == 1
    # LINE ButtonsTemplate は最大4アクションのため、追加した「持ち点」込みで4件に収まること
    assert len(reply_service.buttons[0].template.actions) == 4


def test_success_key_rate():
    # Arrange
    reply_service = ReplyService()

    # Act
    reply_service.add_settings_menu("レート")

    # Assert: Quick Reply で返るため texts に追加される
    assert len(reply_service.texts) == 1
    assert reply_service.texts[0].quick_reply is not None
    # なし + 点1~5 + 点10 = 7 items
    assert len(reply_service.texts[0].quick_reply.items) == 7


def test_success_key_chip():
    # Arrange
    reply_service = ReplyService()

    # Act
    reply_service.add_settings_menu("チップ")

    # Assert
    assert len(reply_service.buttons) == 1


def test_success_key_ranking_point():
    # Arrange
    reply_service = ReplyService()

    # Act
    reply_service.add_settings_menu("順位点")

    # Assert
    assert len(reply_service.buttons) == 1
    # 4人麻雀用の2パターンが選択肢になっていること
    actions = reply_service.buttons[0].template.actions
    assert len(actions) == 2
    assert actions[0].data == "_update_config 順位点 20,10,-10,-20"


def test_success_key_ranking_point_three_players():
    """num_of_players=3 を渡すと3人麻雀用の順位点パターンが選択肢になること(FEZ-126)。"""
    # Arrange
    reply_service = ReplyService()

    # Act
    reply_service.add_settings_menu("順位点", num_of_players=3)

    # Assert
    assert len(reply_service.buttons) == 1
    actions = reply_service.buttons[0].template.actions
    assert len(actions) == 2
    assert actions[0].data == "_update_config 順位点 30,0,-30"
    assert actions[1].data == "_update_config 順位点 15,0,-15"


def test_success_key_starting_points():
    """持ち点設定のクイックリプライ/ボタンが返ること(FEZ-126)。"""
    # Arrange
    reply_service = ReplyService()

    # Act
    reply_service.add_settings_menu("持ち点")

    # Assert
    assert len(reply_service.buttons) == 1
    actions = reply_service.buttons[0].template.actions
    assert [a.data for a in actions] == [
        "_update_config 持ち点 25000",
        "_update_config 持ち点 30000",
        "_update_config 持ち点 35000",
        "_update_config 持ち点 40000",
    ]


def test_success_key_tobi_bonus():
    # Arrange
    reply_service = ReplyService()

    # Act
    reply_service.add_settings_menu("飛び賞")

    # Assert
    assert len(reply_service.buttons) == 1


def test_success_key_calculate_method1():
    # Arrange
    reply_service = ReplyService()

    # Act
    reply_service.add_settings_menu("端数計算方法")

    # Assert
    assert len(reply_service.buttons) == 1


def test_success_key_calculate_method2():
    # Arrange
    reply_service = ReplyService()

    # Act
    reply_service.add_settings_menu(key="端数計算方法2")

    # Assert
    assert len(reply_service.buttons) == 1
