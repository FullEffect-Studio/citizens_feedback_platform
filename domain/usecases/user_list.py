from application.dtos.user_list_dto import UserInListDto
from application.responses import ResponseSuccess, ResponseTypes, ResponseFailure


def user_list_usecase(repo):
    try:
        users = repo.get_all()
        result = [UserInListDto(id=user.id, username=user.username, role=user.role).dict() for user in users]
        return ResponseSuccess(result)
    except Exception as e:
        print(e)
        return ResponseFailure(ResponseTypes.SYSTEM_ERROR, e)
