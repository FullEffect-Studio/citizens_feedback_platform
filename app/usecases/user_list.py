from app.requests.user_list import UserListRequest
from app.responses import ResponseSuccess


def user_list_usecase(repo, request: UserListRequest):
    # Introduce error checking for invariants
    return ResponseSuccess(repo.list())
