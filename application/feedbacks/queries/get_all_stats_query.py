from dataclasses import dataclass
from uuid import uuid4

from injector import inject

from application.dtos.save_feedback_dto import SaveFeedbackDto
from application.responses import ResponseSuccess
from data.statistics.statistics_repository import StatisticsRepository
from domain.exceptions.invalid_user_input_exception import HttpException
from domain.statistic import Statistic


@dataclass
class GetAllStatsQuery:
    # current_user_id: str

    @inject
    def execute(self, stats_repo: StatisticsRepository):

        try:
            user_stat = stats_repo.get_all()
            return ResponseSuccess(value=user_stat.to_dict())
        except Exception as e:
            raise HttpException(f'Failed to query all stats statistics: {e}', 401)
