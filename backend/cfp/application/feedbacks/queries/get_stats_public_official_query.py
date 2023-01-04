from dataclasses import dataclass

from injector import inject

from cfp.data.statistics.statistics_repository import StatisticsRepository
from cfp.domain.common.exceptions import HttpException
from cfp.domain.common.responses import ResponseSuccess


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
