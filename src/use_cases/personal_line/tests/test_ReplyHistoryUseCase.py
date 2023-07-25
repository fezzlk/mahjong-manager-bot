from use_cases.personal_line.ReplyHistoryUseCase import ReplyHistoryUseCase
from ApplicationService import (
    reply_service,
    request_info_service,
)
from DomainModel.entities.User import User, UserMode
from DomainModel.entities.Match import Match
from DomainModel.entities.Hanchan import Hanchan
from DomainModel.entities.UserMatch import UserMatch
from repositories import (
    user_repository,
    match_repository,
    user_match_repository,
    hanchan_repository,
)
from bson.objectid import ObjectId
import pytest

dummy_user = User(
    line_user_name="test_user1",
    line_user_id="U0123456789abcdefghijklmnopqrstu1",
    mode=UserMode.wait.value,
    jantama_name="jantama_user1",
)

dummy_match = Match(
    line_group_id="G0123456789abcdefghijklmnopqrstu1",
    status=2,
    _id=ObjectId('644c838186bbd9e20a91b783'),
)

dummy_hanchans = [
    Hanchan(
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
        raw_scores={
            "U0123456789abcdefghijklmnopqrstu1": 40000,
            "U0123456789abcdefghijklmnopqrstu2": 30000,
            "U0123456789abcdefghijklmnopqrstu3": 20000,
            "U0123456789abcdefghijklmnopqrstu4": 10000,
        },
        converted_scores={
            "U0123456789abcdefghijklmnopqrstu1": 50,
            "U0123456789abcdefghijklmnopqrstu2": 10,
            "U0123456789abcdefghijklmnopqrstu3": -20,
            "U0123456789abcdefghijklmnopqrstu4": -40,
        },
        status=2,
        match_id=ObjectId('644c838186bbd9e20a91b783'),
    ),
    Hanchan(
        line_group_id="G0123456789abcdefghijklmnopqrstu1",
        raw_scores={
            "U0123456789abcdefghijklmnopqrstu1": 40000,
            "U0123456789abcdefghijklmnopqrstu2": 30000,
            "U0123456789abcdefghijklmnopqrstu3": 20000,
            "U0123456789abcdefghijklmnopqrstu4": 10000,
        },
        converted_scores={
            "U0123456789abcdefghijklmnopqrstu1": 50,
            "U0123456789abcdefghijklmnopqrstu2": 10,
            "U0123456789abcdefghijklmnopqrstu3": -20,
            "U0123456789abcdefghijklmnopqrstu4": -40,
        },
        status=1,
        match_id=ObjectId('644c838186bbd9e20a91b783'),
    ),
]


def test_execute_no_user():
    # Arrange
    user_repository.create(dummy_user)

    request_info_service.req_line_user_id = 'unknown'
    use_case = ReplyHistoryUseCase()

    # Act
    use_case.execute()

    # Assert
    assert len(reply_service.texts) == 2
    assert reply_service.texts[0].text == 'ユーザーが登録されていません。友達追加してください。'
    assert reply_service.texts[1].text == '既に友達の場合は一度ブロックして、ブロック解除を行ってください。'


def test_execute_not_match():
    # Arrange
    user_repository.create(dummy_user)

    request_info_service.req_line_user_id = dummy_user.line_user_id
    use_case = ReplyHistoryUseCase()

    # Act
    use_case.execute()

    # Assert
    assert len(reply_service.texts) == 1
    assert reply_service.texts[0].text == '対局履歴がありません。'


def test_fail_get_hanchans():
    with pytest.raises(ValueError):
        # Arrange
        user = user_repository.create(dummy_user)
        match_repository.create(dummy_match)

        dummy_user_match = UserMatch(
            user_id=user._id,
            match_id=dummy_match._id,
        )
        user_match_repository.create(dummy_user_match)

        request_info_service.req_line_user_id = dummy_user.line_user_id
        use_case = ReplyHistoryUseCase()

        # Act
        use_case.execute()

        # Assert


def test_execute(mocker):
    # Arrange
    import matplotlib.pyplot as plt
    fig = plt.figure()
    mocker.patch.object(
        plt,
        'figure',
        return_value=fig,
    )
    mock_fig = mocker.patch.object(
        fig,
        'savefig',
        return_value=None,
    )
        
    user = user_repository.create(dummy_user)
    match = match_repository.create(dummy_match)
    for dummy_hanchan in dummy_hanchans:
        hanchan_repository.create(dummy_hanchan)
    
    dummy_user_match = UserMatch(
        user_id=user._id,
        match_id=match._id,
    )
    user_match_repository.create(dummy_user_match)

    request_info_service.req_line_user_id = dummy_user.line_user_id
    use_case = ReplyHistoryUseCase()

    # Act
    use_case.execute()

    # Assert
    mock_fig.assert_called_once()
    assert len(reply_service.images) == 1
