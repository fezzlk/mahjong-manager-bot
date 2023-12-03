from ApplicationService.MessageService import MessageService
import pytest
from datetime import datetime


def test_None():
    # Arrange
    message_service = MessageService()

    # Act
    result = message_service.parse_date_from_text(None)

    # Assert
    assert result[0] is None
    assert result[1] == False


@pytest.fixture(params=[
    '',
    'hoge',
    '2023-0101',
    '20230100',
    '20230132',
    '120230101',
    '0',
    '001',
    '0000101',
    '00000101',
])
def case_invalid(request) -> str:
    return request.param

def test_invalid_text(case_invalid):
    # Arrange
    message_service = MessageService()

    # Act
    result = message_service.parse_date_from_text(case_invalid)

    # Assert
    assert result[0] is None
    assert result[1] == True

now = datetime.now()
@pytest.fixture(params=[
    ('20230101', datetime(2023,1,1)),
    ('20991231', datetime(2099,12,31)),
    ('0230101', datetime(23,1,1)),
    ('000101', datetime(2000,1,1)),
    ('00101', datetime(2000,1,1)),
    ('0101', datetime(now.year,1,1)),
    ('101', datetime(now.year,1,1)),
    ('01', datetime(now.year,now.month,1)),
    ('1', datetime(now.year,now.month,1)),
])
def case_valid(request) -> str:
    return request.param

def test_success(case_valid):
    # Arrange
    message_service = MessageService()

    # Act
    result = message_service.parse_date_from_text(case_valid[0])

    # Assert
    assert result[0] == case_valid[1]
    assert result[1] == False
