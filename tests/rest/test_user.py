import json
from unittest import mock
import pytest

from domain.user import UserRole
from application.dtos.user_list_dto import UserInListDto
from application.responses import ResponseSuccess, ResponseTypes, ResponseFailure

user_in_list_dict = {
    "id": "3251a5bd-86be-428d-8ae9-6e51a8048c33",
    "username": "Ben",
    "role": UserRole.ADMIN
}

users = [UserInListDto(**user_in_list_dict).dict()]


@mock.patch("web.rest.user.user_list_usecase")
def test_get(mock_usecase, client):
    mock_usecase.return_value = ResponseSuccess(users)

    http_response = client.get('/users')

    assert json.loads(http_response.data.decode("UTF-8")) == [user_in_list_dict]

    mock_usecase.assert_called()

    assert http_response.status_code == 200
    assert http_response.mimetype == 'application/json'


@pytest.mark.parametrize(
    "response_type, expected_status_code",
    [
        (ResponseTypes.PARAMETERS_ERROR, 400),
        (ResponseTypes.RESOURCE_ERROR, 404),
        (ResponseTypes.SYSTEM_ERROR, 500),
    ],
)
@mock.patch("web.rest.user.user_list_usecase")
def test_get_response_failures(
        mock_use_case,
        client,
        response_type,
        expected_status_code,
):
    mock_use_case.return_value = ResponseFailure(
        response_type,
        message="Just an error message",
    )

    http_response = client.get("/users?dummy_request_string")

    mock_use_case.assert_called()

    print('STATUS CODE', http_response.status_code, expected_status_code)
    assert http_response.status_code == expected_status_code
