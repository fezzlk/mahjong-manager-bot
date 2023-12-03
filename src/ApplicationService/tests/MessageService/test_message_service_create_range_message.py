from ApplicationService.MessageService import MessageService, HAI
from tests.dummies import generate_dummy_user_list
import pytest
from datetime import datetime



@pytest.fixture(params=[
    (None, None, None),
    (datetime(2023,1,1), None, '範囲指定: 2023年01月01日から'),
    (None, datetime(2024,12,31), '範囲指定: 2024年12月31日まで'),
    (datetime(2023,1,1), datetime(2024,12,31), '範囲指定: 2023年01月01日から2024年12月31日まで'),
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