from flask import Flask
from server.api import api
from server.api.config import config

# Run this file to start your personal MVS server
#
# Standard host = 127.0.0.1 or `localhost`
# Standard port = 80

app = Flask(__name__, template_folder="templates")
api = api.api(app, host=config.getHost(), port=config.getPort())

api.routing()
