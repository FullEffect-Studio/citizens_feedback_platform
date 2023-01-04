import datetime
from dataclasses import dataclass
from uuid import uuid4

from injector import inject

from application.dtos.revise_data_dto import ReviseDataDto
from application.dtos.save_feedback_dto import SaveFeedbackDto
from application.responses import ResponseSuccess
from data.messages.messages_repository import MessagesRepository
from data.statistics.statistics_repository import StatisticsRepository
from domain.exceptions import HttpException
from domain.message import Message
from domain.statistic import Statistic


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
