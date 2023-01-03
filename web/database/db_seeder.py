import pymongo
from werkzeug.security import generate_password_hash

from domain.user import UserRole

USERS = [
    {
        "_id": "f853578c-fc0f-4e65-81b8-566c5dffa35a",
        "username": "Bernard",
        "password": generate_password_hash("qwe123!"),
        "role": UserRole.ADMIN
    },
]


def db_seeder(db_uri):
    client = pymongo.MongoClient(db_uri)
    db = client.get_default_database()

    collection = db.users
    results = collection.find()

    users = [user for user in results]

    if len(users) == 0:
        collection.insert_many(USERS)
        print('Database seeding completed!!!')
        return

    print(f'Database already have {len(users)} users. Skipping seed operation...')

