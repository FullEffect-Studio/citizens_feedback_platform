import pytest

from data.repository import mongorepo

pytestmark = pytest.mark.integration


def test_repository_list(
        app_configuration, mg_database, mg_test_data
):
    repo = mongorepo.MongoRepo(app_configuration)

    repo_users = repo.get_all()

    assert set([r.id for r in repo_users]) == set([r['id'] for r in mg_test_data])

