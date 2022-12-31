from flask import Flask

from web.rest import user


def create_app(config_name):
    app = Flask(__name__)

    config_module = f"web.config.{config_name.capitalize()}Config"

    app.config.from_object(config_module)

    app.register_blueprint(user.blueprint)

    return app

