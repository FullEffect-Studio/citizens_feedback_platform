import datetime
from dataclasses import dataclass
from uuid import uuid4

from injector import inject

from src.application.dtos.revise_data_dto import ReviseDataDto
from src.application.responses import ResponseSuccess
from src.data.messages.messages_repository import MessagesRepository
from src.domain.exceptions import HttpException
from src.domain.message import Message


@dataclass
class ReviseDataCommand:
    payload: ReviseDataDto

    @inject
    def execute(self, msg_repo: MessagesRepository):
        message = Message(
            id=uuid4(),
            community_name=self.payload.community_name,
            social_worker_id=self.payload.social_worker_id,
            date_created=datetime.datetime.now().date()
        )



        try:
            msg_repo.save_message(message)
            return ResponseSuccess()
        except Exception as e:
            raise HttpException(f'An error occurred while saving message: {e}', 401)
