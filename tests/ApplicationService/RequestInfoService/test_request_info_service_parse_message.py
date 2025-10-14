import pytest

from ApplicationService.RequestInfoService import RequestInfoService


@pytest.fixture(params=[None, "", "a", "abc", "_", " _"])
def text_case_none(request):
    return request.param


def test_success_no_command(text_case_none):
    # Arrange
    request_info_service = RequestInfoService()
    request_info_service.message = text_case_none

    # Act
    request_info_service.parse_message()

    # Assert
    assert request_info_service.command is None
    assert request_info_service.body is None
    assert len(request_info_service.params) == 0


@pytest.fixture(params=[("_dummy", "dummy"), ("_?", ""), ("_ ", "")])
def text_case_command(request):
    return request.param


def test_success_only_command(text_case_command):
    # Arrange
    request_info_service = RequestInfoService()
    request_info_service.message = text_case_command[0]

    # Act
    request_info_service.parse_message()

    # Assert
    assert request_info_service.command == text_case_command[1]
    assert request_info_service.body == ""
    assert len(request_info_service.params) == 0


@pytest.fixture(
    params=["", " ", "a", "body", "body text", "body_text", "body?text", "body&text"]
)
def text_case_body(request):
    return request.param


def test_success_command_body(text_case_body):
    # Arrange
    request_info_service = RequestInfoService()
    request_info_service.message = "_dummy " + text_case_body

    # Act
    request_info_service.parse_message()

    # Assert
    assert request_info_service.command == "dummy"
    assert request_info_service.body == text_case_body
    assert len(request_info_service.params) == 0


@pytest.fixture(params=["", "?", "a", "?a", "abc"])
def text_case_no_params(request):
    return request.param


def test_success_command_body_no_params(text_case_no_params):
    # Arrange
    request_info_service = RequestInfoService()
    request_info_service.message = "_dummy?" + text_case_no_params + " body _?&text"

    # Act
    request_info_service.parse_message()

    # Assert
    assert request_info_service.command == "dummy"
    assert request_info_service.body == "body _?&text"
    assert len(request_info_service.params) == 0


@pytest.fixture(
    params=[
        ("=", "", ""),
        ("==", "", "="),
        ("a=b", "a", "b"),
        ("abc=xyz", "abc", "xyz"),
        ("?=", "?", ""),
    ]
)
def text_case_one_param(request):
    return request.param


def test_success_command_body_one_param(text_case_one_param):
    # Arrange
    request_info_service = RequestInfoService()
    request_info_service.message = "_dummy?" + text_case_one_param[0] + " body _?&text"

    # Act
    request_info_service.parse_message()

    # Assert
    assert request_info_service.command == "dummy"
    assert request_info_service.body == "body _?&text"
    assert len(request_info_service.params) == 1
    assert request_info_service.params[text_case_one_param[1]] == text_case_one_param[2]


@pytest.fixture(
    params=[
        (
            "a=x&b=y&c=z",
            {
                "a": "x",
                "b": "y",
                "c": "z",
            },
        ),
        (
            "a=x&b=y&cz",
            {
                "a": "x",
                "b": "y",
            },
        ),
        (
            "ax&by&c=z",
            {
                "c": "z",
            },
        ),
        (
            "ax&&cz",
            {},
        ),
        (
            "?a=x?&b==y&c=z",
            {
                "?a": "x?",
                "b": "=y",
                "c": "z",
            },
        ),
    ]
)
def text_case_multi_params(request):
    return request.param


def test_success_command_body_multi_params(text_case_multi_params):
    # Arrange
    request_info_service = RequestInfoService()
    request_info_service.message = (
        "_dummy?" + text_case_multi_params[0] + " body _?&text"
    )

    # Act
    request_info_service.parse_message()

    # Assert
    assert request_info_service.command == "dummy"
    assert request_info_service.body == "body _?&text"
    assert len(request_info_service.params) == len(text_case_multi_params[1])
    for k in request_info_service.params:
        assert request_info_service.params[k] == text_case_multi_params[1][k]
