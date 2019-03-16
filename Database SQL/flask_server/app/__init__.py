# this is the base application file. 
# We import all the needed libraries and prep the server to be exported into run.py
from flask import Flask, g
from flask_cors import CORS
from utils.config import config
from db import connect_db

server = Flask(__name__)
server.secret_key = config['flask_login_secret']
cors = CORS(server, supports_credentials=True)

@server.before_request
def before_request():
    # open a connection to postgresql
    g.db = connect_db()

@server.teardown_request
def teardown_request(exception):
    # check the postgres connection and close it if it exists
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

# The routes to our application are located in the API.
import api
