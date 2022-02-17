from flask import Flask
from flask_app.datadic import group26_database_dictionary

# DEFINE APP

app = Flask(__name__)

# DEFINE DATABASE CONNECTION

myhost = group26_database_dictionary['endpoint']
myuser = group26_database_dictionary['username']
mypassword = group26_database_dictionary['password']
myport = group26_database_dictionary['port']
mydb = group26_database_dictionary['database']

# ----RUN---- #

if __name__ == "__main__":
    print('Running')
