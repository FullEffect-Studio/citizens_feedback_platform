from dataclasses import dataclass
from uuid import uuid4

from injector import inject

from application.dtos.save_feedback_dto import SaveFeedbackDto
from application.responses import ResponseSuccess
from data.statistics.statistics_repository import StatisticsRepository
from domain.exceptions.invalid_user_input_exception import HttpException
from domain.statistic import Statistic


@dataclass
class SaveFeedbackCommand:
    payload: SaveFeedbackDto
    current_user_id: str

    @inject
    def execute(self, stats_repo: StatisticsRepository):
        user_stat = stats_repo.get_stats_by_social_worker(self.current_user_id)
        family = 0
        health = 0
        unknown = 0


        for feed in self.payload.feedback:
            concern = feed[0]
            age = feed[1]

            if 'family' in str(concern).lower() and age < 25:
                family += 1
            elif 'health' in str(concern).lower() and age > 18:
                health += 1
            else:
                unknown += 1

        try:
            if user_stat is None:
                model = Statistic(
                    id=uuid4(),
                    social_worker_id=self.current_user_id,
                    family=family,
                    health=health,
                    unknown=unknown
                )
                stats_repo.add_stats(model)
            else:
                user_stat.family += family
                user_stat.health += health
                user_stat.unknown += unknown
                stats_repo.update_stats(user_stat)

            return ResponseSuccess()
        except Exception as e:
            raise HttpException(f'An error occurred while saving statistics: {e}', 401)
