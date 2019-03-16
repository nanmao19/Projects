# This is the entry point for the application, 
# here we import our app and the api routes and 
# run the app.
from app import server
import app.api

if __name__ == '__main__':
    server.run(debug=True, host='localhost')
