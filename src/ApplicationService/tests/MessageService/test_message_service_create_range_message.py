from datetime import datetime

import pytest

from ApplicationService.MessageService import MessageService


@pytest.fixture(params=[
    (None, None, None),
    (datetime(2023,1,1), None, "範囲指定: 2023年01月01日0時から"),
    (None, datetime(2024,12,31), "範囲指定: 2024年12月31日0時まで"),
    (datetime(2023,1,1), datetime(2024,12,31), "範囲指定: 2023年01月01日0時から2024年12月31日0時まで"),
])
def case(request) -> str:
    return request.param

def test_success(case):
    # Arrange
    message_service = MessageService()

    # Act
    result = message_service.create_range_message(
        from_dt=case[0],
        to_dt=case[1],
    )

    # Assert
    assert result == case[2]
