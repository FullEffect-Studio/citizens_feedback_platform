from dataclasses import dataclass

from injector import inject

from cfp.data.statistics.statistics_repository import StatisticsRepository
from cfp.domain.common.exceptions import HttpException
from cfp.domain.common.responses import ResponseSuccess


@dataclass
class GetStatBySocialWorkerQuery:
    current_user_id: str

    @inject
    def execute(self, stats_repo: StatisticsRepository):
        try:
            user_stats = stats_repo.get_stats_by_social_worker(self.current_user_id)
            results = [stat.to_dict() for stat in user_stats]
            return ResponseSuccess(value=results)
        except Exception as e:
            raise HttpException(f'Failed to query social worker statistics: {e}', 401)
