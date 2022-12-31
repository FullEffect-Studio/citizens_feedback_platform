from app.requests.user_list import UserListRequest


def test_build_user_list_request_without_parameters():
    request = UserListRequest()
    assert bool(request) is True


def test_build_user_list_request_from_empty_dict():
    request = UserListRequest.from_dict({})
    assert bool(request) is True
