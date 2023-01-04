from dataclasses import dataclass

from injector import inject

from src.application.responses import ResponseSuccess
from src.data.messages.messages_repository import MessagesRepository
from src.domain.exceptions import HttpException


@dataclass
class GetMessagesForSocialWorkerQuery:
    current_user_id: str

    @inject
    def execute(self, msg_repo: MessagesRepository):
        try:
            messages = msg_repo.get_messages(self.current_user_id)
            results = [msg.to_dict() for msg in messages]
            return ResponseSuccess(value=results)
        except Exception as e:
            raise HttpException(f'Failed to query social worker messages: {e}', 401)
