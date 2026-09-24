import pytest

from application_service import (
    reply_service,
    request_info_service,
)
from domain_model.entities.group import Group, GroupMode
from domain_model.entities.hanchan import Hanchan
from domain_model.entities.match import Match, MatchStatus
from line_models.event import Event
from repositories import (
    group_repository,
    hanchan_repository,
    match_repository,
)
from use_cases.group_line.drop_hanchan_by_index_use_case import (
    DropHanchanByIndexUseCase,
)

dummy_event = Event(
    type="message",
    source_type="group",
    user_id="U0123456789abcdefghijklmnopqrstu1",
    group_id="G0123456789abcdefghijklmnopqrstu1",
    message_type="text",
    text="dummy_text",
)

dummy_group = Group(
    line_group_id="G0123456789abcdefghijklmnopqrstu1",
    mode=GroupMode.input.value,
    current_input_match_id=1,
    _id=1,
)

dummy_matches = [
    Match(
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
        _id=1,
    ),
]
dummy_hanchans = [
    Hanchan(
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
        match_id=1,
        raw_scores={
            "U0123456789abcdefghijklmnopqrstu1": 10000,
            "U0123456789abcdefghijklmnopqrstu2": 20000,
            "U0123456789abcdefghijklmnopqrstu3": 30000,
            "U0123456789abcdefghijklmnopqrstu4": 40000,
        },
        converted_scores={
            "U0123456789abcdefghijklmnopqrstu1": -40,
            "U0123456789abcdefghijklmnopqrstu2": -20,
            "U0123456789abcdefghijklmnopqrstu3": 10,
            "U0123456789abcdefghijklmnopqrstu4": 50,
        },
        _id=1,
    ),
    Hanchan(
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
        match_id=1,
        raw_scores={
            "U0123456789abcdefghijklmnopqrstu1": 10000,
            "U0123456789abcdefghijklmnopqrstu2": 20000,
            "U0123456789abcdefghijklmnopqrstu3": 30000,
            "U0123456789abcdefghijklmnopqrstu4": 40000,
        },
        converted_scores={
            "U0123456789abcdefghijklmnopqrstu1": -40,
            "U0123456789abcdefghijklmnopqrstu2": -20,
            "U0123456789abcdefghijklmnopqrstu3": 10,
            "U0123456789abcdefghijklmnopqrstu4": 50,
        },
        _id=2,
    ),
    Hanchan(
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
        match_id=1,
        _id=3,
        raw_scores={
            "U0123456789abcdefghijklmnopqrstu1": 10000,
            "U0123456789abcdefghijklmnopqrstu2": 20000,
            "U0123456789abcdefghijklmnopqrstu3": 30000,
            "U0123456789abcdefghijklmnopqrstu4": 40000,
        },
        converted_scores={
            "U0123456789abcdefghijklmnopqrstu1": -40,
            "U0123456789abcdefghijklmnopqrstu2": -20,
            "U0123456789abcdefghijklmnopqrstu3": 10,
            "U0123456789abcdefghijklmnopqrstu4": 50,
        },
    ),
    Hanchan(
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
        match_id=1,
        _id=4,
    ),
    Hanchan(
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
        match_id=1,
        is_deleted=True,
        _id=5,
        raw_scores={
            "U0123456789abcdefghijklmnopqrstu1": 10000,
            "U0123456789abcdefghijklmnopqrstu2": 20000,
            "U0123456789abcdefghijklmnopqrstu3": 30000,
            "U0123456789abcdefghijklmnopqrstu4": 40000,
        },
        converted_scores={
            "U0123456789abcdefghijklmnopqrstu1": -40,
            "U0123456789abcdefghijklmnopqrstu2": -20,
            "U0123456789abcdefghijklmnopqrstu3": 10,
            "U0123456789abcdefghijklmnopqrstu4": 50,
        },
    ),
    Hanchan(
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
        match_id=999,
        _id=6,
        raw_scores={
            "U0123456789abcdefghijklmnopqrstu1": 10000,
            "U0123456789abcdefghijklmnopqrstu2": 20000,
            "U0123456789abcdefghijklmnopqrstu3": 30000,
            "U0123456789abcdefghijklmnopqrstu4": 40000,
        },
        converted_scores={
            "U0123456789abcdefghijklmnopqrstu1": -40,
            "U0123456789abcdefghijklmnopqrstu2": -20,
            "U0123456789abcdefghijklmnopqrstu3": 10,
            "U0123456789abcdefghijklmnopqrstu4": 50,
        },
    ),
    Hanchan(
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
        match_id=1,
        _id=7,
        raw_scores={
            "U0123456789abcdefghijklmnopqrstu1": 10000,
            "U0123456789abcdefghijklmnopqrstu2": 20000,
            "U0123456789abcdefghijklmnopqrstu3": 30000,
            "U0123456789abcdefghijklmnopqrstu4": 40000,
        },
        converted_scores={
            "U0123456789abcdefghijklmnopqrstu1": -40,
            "U0123456789abcdefghijklmnopqrstu2": -20,
            "U0123456789abcdefghijklmnopqrstu3": 10,
            "U0123456789abcdefghijklmnopqrstu4": 50,
        },
    ),
]


