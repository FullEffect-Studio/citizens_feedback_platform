from dataclasses import dataclass
from uuid import uuid4

from injector import inject

from application.dtos.save_feedback_dto import SaveFeedbackDto
from application.responses import ResponseSuccess
from data.statistics.statistics_repository import StatisticsRepository
from domain.exceptions.invalid_user_input_exception import HttpException
from domain.statistic import Statistic


@dataclass
class GetStatBySocialWorkerQuery:
    current_user_id: str

    @inject
    def execute(self, stats_repo: StatisticsRepository):
        user_stat = stats_repo.get_stats_by_social_worker(self.current_user_id)

        try:
            if user_stat is None:
                model = Statistic(
                    id=uuid4(),
                    social_worker_id=self.current_user_id,
                    family=0,
                    health=0,
                    unknown=0
                )
                return ResponseSuccess(value=model.to_dict())
            else:
                return ResponseSuccess(value=user_stat.to_dict())
        except Exception as e:
            raise HttpException(f'Failed to query social worker statistics: {e}', 401)
