from app.dtos.user_list_dto import UserListDto
from app.responses import ResponseSuccess,  ResponseTypes, ResponseFailure





def user_list_usecase(repo):
    try:
        users = repo.list()
        result = [UserListDto(id=user.id, username=user.username, role=user.role).dict() for user in users]
        return ResponseSuccess(result)
    except Exception as e:
        print(e)
        return ResponseFailure(ResponseTypes.SYSTEM_ERROR, e)
