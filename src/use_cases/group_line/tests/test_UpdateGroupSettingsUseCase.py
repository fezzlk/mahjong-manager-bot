from use_cases.group_line.UpdateGroupSettingsUseCase import UpdateGroupSettingsUseCase
from ApplicationService import (
    reply_service,
    request_info_service,
)
from line_models.Event import Event
from DomainModel.entities.GroupSetting import GroupSetting, ROUNDING_METHOD_LIST
from repositories import group_setting_repository
import pytest


dummy_event = Event(
    type='message',
    source_type='group',
    user_id="U0123456789abcdefghijklmnopqrstu1",
    group_id="G0123456789abcdefghijklmnopqrstu1",
    message_type='text',
    text='_input',
)

dummy_setting = GroupSetting(
    line_group_id='G0123456789abcdefghijklmnopqrstu1',
    rate=0,
    ranking_prize=[20, 10, -10, -20],
    tip_rate=0,
    tobi_prize=10,
    num_of_players=4,
    rounding_method=0,
)

def test_execute_rate():
    # Arrange
    request_info_service.set_req_info(event=dummy_event)
    use_case = UpdateGroupSettingsUseCase()
    group_setting_repository.create(dummy_setting)

    # Act
    use_case.execute('レート', '3')

    # Assert
    assert len(reply_service.texts) == 1
    assert reply_service.texts[0].text == '[レート]を[点3]に変更しました。'
    settings = group_setting_repository.find()
    assert settings[0].line_group_id == 'G0123456789abcdefghijklmnopqrstu1'
    assert settings[0].rate == 3
    assert settings[0].ranking_prize == [20, 10, -10, -20]
    assert settings[0].tip_rate == 0
    assert settings[0].tobi_prize == 10
    assert settings[0].num_of_players == 4
    assert settings[0].rounding_method == 0


def test_execute_ranking_prize():
    # Arrange
    request_info_service.set_req_info(event=dummy_event)
    use_case = UpdateGroupSettingsUseCase()
    group_setting_repository.create(dummy_setting)

    # Act
    use_case.execute('順位点', '30,10,-10,-30')

    # Assert
    assert len(reply_service.texts) == 1
    assert reply_service.texts[0].text == '[順位点]を[1着 30/2着 10/3着 -10/4着 -30]に変更しました。'
    settings = group_setting_repository.find()
    assert settings[0].line_group_id == 'G0123456789abcdefghijklmnopqrstu1'
    assert settings[0].rate == 0
    assert settings[0].ranking_prize == [30, 10, -10, -30]
    assert settings[0].tip_rate == 0
    assert settings[0].tobi_prize == 10
    assert settings[0].num_of_players == 4
    assert settings[0].rounding_method == 0

    
def test_execute_tip_rate():
    # Arrange
    request_info_service.set_req_info(event=dummy_event)
    use_case = UpdateGroupSettingsUseCase()
    group_setting_repository.create(dummy_setting)

    # Act
    use_case.execute('チップ', '100')

    # Assert
    assert len(reply_service.texts) == 1
    assert reply_service.texts[0].text == '[チップ]を[1枚100円]に変更しました。'
    settings = group_setting_repository.find()
    assert settings[0].line_group_id == 'G0123456789abcdefghijklmnopqrstu1'
    assert settings[0].rate == 0
    assert settings[0].ranking_prize == [20, 10, -10, -20]
    assert settings[0].tip_rate == 100
    assert settings[0].tobi_prize == 10
    assert settings[0].num_of_players == 4
    assert settings[0].rounding_method == 0


def test_execute_tobi_prize():
    # Arrange
    request_info_service.set_req_info(event=dummy_event)
    use_case = UpdateGroupSettingsUseCase()
    group_setting_repository.create(dummy_setting)

    # Act
    use_case.execute('飛び賞', '0')

    # Assert
    assert len(reply_service.texts) == 1
    assert reply_service.texts[0].text == '[飛び賞]を[0]に変更しました。'
    settings = group_setting_repository.find()
    assert settings[0].line_group_id == 'G0123456789abcdefghijklmnopqrstu1'
    assert settings[0].rate == 0
    assert settings[0].ranking_prize == [20, 10, -10, -20]
    assert settings[0].tip_rate == 0
    assert settings[0].tobi_prize == 0
    assert settings[0].num_of_players == 4
    assert settings[0].rounding_method == 0


