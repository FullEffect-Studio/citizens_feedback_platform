import logging
import pprint
from injector import inject

from cfp.data.mongo_base import BaseRepository
from cfp.data.mongo_client import AppMongoClient
from cfp.data.statistics.statistics_data import StatisticData
from cfp.domain.statistic import Statistic

logger = logging.getLogger(__name__)
class StatisticsRepository(BaseRepository):

    @inject
    def __init__(self, client: AppMongoClient):
        super().__init__(client)
        self.statistics = self.client.get_default_database().get_collection('statistics')

    def get_all(self):
        logger.info(f'Getting all stats from database')
        result = self.statistics.find()
        return [
            self._build_stat(data)
            for data in result
        ]

    def get_aggregated_stats(self):
        logger.info(f'Aggregating statistics across all communities and social workers from database')
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
            logger.info(f'Getting statistics by Social Worker {social_worker_id} to database')

            result = self.statistics.find({'social_worker_id': social_worker_id})
            return [self._build_stat(data) for data in result]
        except Exception as e:
            logger.exception(f'[Failed] Getting statistics by Social Worker')
            raise e

    def add_stats(self, domain_stat: Statistic):
        data = domain_stat.to_dict()
        data['id'] = str(domain_stat.id)


        try:
            logger.info(f'Saving new statistics database {domain_stat.to_dict()}')
            model = StatisticData(**data).save()
        except Exception as e:
            logger.exception('[Failed]: To save statistics')
            raise e

    def update_stats(self, domain_stat: Statistic):
        data = domain_stat.to_dict()
        data['id'] = str(domain_stat.id)
        pprint.pprint(data)

        try:
            logger.info(f'Updating stats for  {domain_stat.community_name}')
            self.statistics.update_one(
                filter={'social_worker_id': domain_stat.social_worker_id, 'community_name': domain_stat.community_name},
                update={'$set': {'family': domain_stat.family, 'health': domain_stat.health,
                                 'unknown': domain_stat.unknown, 'community_size': domain_stat.community_size}},
                upsert=True
            )
        except Exception as e:
            logger.exception('[Failed]: To save update stats')
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
            logger.info(f'Getting stats by community and social worker')
            result = self.statistics.find_one({'community_name': community_name, 'social_worker_id': social_worker_id})
            if result is not None:
                return self._build_stat(result)
            return None
        except Exception as e:
            logger.exception(f'[FAILED] Getting stats by community and social worker')
            raise e
