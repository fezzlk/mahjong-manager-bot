import pytest

from application_service import (
    reply_service,
    request_info_service,
)
from domain_model.entities.group import Group, GroupMode
from domain_model.entities.group_setting import EmbeddedGroupSettings
from line_models.event import Event
from repositories import group_repository
from use_cases.group_line.update_group_settings_use_case import (
    UpdateGroupSettingsUseCase,
)

dummy_line_group_id = "G0123456789abcdefghijklmnopqrstu1"

dummy_event = Event(
    type="message",
    source_type="group",
    user_id="U0123456789abcdefghijklmnopqrstu1",
    group_id=dummy_line_group_id,
    message_type="text",
    text="_input",
)

dummy_initial_settings = EmbeddedGroupSettings(
    rate=0,
    ranking_prize=[20, 10, -10, -20],
    chip_rate=0,
    tobi_prize=10,
    num_of_players=4,
    rounding_method=0,
)


def _setup():
    """グループと初期設定を作成する"""
    group_repository.create(Group(line_group_id=dummy_line_group_id, mode=GroupMode.wait.value))
    group_repository.update_settings(dummy_line_group_id, dummy_initial_settings)


def _get_settings():
    return group_repository.find({"line_group_id": dummy_line_group_id})[0].settings


def test_execute_rate():
    # 目的: レートを変更したとき settings.rate が更新されること
    # 入力: rate=3
    # 想定出力: settings.rate が 3 / 他フィールドは変わらない
    request_info_service.set_req_info(event=dummy_event)
    _setup()
    use_case = UpdateGroupSettingsUseCase()

    use_case.execute("レート", "3")

    assert len(reply_service.texts) == 1
    assert reply_service.texts[0].text == "[レート]を[点3]に変更しました。"
    s = _get_settings()
    assert s.rate == 3
    assert s.ranking_prize == [20, 10, -10, -20]
    assert s.chip_rate == 0
    assert s.tobi_prize == 10
    assert s.num_of_players == 4
    assert s.rounding_method == 0


def test_execute_ranking_prize():
    # 目的: 順位点を変更したとき settings.ranking_prize が更新されること
    request_info_service.set_req_info(event=dummy_event)
    _setup()
    use_case = UpdateGroupSettingsUseCase()

    use_case.execute("順位点", "30,10,-10,-30")

    assert len(reply_service.texts) == 1
    assert (
        reply_service.texts[0].text
        == "[順位点]を[1着 30/2着 10/3着 -10/4着 -30]に変更しました。"
    )
    s = _get_settings()
    assert s.rate == 0
    assert s.ranking_prize == [30, 10, -10, -30]
    assert s.chip_rate == 0
    assert s.tobi_prize == 10
    assert s.num_of_players == 4
    assert s.rounding_method == 0


def test_execute_chip_rate():
    # 目的: チップを変更したとき settings.chip_rate が更新されること
    request_info_service.set_req_info(event=dummy_event)
    _setup()
    use_case = UpdateGroupSettingsUseCase()

    use_case.execute("チップ", "1")

    assert len(reply_service.texts) == 1
    assert reply_service.texts[0].text == "[チップ]を[あり(1枚=1点)]に変更しました。"
    s = _get_settings()
    assert s.rate == 0
    assert s.ranking_prize == [20, 10, -10, -20]
    assert s.chip_rate == 1
    assert s.tobi_prize == 10
    assert s.num_of_players == 4
    assert s.rounding_method == 0


def test_execute_tobi_prize():
    # 目的: 飛び賞を変更したとき settings.tobi_prize が更新されること
    request_info_service.set_req_info(event=dummy_event)
    _setup()
    use_case = UpdateGroupSettingsUseCase()

    use_case.execute("飛び賞", "0")

    assert len(reply_service.texts) == 1
    assert reply_service.texts[0].text == "[飛び賞]を[0]に変更しました。"
    s = _get_settings()
    assert s.rate == 0
    assert s.ranking_prize == [20, 10, -10, -20]
    assert s.chip_rate == 0
    assert s.tobi_prize == 0
    assert s.num_of_players == 4
    assert s.rounding_method == 0


def test_execute_num_of_players():
    # 目的: 人数を変更したとき settings.num_of_players が更新されること
    request_info_service.set_req_info(event=dummy_event)
    _setup()
    use_case = UpdateGroupSettingsUseCase()

    use_case.execute("人数", "3")

    assert len(reply_service.texts) == 1
    assert reply_service.texts[0].text == "[人数]を[3人]に変更しました。"
    s = _get_settings()
    assert s.rate == 0
    assert s.ranking_prize == [20, 10, -10, -20]
    assert s.chip_rate == 0
    assert s.tobi_prize == 10
    assert s.num_of_players == 3
    assert s.rounding_method == 0


def test_execute_rounding_method():
    # 目的: 端数計算方法を変更したとき settings.rounding_method が更新されること
    request_info_service.set_req_info(event=dummy_event)
    _setup()
    use_case = UpdateGroupSettingsUseCase()

    use_case.execute("端数計算方法", "1")

    assert len(reply_service.texts) == 1
    assert reply_service.texts[0].text == "[端数計算方法]を[五捨六入]に変更しました。"
    s = _get_settings()
    assert s.rate == 0
    assert s.ranking_prize == [20, 10, -10, -20]
    assert s.chip_rate == 0
    assert s.tobi_prize == 10
    assert s.num_of_players == 4
    assert s.rounding_method == 1


def test_execute_invalid_key():
    # 目的: 未知の項目を渡したとき適切なエラーメッセージが返ること
    request_info_service.set_req_info(event=dummy_event)
    _setup()
    use_case = UpdateGroupSettingsUseCase()

    use_case.execute("dummy", "1")

    assert len(reply_service.texts) == 1
    assert (
        reply_service.texts[0].text
        == "項目[dummy]は未知の項目のため、[dummy]を[1]に変更できません"
    )
    s = _get_settings()
    assert s.rate == 0
    assert s.ranking_prize == [20, 10, -10, -20]
    assert s.chip_rate == 0
    assert s.tobi_prize == 10
    assert s.num_of_players == 4
    assert s.rounding_method == 0


@pytest.fixture(
    params=[
        ("レート", "6", "[レート]を[6]に変更できません"),
        ("順位点", "10,20,30", "[順位点]を[10,20,30]に変更できません"),
        ("順位点", "10,20,30,40,50", "[順位点]を[10,20,30,40,50]に変更できません"),
        ("チップ", "2", "[チップ]を[2]に変更できません"),
        ("飛び賞", "1", "[飛び賞]を[1]に変更できません"),
        ("人数", "2", "[人数]を[2]に変更できません"),
        ("端数計算方法", "5", "[端数計算方法]を[5]に変更できません"),
    ],
)
def text_case1(request):
    return request.param


def test_execute_invalid_value(text_case1):
    # 目的: 不正な値を渡したとき変更不可メッセージが返ること
    request_info_service.set_req_info(event=dummy_event)
    _setup()
    use_case = UpdateGroupSettingsUseCase()

    use_case.execute(text_case1[0], text_case1[1])

    assert len(reply_service.texts) == 1
    assert reply_service.texts[0].text == text_case1[2]
    s = _get_settings()
    assert s.rate == 0
    assert s.ranking_prize == [20, 10, -10, -20]
    assert s.chip_rate == 0
    assert s.tobi_prize == 10
    assert s.num_of_players == 4
    assert s.rounding_method == 0
