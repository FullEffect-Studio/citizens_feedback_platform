import pprint
from typing import List
from injector import inject

from data.mongo_base import BaseRepository, AppMongoClient
from data.statistics.statistics_data import StatisticData
from domain.statistic import Statistic


class StatisticsRepository(BaseRepository):
    @inject
    def __init__(self, client: AppMongoClient):
        super().__init__(client)
        self.statistics = self.client.get_default_database().get_collection('statistics')

    def get_all(self):
        result = self.statistics.find()
        return [
            self._build_stat(data)
            for data in result
        ]

    def get_aggregated_stats(self):
        pipeline = [
            {
                "$group": {
                    "_id": None,
                    "family": {"$sum": "$family"},
                    "health": {"$sum": "$health"},
                    "unknown": {"$sum": "$unknown"}
                }
            }
        ]
        result = self.statistics.aggregate(pipeline)
        result_dict = next(result)
        data = {
            "family": result_dict['family'],
            "health": result_dict['health'],
            "unknown": result_dict['unknown']
        }
        return data

    def get_stats_by_social_worker(self, social_worker_id):
        try:
            result = self.statistics.find({'social_worker_id': social_worker_id})
            print(result)
            return [self._build_stat(data) for data in result]
        except Exception as e:
            print(e)
            raise e

    def add_stats(self, domain_stat: Statistic):
        data = domain_stat.to_dict()
        data['id'] = str(domain_stat.id)
        # pprint.pprint(data)

        try:
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
                filter={'social_worker_id': domain_stat.social_worker_id, 'community_name': domain_stat.community_name},
                update={'$set': {'family': domain_stat.family, 'health': domain_stat.health,
                                 'unknown': domain_stat.unknown, 'community_size': domain_stat.community_size}},
                upsert=True
            )
        except Exception as e:
            print(e)
            raise e

    def _build_stat(self, result):
        return Statistic(
            id=result['_id'],
            community_size=result['community_size'],
            community_name=result['community_name'],
            social_worker_id=result['social_worker_id'],
            family=result['family'],
            health=result['health'],
            unknown=result['unknown'],
        )

    def get_stats_by_community_and_social_worker(self, community_name: str, social_worker_id: str):
        try:
            result = self.statistics.find_one({'community_name': community_name, 'social_worker_id': social_worker_id})
            if result is not None:
                return self._build_stat(result)
            return None
        except Exception as e:
            raise e
