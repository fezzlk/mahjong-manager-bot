from services.ReplyService import ReplyService


def test_success():
    # Arrange
    reply_service = ReplyService()

    # Act
    reply_service.add_settings_menu()

    # Assert
    assert len(reply_service.buttons) == 1


def test_success_key_rate():
    # Arrange
    reply_service = ReplyService()

    # Act
    reply_service.add_settings_menu('レート')

    # Assert
    assert len(reply_service.buttons) == 1


def test_success_key_high_rate():
    # Arrange
    reply_service = ReplyService()

    # Act
    reply_service.add_settings_menu('高レート')

    # Assert
    assert len(reply_service.buttons) == 1


def test_success_key_ranking_point():
    # Arrange
    reply_service = ReplyService()

    # Act
    reply_service.add_settings_menu('順位点')

    # Assert
    assert len(reply_service.buttons) == 1


def test_success_key_tobi_bonus():
    # Arrange
    reply_service = ReplyService()

    # Act
    reply_service.add_settings_menu('飛び賞')

    # Assert
    assert len(reply_service.buttons) == 1


def test_success_key_calculate_method1():
    # Arrange
    reply_service = ReplyService()

    # Act
    reply_service.add_settings_menu('端数計算方法')

    # Assert
    assert len(reply_service.buttons) == 1


def test_success_key_calculate_method2():
    # Arrange
    reply_service = ReplyService()

    # Act
    reply_service.add_settings_menu(key='端数計算方法2')

    # Assert
    assert len(reply_service.buttons) == 1
