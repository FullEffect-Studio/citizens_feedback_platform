from dataclasses import dataclass

from injector import inject

from src.application.responses import ResponseSuccess
from src.data.statistics.statistics_repository import StatisticsRepository
from src.domain.exceptions import HttpException


@dataclass
class GetStatsPublicOfficialQuery:

    @inject
    def execute(self, stats_repo: StatisticsRepository):

        try:
            all_stats = stats_repo.get_all()
            aggregates = stats_repo.get_aggregated_stats()

            result = {
                'aggregates': aggregates,
                'all_stats': [stat.to_dict() for stat in all_stats]
            }
            return ResponseSuccess(value=result)
        except Exception as e:
            raise HttpException(f'Failed to query all stats statistics: {e}', 401)
