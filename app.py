from flask import Flask
from dotenv import load_dotenv

from einsteinzoo.interfaces.handlers import slack

load_dotenv(verbose=True)

app = Flask(__name__)

blueprints = [slack.blueprint]

for blueprint in blueprints:
    app.register_blueprint(blueprint)

if __name__ == '__main__':
    app.run(debug=True)
