import json
from unittest import mock
import pytest

from app.domain.user import User

user_dict = {
    "id": "3251a5bd-86be-428d-8ae9-6e51a8048c33",
    "username": "Ben",
    "password": "qwe123!"
}

users = [User.from_dict(user_dict)]


@mock.patch("web.rest.user.user_list_usecase")
def test_get(mock_usecase, client):
    mock_usecase.return_value = users

    http_response = client.get('/users')

    print(http_response)
    assert json.loads(http_response.data.decode("UTF-8")) == [user_dict]
    mock_usecase.assert_called()
    assert http_response.status_code == 200
    assert http_response.mimetype == 'application/json'
