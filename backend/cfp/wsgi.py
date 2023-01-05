import os

from cfp.web.app import create_app

try:
    env = os.environ['FLASK_CONFIG']
    print(f'Executing app in {env} environment')
except KeyError:
    # print('FLASK_CONFIG env variable was not found.')
    # print('Defaulting to development environment')

    env = 'development'

app = create_app(env)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

