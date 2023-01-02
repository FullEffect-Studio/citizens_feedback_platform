import pymongo
import pytest

from domain.user import UserRole


@pytest.fixture(scope='session')
def mg_database_empty(app_configuration):
    client = pymongo.MongoClient(
        host=app_configuration['MONGODB_HOSTNAME'],
        port=int(app_configuration['MONGODB_PORT']),
        username=app_configuration['MONGODB_USER'],
        password=app_configuration['MONGODB_PASSWORD'],
        authSource='admin'
    )

    db = client[app_configuration['APPLICATION_DB']]

    yield db

    client.drop_database(app_configuration['APPLICATION_DB'])
    client.close()


@pytest.fixture(scope='function')
def mg_test_data():
    return [
        {
            "id": "f853578c-fc0f-4e65-81b8-566c5dffa35a",
            "username": "Danquah",
            "password": "pass111",
            "role": UserRole.PUBLIC_OFFICIAL
        },
        {
            "id": "fe2c3195-aeff-487a-a08f-e0bdc0ec6e9a",
            "username": "Fahrid",
            "password": "pass222",
            "role": UserRole.PUBLIC_OFFICIAL
        },
        {
            "id": "913694c6-435a-4366-ba0d-da5334a611b2",
            "username": "Yau",
            "password": "pass333",
            "role": UserRole.ADMIN
        },

        {
            "id": "913694c6-435a-4366-ba0d-da5334a611b2",
            "username": "Lowe",
            "password": "pass444",
            "role": UserRole.COMMUNITY_SOCIAL_WORKER
        },
    ]


@pytest.fixture(scope='function')
def mg_database(mg_database_empty, mg_test_data):
    collection = mg_database_empty.users

    collection.insert_many(mg_test_data)

    yield mg_database_empty

    collection.delete_many({})


