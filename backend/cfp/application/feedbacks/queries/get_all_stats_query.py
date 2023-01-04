from dataclasses import dataclass

from injector import inject

from cfp.domain.common.responses import ResponseSuccess
from cfp.data.statistics.statistics_repository import StatisticsRepository
from cfp.domain.common.exceptions import HttpException


@dataclass
class GetAllStatsQuery:
    @inject
    def execute(self, stats_repo: StatisticsRepository):

        try:
            user_stat = stats_repo.get_all()
            return ResponseSuccess(value=user_stat.to_dict())
        except Exception as e:
            raise HttpException(f'Failed to query all stats statistics: {e}', 401)