def test_execute():
    # 目的: test_execute の挙動を検証する。
    # 入力: なし
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: hanchans の件数が 0 件 / reply_service.texts の件数が 1 件 / reply_service.texts[0].text が "現在の対戦の第2半荘の結果を削除しました。" である
    # reply_service: texts
    # DB操作: group_repository.create(dummy_group); match_repository.create(dummy_matches[0]); hanchan_repository.create(dummy_hanchan); hanchans = hanchan_repository.find({"_id": 2})
    # Arrange
    use_case = DropHanchanByIndexUseCase()
    request_info_service.set_req_info(event=dummy_event)
    group_repository.create(dummy_group)
    match_repository.create(dummy_matches[0])
    for dummy_hanchan in dummy_hanchans:
        hanchan_repository.create(dummy_hanchan)

    # Act
    use_case.execute("2")

    # Assert
    hanchans = hanchan_repository.find({"_id": 2})
    assert len(hanchans) == 0
    assert len(reply_service.texts) == 1
    assert reply_service.texts[0].text == "現在の対戦の第2半荘の結果を削除しました。"


def test_execute_ignore_other_hanchans():
    # 目的: test_execute_ignore_other_hanchans の挙動を検証する。
    # 入力: なし
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: hanchans の件数が 0 件 / reply_service.texts の件数が 1 件 / reply_service.texts[0].text が "現在の対戦の第4半荘の結果を削除しました。" である
    # reply_service: texts
    # DB操作: group_repository.create(dummy_group); match_repository.create(dummy_matches[0]); hanchan_repository.create(dummy_hanchan); hanchans = hanchan_repository.find({"_id": 7})
    # Arrange
    use_case = DropHanchanByIndexUseCase()
    request_info_service.set_req_info(event=dummy_event)
    group_repository.create(dummy_group)
    match_repository.create(dummy_matches[0])
    for dummy_hanchan in dummy_hanchans:
        hanchan_repository.create(dummy_hanchan)

    # Act
    use_case.execute("4")

    # Assert
    hanchans = hanchan_repository.find({"_id": 7})
    assert len(hanchans) == 0
    assert len(reply_service.texts) == 1
    assert reply_service.texts[0].text == "現在の対戦の第4半荘の結果を削除しました。"


def test_execute_arg_int():
    # 目的: test_execute_arg_int の挙動を検証する。
    # 入力: なし
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: records_in_db の件数が 6 件
    # reply_service: なし
    # DB操作: group_repository.create(dummy_group); match_repository.create(dummy_matches[0]); hanchan_repository.create(dummy_hanchan); records_in_db = hanchan_repository.find()
    # Arrange
    use_case = DropHanchanByIndexUseCase()
    request_info_service.set_req_info(event=dummy_event)
    group_repository.create(dummy_group)
    match_repository.create(dummy_matches[0])
    for dummy_hanchan in dummy_hanchans:
        hanchan_repository.create(dummy_hanchan)

    # Act
    with pytest.raises(
        AttributeError,
        match="'int' object has no attribute 'isdigit'",
    ):
        use_case.execute(1)

    # Assert
    records_in_db = hanchan_repository.find()
    assert len(records_in_db) == 6


def test_execute_no_arg():
    # 目的: test_execute_no_arg の挙動を検証する。
    # 入力: なし
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: records_in_db の件数が 6 件
    # reply_service: なし
    # DB操作: group_repository.create(dummy_group); match_repository.create(dummy_matches[0]); hanchan_repository.create(dummy_hanchan); records_in_db = hanchan_repository.find()
    # Arrange
    use_case = DropHanchanByIndexUseCase()
    request_info_service.set_req_info(event=dummy_event)
    group_repository.create(dummy_group)
    match_repository.create(dummy_matches[0])
    for dummy_hanchan in dummy_hanchans:
        hanchan_repository.create(dummy_hanchan)

    # Act
    with pytest.raises(
        AttributeError,
        match="'int' object has no attribute 'isdigit'",
    ):
        use_case.execute(1)

    # Assert
    records_in_db = hanchan_repository.find()
    assert len(records_in_db) == 6


