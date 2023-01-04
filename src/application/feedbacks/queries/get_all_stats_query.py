from dataclasses import dataclass

from injector import inject

from src.application.responses import ResponseSuccess
from src.data.statistics.statistics_repository import StatisticsRepository
from src.domain.exceptions import HttpException


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
