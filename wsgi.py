import os

from web.app import create_app

env = os.environ['FLASK_CONFIG']
print(f'Executing app in {env} environment')
app = create_app(os.environ['FLASK_CONFIG'])