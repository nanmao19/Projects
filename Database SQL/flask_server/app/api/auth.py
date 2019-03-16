from flask import current_app, g, redirect, request, session
from datetime import datetime, timedelta

import flask_login
from flask_login import current_user

from app import server
from app.utils import config
import app.db

login_manager = flask_login.LoginManager()
login_manager.init_app(server)

# User class used by flask_login
class User:
    def __init__(self, uid):
        self.uid = uid

    def get_id(self):
        return self.uid

    def is_active(self):
        return True

    def is_authenticated(self):
        return self.authenticated

    def is_anonymous(self):
        return False

#before each request, extend a session
@server.before_request
def extend_session():
    session.permanent = True
    # 1440 minutes = 1 day
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=1440)
    session.modified = True

@login_manager.user_loader
def user_loader(user_id):
    if user_id:
        return User(user_id)
    return

# auth routes will go below

@server.route('/session', methods=['POST'])
def login():
    """
    Creates new session if user credentials validate properly.

    Args:
        email: user's email
        password: user's password
    """
    username = request.form['user_name']
    password = request.form['user_password']

    # Open a cursor to perform database operations
    cur = g.db.cursor()
    # Query the database and obtain data as Python objects
    cur.execute("SELECT username, password FROM regularUser WHERE username = %s AND password = %s;",
            [username, password])

    row = cur.fetchone()

    # if a row is returned from the DB, assign it to a user obj
    # else create a user obj with None for values.
    if len(row) == 1:
        user = {
            'username': row[0],
            'password': row[1]
        }
    else:
        user = {
            'username': None,
            'password': None,
        }

    if user['username'] and password == user['password']:
        flask_login.login_user(User(user['username']))
        cur.close()
        return redirect('/list_item')
    else:
        cur.close()
        return redirect('/login')

@server.route('/session', methods=['DELETE'])
def logout():
    """Destroys current session (if exists) and logs user out.

    TODO: redirecting to register if this doesn't work makes little sense
    we may want to consider other options about the failure case.
    """
    if current_user.is_authenticated:
        flask_login.logout_user()
        return redirect('/login')
    return redirect('/register')
