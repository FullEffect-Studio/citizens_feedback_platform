import pytest

from app.requests.user_list import build_user_list_request


def test_build_user_list_request_without_parameters():
    request = build_user_list_request()

    assert request.filters is None
    assert bool(request) is True


def test_build_user_list_request_from_empty_filters():
    request = build_user_list_request({})
    assert request.filters == {}
    assert bool(request) is True


def test_build_user_list_with_invalid_parameters():
    request = build_user_list_request(filters=5)

    assert request.has_errors()
    assert request.errors[0]['parameter'] == 'filters'
    assert bool(request) is False


def test_build_user_list_with_incorrect_filter_keys():
    request = build_user_list_request(filters={"a": 1})

    assert request.has_errors()
    assert request.errors[0]['parameter'] == 'filters'
    assert bool(request) is False


@pytest.mark.parametrize("key", ["role__eq", "id__eq"])
def test_build_user_list_request_accepted_filters(key):
    filters = {key: 1}

    request = build_user_list_request(filters=filters)

    assert request.filters == filters
    assert bool(request) is True


@pytest.mark.parametrize("key", ["role__lt", "id__gt"])
def test_build_user_list_request_rejected_filters(key):
    filters = {key: 1}

    request = build_user_list_request(filters=filters)

    assert request.has_errors()
    assert request.errors[0]['parameter'] == 'filters'
    assert bool(request) is False
