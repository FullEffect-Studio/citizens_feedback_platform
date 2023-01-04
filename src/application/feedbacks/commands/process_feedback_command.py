from dataclasses import dataclass
from uuid import uuid4

from injector import inject

from src.application.dtos.save_feedback_dto import SaveFeedbackDto
from src.application.responses import ResponseSuccess
from src.data.statistics.statistics_repository import StatisticsRepository
from src.domain.exceptions import HttpException
from src.domain.statistic import Statistic


@dataclass
class ProcessFeedbackCommand:
    payload: SaveFeedbackDto
    current_user_id: str

    @inject
    def execute(self, stats_repo: StatisticsRepository):
        user_stat = stats_repo.get_stats_by_community_and_social_worker(
            self.payload.community_name,
            self.current_user_id
        )

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
                print('adding new')
                model = Statistic(
                    id=uuid4(),
                    community_name=str(self.payload.community_name).strip(),
                    community_size=int(self.payload.community_size),
                    social_worker_id=self.current_user_id,
                    family=family,
                    health=health,
                    unknown=unknown
                )
                stats_repo.add_stats(model)
            else:
                print('updating exisitng')
                user_stat.family += family
                user_stat.health += health
                user_stat.unknown += unknown
                user_stat.community_size = self.payload.community_size
                stats_repo.update_stats(user_stat)

            return ResponseSuccess()
        except Exception as e:
            raise HttpException(f'An error occurred while saving statistics: {e}', 401)
