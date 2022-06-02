from use_cases.group_line.QuitGroupUseCase import QuitGroupUseCase
from ApplicationService import (
    reply_service,
    request_info_service,
)
from DomainModel.entities.Group import Group, GroupMode
from DomainModel.entities.Hanchan import Hanchan
from DomainModel.entities.Match import Match
from repositories import (
    match_repository,
    group_repository,
    hanchan_repository,
    session_scope,
)

dummy_group = Group(
    line_group_id="G0123456789abcdefghijklmnopqrstu1",
    zoom_url="https://us01web.zoom.us/j/01234567891?pwd=abcdefghijklmnopqrstuvwxyz",
    mode=GroupMode.input,
    _id=1,
)

dummy_match = Match(
    line_group_id=dummy_group.line_group_id,
    hanchan_ids=[],
    users=[],
    status=1,
)

dummy_hanchan = Hanchan(
    line_group_id=dummy_group.line_group_id,
    raw_scores={},
    converted_scores={},
    match_id=1,
    status=1,
)


def test_execute():
    # Arrage
    use_case = QuitGroupUseCase()
    request_info_service.req_line_group_id = dummy_group.line_group_id
    with session_scope() as session:
        group_repository.create(session, dummy_group)
        match_repository.create(session, dummy_match)
        hanchan_repository.create(session, dummy_hanchan)

    # Act
    use_case.execute()

    # Assert
    assert len(reply_service.texts) == 1
    assert reply_service.texts[0].text == "始める時は「_start」と入力してください。"
    with session_scope() as session:
        groups = group_repository.find_all(session)
        assert groups[0].mode == GroupMode.wait
        hanchans = hanchan_repository.find_all(session)
        assert hanchans[0].status == 0