def test_execute_num_of_players():
    # Arrange
    request_info_service.set_req_info(event=dummy_event)
    use_case = UpdateGroupSettingsUseCase()
    group_setting_repository.create(dummy_setting)

    # Act
    use_case.execute('人数', '3')

    # Assert
    assert len(reply_service.texts) == 1
    assert reply_service.texts[0].text == '[人数]を[3人]に変更しました。'
    settings = group_setting_repository.find()
    assert settings[0].line_group_id == 'G0123456789abcdefghijklmnopqrstu1'
    assert settings[0].rate == 0
    assert settings[0].ranking_prize == [20, 10, -10, -20]
    assert settings[0].tip_rate == 0
    assert settings[0].tobi_prize == 10
    assert settings[0].num_of_players == 3
    assert settings[0].rounding_method == 0


def test_execute_rounding_method():
    # Arrange
    request_info_service.set_req_info(event=dummy_event)
    use_case = UpdateGroupSettingsUseCase()
    group_setting_repository.create(dummy_setting)

    # Act
    use_case.execute('端数計算方法', '1')

    # Assert
    assert len(reply_service.texts) == 1
    assert reply_service.texts[0].text == '[端数計算方法]を[五捨六入]に変更しました。'
    settings = group_setting_repository.find()
    assert settings[0].line_group_id == 'G0123456789abcdefghijklmnopqrstu1'
    assert settings[0].rate == 0
    assert settings[0].ranking_prize == [20, 10, -10, -20]
    assert settings[0].tip_rate == 0
    assert settings[0].tobi_prize == 10
    assert settings[0].num_of_players == 4
    assert settings[0].rounding_method == 1


def test_execute_rounding_method():
    # Arrange
    request_info_service.set_req_info(event=dummy_event)
    use_case = UpdateGroupSettingsUseCase()
    group_setting_repository.create(dummy_setting)

    # Act
    use_case.execute('端数計算方法', '1')

    # Assert
    assert len(reply_service.texts) == 1
    assert reply_service.texts[0].text == '[端数計算方法]を[五捨六入]に変更しました。'
    settings = group_setting_repository.find()
    assert settings[0].line_group_id == 'G0123456789abcdefghijklmnopqrstu1'
    assert settings[0].rate == 0
    assert settings[0].ranking_prize == [20, 10, -10, -20]
    assert settings[0].tip_rate == 0
    assert settings[0].tobi_prize == 10
    assert settings[0].num_of_players == 4
    assert settings[0].rounding_method == 1


def test_execute_invalid_key():
    # Arrange
    request_info_service.set_req_info(event=dummy_event)
    use_case = UpdateGroupSettingsUseCase()
    group_setting_repository.create(dummy_setting)

    # Act
    use_case.execute('dummy', '1')

    # Assert
    assert len(reply_service.texts) == 1
    assert reply_service.texts[0].text == '項目[dummy]は未知の項目のため、[dummy]を[1]に変更できません'
    settings = group_setting_repository.find()
    assert settings[0].line_group_id == 'G0123456789abcdefghijklmnopqrstu1'
    assert settings[0].rate == 0
    assert settings[0].ranking_prize == [20, 10, -10, -20]
    assert settings[0].tip_rate == 0
    assert settings[0].tobi_prize == 10
    assert settings[0].num_of_players == 4
    assert settings[0].rounding_method == 0



@pytest.fixture(params=[
    ('レート', '6', '[レート]を[6]に変更できません'),
    ('順位点', '10,20,30', '[順位点]を[10,20,30]に変更できません'),
    ('順位点', '10,20,30,40,50', '[順位点]を[10,20,30,40,50]に変更できません'),
    ('チップ', '1', '[チップ]を[1]に変更できません'),
    ('飛び賞', '1', '[飛び賞]を[1]に変更できません'),
    ('人数', '2', '[人数]を[2]に変更できません'),
    ('端数計算方法', '5', '[端数計算方法]を[5]に変更できません'),
])
def text_case1(request):
    return request.param

def test_execute_invalid_key(text_case1):
    # Arrange
    request_info_service.set_req_info(event=dummy_event)
    use_case = UpdateGroupSettingsUseCase()
    group_setting_repository.create(dummy_setting)

    # Act
    use_case.execute(text_case1[0], text_case1[1])

    # Assert
    assert len(reply_service.texts) == 1
    assert reply_service.texts[0].text == text_case1[2]
    settings = group_setting_repository.find()
    assert settings[0].line_group_id == 'G0123456789abcdefghijklmnopqrstu1'
    assert settings[0].rate == 0
    assert settings[0].ranking_prize == [20, 10, -10, -20]
    assert settings[0].tip_rate == 0
    assert settings[0].tobi_prize == 10
    assert settings[0].num_of_players == 4
    assert settings[0].rounding_method == 0
