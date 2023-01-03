import pprint

from data.mongo_base import BaseRepository, AppMongoClient
from data.statistics.statistics_data import StatisticData
from domain.statistic import Statistic


class StatisticsRepository(BaseRepository):
    def __init__(self, client: AppMongoClient):
        super().__init__(client)
        self.statistics = self.client.get_default_database().get_collection('statistics')

    def list(self):
        result = self.statistics.find()
        return [
            q
            for q in result
        ]

    def get_stats_by_social_worker(self, social_worker_id) -> Statistic:
        try:
            result = self.statistics.find_one({'social_worker_id': social_worker_id})
            if result is not None:
                return Statistic(
                    id=result['_id'],
                    social_worker_id=result['social_worker_id'],
                    family=result['family'],
                    health=result['health'],
                    unknown=result['unknown'],
                )
            return None
        except Exception as e:
            raise e

    def add_stats(self, domain_stat: Statistic):
        data = domain_stat.to_dict()
        data['id'] = str(domain_stat.id)
        pprint.pprint(data)

        try:
            print(StatisticData(**data))
            model = StatisticData(**data).save()
        except Exception as e:
            print(e)
            raise e

    def update_stats(self, domain_stat: Statistic):
        data = domain_stat.to_dict()
        data['id'] = str(domain_stat.id)
        pprint.pprint(data)

        try:
            self.statistics.update_one(
                filter={'social_worker_id': domain_stat.social_worker_id},
                update={'$set': {'family': domain_stat.family, 'health': domain_stat.health, 'unknown': domain_stat.unknown}},
                upsert=True
            )
        except Exception as e:
            print(e)
            raise e



