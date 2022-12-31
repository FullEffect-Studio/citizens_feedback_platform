from app.requests.user_list import UserListValidRequest, UserListInvalidRequest
from app.responses import ResponseSuccess, build_response_from_invalid_request, ResponseTypes, ResponseFailure


def user_list_usecase(repo, request):

    if not request:
        return build_response_from_invalid_request(request)

    try:
        users = repo.list(filters=request.filters)
        return ResponseSuccess(users)
    except Exception as e:
        return ResponseFailure(ResponseTypes.SYSTEM_ERROR, e)

