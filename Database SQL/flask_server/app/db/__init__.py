import psycopg2

from ..utils.config import config

def connect_db():
    """Connects to the specific database."""
    # Connect to an existing database
    conn = psycopg2.connect(config['DATABASE'])
    return conn

