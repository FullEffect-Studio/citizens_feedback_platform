from flask import Flask, jsonify, request, render_template
from flask_restful import Api, Resource
from flask_mongoengine import MongoEngine

from add_controller import Add
from users_controller import UsersController

db = MongoEngine()
app = Flask(__name__)
app.config["MONGODB_SETTINGS"] = [
    {
        "db": "test_db",
        "host": "db",
        "port": 27017,
        "alias": "default",
    }
]
db.init_app(app)
api = Api(app)


print(f'Connecting to {db.name}')
print(f'Using collection {db.user_num_collection}')


db.user_num_collection.insert_one({
    'num_of_users': 0
})


class Visit(Resource):

    def get(self):
        prev_num = db.user_num_collection.find({})[0]['num_of_users']
        new_num = prev_num + 1
        db.user_num_collection.update({}, {"$set": {"num_of_users": new_num}})
        return str(f"Hell user {new_num}")




api.add_resource(Visit, '/')
api.add_resource(Add, '/add')
api.add_resource(UsersController, '/users')


@app.route('/about')
def about():
    return render_template('about.html', company='James Clear')


@app.route('/<name>')
def greet(name):
    return f'Hello {name}'


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
