import logging
from dataclasses import dataclass

from uuid import uuid4

from injector import inject

from cfp.domain.common.responses import ResponseSuccess
from cfp.data.statistics.statistics_repository import StatisticsRepository
from cfp.domain.dtos.save_feedback_dto import SaveFeedbackDto
from cfp.domain.common.exceptions import HttpException
from cfp.domain.statistic import Statistic


@dataclass
class ProcessFeedbackCommand:
    payload: SaveFeedbackDto
    current_user_id: str

    logger = logging.getLogger(__name__)

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
                logging.warning(f'No stats has been recorded for {self.payload.community_name}')
                logging.info(f'Adding new Statistic for {self.payload.community_name}')

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
                user_stat.family += family
                user_stat.health += health
                user_stat.unknown += unknown
                user_stat.community_size = self.payload.community_size
                stats_repo.update_stats(user_stat)

                logging.info(f'Update stats for "{self.payload.community_name}" community', user_stat.to_dict())

            return ResponseSuccess()
        except Exception as e:
            raise HttpException(f'An error occurred while saving statistics: {e}', 401)