def test_execute_arg_no_digit():
    # 目的: test_execute_arg_no_digit の挙動を検証する。
    # 入力: なし
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: hanchans の件数が 6 件 / reply_service.texts の件数が 1 件 / reply_service.texts[0].text が "引数は整数で指定してください。" である
    # reply_service: texts
    # DB操作: group_repository.create(dummy_group); match_repository.create(dummy_matches[0]); hanchan_repository.create(dummy_hanchan); hanchans = hanchan_repository.find()
    # Arrange
    use_case = DropHanchanByIndexUseCase()
    request_info_service.set_req_info(event=dummy_event)
    group_repository.create(dummy_group)
    match_repository.create(dummy_matches[0])
    for dummy_hanchan in dummy_hanchans:
        hanchan_repository.create(dummy_hanchan)

    # Act
    use_case.execute("test")

    # Assert
    hanchans = hanchan_repository.find()
    assert len(hanchans) == 6
    assert len(reply_service.texts) == 1
    assert reply_service.texts[0].text == "引数は整数で指定してください。"


def test_execute_no_group():
    # 目的: test_execute_no_group の挙動を検証する。
    # 入力: なし
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: hanchans の件数が 6 件 / reply_service.texts の件数が 1 件 / (
    # reply_service: texts
    # DB操作: match_repository.create(dummy_matches[0]); hanchan_repository.create(dummy_hanchan); hanchans = hanchan_repository.find()
    # Arrange
    use_case = DropHanchanByIndexUseCase()
    request_info_service.set_req_info(event=dummy_event)
    match_repository.create(dummy_matches[0])
    for dummy_hanchan in dummy_hanchans:
        hanchan_repository.create(dummy_hanchan)

    # Act
    use_case.execute("1")

    # Assert
    hanchans = hanchan_repository.find()
    assert len(hanchans) == 6
    assert len(reply_service.texts) == 1
    assert (
        reply_service.texts[0].text
        == "トークルームが登録されていません。招待し直してください。"
    )


def test_execute_no_match():
    # 目的: test_execute_no_match の挙動を検証する。
    # 入力: なし
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: hanchans の件数が 6 件 / reply_service.texts の件数が 1 件 / reply_service.texts[0].text が "現在進行中の対戦がありません。" である
    # reply_service: texts
    # DB操作: group_repository.create(no_match_group); match_repository.create(dummy_matches[0]); hanchan_repository.create(dummy_hanchan); hanchans = hanchan_repository.find()
    # Arrange
    use_case = DropHanchanByIndexUseCase()
    request_info_service.set_req_info(event=dummy_event)
    no_match_group = Group(
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
        mode=GroupMode.input.value,
        _id=1,
    )
    group_repository.create(no_match_group)
    match_repository.create(dummy_matches[0])
    for dummy_hanchan in dummy_hanchans:
        hanchan_repository.create(dummy_hanchan)

    # Act
    use_case.execute("1")

    # Assert
    hanchans = hanchan_repository.find()
    assert len(hanchans) == 6
    assert len(reply_service.texts) == 1
    assert reply_service.texts[0].text == "現在進行中の対戦がありません。"


def test_execute_fail_get_active_match():
    # 目的: test_execute_fail_get_active_match の挙動を検証する。
    # 入力: なし
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: hanchans の件数が 6 件 / reply_service.texts の件数が 0 件
    # reply_service: texts
    # DB操作: group_repository.create(dummy_group); hanchan_repository.create(dummy_hanchan); hanchans = hanchan_repository.find()
    # Arrange
    use_case = DropHanchanByIndexUseCase()
    request_info_service.set_req_info(event=dummy_event)
    group_repository.create(dummy_group)
    for dummy_hanchan in dummy_hanchans:
        hanchan_repository.create(dummy_hanchan)

    # Act
    with pytest.raises(BaseException):
        use_case.execute("1")

    # Assert
    hanchans = hanchan_repository.find()
    assert len(hanchans) == 6
    assert len(reply_service.texts) == 0


@pytest.fixture(params=["0", "5"])
def text_case1(request):
    return request.param


def test_execute_out_of_index(text_case1):
    # 目的: test_execute_out_of_index の挙動を検証する。
    # 入力: text_case1
    # 入力の意図: 指定入力・状態に対するユースケースの出力/副作用を確認する。
    # 想定出力: hanchans の件数が 6 件 / reply_service.texts の件数が 1 件 / (
    # reply_service: texts
    # DB操作: group_repository.create(dummy_group); match_repository.create(dummy_matches[0]); hanchan_repository.create(dummy_hanchan); hanchans = hanchan_repository.find()
    # Arrange
    use_case = DropHanchanByIndexUseCase()
    request_info_service.set_req_info(event=dummy_event)
    group_repository.create(dummy_group)
    match_repository.create(dummy_matches[0])
    for dummy_hanchan in dummy_hanchans:
        hanchan_repository.create(dummy_hanchan)

    # Act
    use_case.execute(text_case1)

    # Assert
    hanchans = hanchan_repository.find()
    assert len(hanchans) == 6
    assert len(reply_service.texts) == 1
    assert (
        reply_service.texts[0].text
        == f"このトークルームには全4回までしか登録されていないため第{text_case1}回はありません。"
    )


def test_select_deletes_the_chosen_hanchan():
    """_drop_select?to=<hanchan_id> で指定された半荘を削除する。"""
    match = match_repository.create(
        Match(line_group_id="G0123456789abcdefghijklmnopqrstu1", status=MatchStatus.open.value),
    )
    hanchan_repository.create(
        Hanchan(
            line_group_id="G0123456789abcdefghijklmnopqrstu1",
            match_id=match._id,
            converted_scores={"U0123456789abcdefghijklmnopqrstu1": 10},
        ),
    )
    target = hanchan_repository.create(
        Hanchan(
            line_group_id="G0123456789abcdefghijklmnopqrstu1",
            match_id=match._id,
            converted_scores={"U0123456789abcdefghijklmnopqrstu1": 20},
        ),
    )
    request_info_service.set_req_info(event=dummy_event)
    request_info_service.params = {"to": str(target._id)}

    DropHanchanByIndexUseCase().select()

    # find()はis_deleted=Trueを除外するため、削除後は見つからなくなる
    assert len(hanchan_repository.find({"_id": target._id})) == 0
    assert len(reply_service.texts) == 1
    assert reply_service.texts[0].text == "現在の対戦の第2半荘の結果を削除しました。"


def test_select_missing_param():
    """toパラメータがない場合はエラーメッセージが返る。"""
    request_info_service.set_req_info(event=dummy_event)
    request_info_service.params = {}

    DropHanchanByIndexUseCase().select()

    assert len(reply_service.texts) == 1
    assert reply_service.texts[0].text == "削除する半荘が指定されていません。"


def test_select_not_found():
    """存在しないhanchan_idを指定した場合はエラーメッセージが返る。"""
    request_info_service.set_req_info(event=dummy_event)
    request_info_service.params = {"to": "644c838186bbd9e20a91b785"}

    DropHanchanByIndexUseCase().select()

    assert len(reply_service.texts) == 1
    assert "見つかりません" in reply_service.texts[0].text


def test_select_already_deleted():
    """既に削除済みの半荘を指定した場合はエラーメッセージが返る。"""
    match = match_repository.create(
        Match(line_group_id="G0123456789abcdefghijklmnopqrstu1", status=MatchStatus.open.value),
    )
    target = hanchan_repository.create(
        Hanchan(
            line_group_id="G0123456789abcdefghijklmnopqrstu1",
            match_id=match._id,
            converted_scores={"U0123456789abcdefghijklmnopqrstu1": 10},
            is_deleted=True,
        ),
    )
    request_info_service.set_req_info(event=dummy_event)
    request_info_service.params = {"to": str(target._id)}

    DropHanchanByIndexUseCase().select()

    assert len(reply_service.texts) == 1
    assert "見つかりません" in reply_service.texts[0].text


def test_select_rejects_hanchan_of_settled_match():
    """紐づくMatchがsettled(open以外)の場合は拒否する(表示していた対戦と
    削除対象がずれる余地をなくすための再検証)。
    """
    match = match_repository.create(
        Match(line_group_id="G0123456789abcdefghijklmnopqrstu1", status=MatchStatus.settled.value),
    )
    target = hanchan_repository.create(
        Hanchan(
            line_group_id="G0123456789abcdefghijklmnopqrstu1",
            match_id=match._id,
            converted_scores={"U0123456789abcdefghijklmnopqrstu1": 10},
        ),
    )
    request_info_service.set_req_info(event=dummy_event)
    request_info_service.params = {"to": str(target._id)}

    DropHanchanByIndexUseCase().select()

    assert len(reply_service.texts) == 1
    assert "見つかりません" in reply_service.texts[0].text
    unchanged = hanchan_repository.find({"_id": target._id})[0]
    assert unchanged.is_deleted is False


def test_select_malformed_hanchan_id():
    """不正な形式のhanchan_idを指定した場合、例外を投げずエラーメッセージが返る。"""
    request_info_service.set_req_info(event=dummy_event)
    request_info_service.params = {"to": "not-a-valid-object-id"}

    DropHanchanByIndexUseCase().select()

    assert len(reply_service.texts) == 1
    assert "見つかりません" in reply_service.texts[0].text
