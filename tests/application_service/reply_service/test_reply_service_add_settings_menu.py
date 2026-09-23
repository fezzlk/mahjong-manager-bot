from linebot.v3.messaging import FlexButton, FlexMessage

from application_service.reply_service import ReplyService


def _button_data(flex_message):
    return [
        c.action.data
        for bubble in flex_message.contents.contents
        for c in bubble.body.contents
        if isinstance(c, FlexButton)
    ]


def test_success():
    # Arrange
    reply_service = ReplyService()

    # Act
    reply_service.add_settings_menu()

    # Assert: 設定メニューはFlexCarousel 1通に全項目が並ぶ
    assert len(reply_service.buttons) == 1
    message = reply_service.buttons[0]
    assert isinstance(message, FlexMessage)
    assert _button_data(message) == [
        "_setting レート",
        "_setting 順位点",
        "_setting チップ",
        "_setting 飛び賞",
        "_setting 端数計算方法",
        "_setting 人数",
        "_setting ゲスト",
        "_migrate",
        "_help",
    ]


def test_legacy_page_keys_return_same_carousel():
    """旧ButtonsTemplateのページ切替ボタンが履歴から押されても同じカルーセルを返す。"""
    for key in ["メニュー1", "メニュー2"]:
        reply_service = ReplyService()
        reply_service.add_settings_menu(key)
        assert len(reply_service.buttons) == 1
        assert isinstance(reply_service.buttons[0], FlexMessage)


def test_success_key_num_of_players():
    # Arrange
    reply_service = ReplyService()

    # Act
    reply_service.add_settings_menu("人数")

    # Assert
    assert len(reply_service.texts) == 1
    items = reply_service.texts[0].quick_reply.items
    assert [i.action.data for i in items] == ["_update_config 人数 4", "_update_config 人数 3"]


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
