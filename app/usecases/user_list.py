from app.requests.user_list import UserListValidRequest, UserListInvalidRequest
from app.responses import ResponseSuccess


def user_list_usecase(repo, request: UserListValidRequest | UserListInvalidRequest):
    # Introduce error checking for invariants
    return ResponseSuccess(repo.list())
