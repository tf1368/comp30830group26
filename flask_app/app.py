from flask import Flask
from flask_app.datadic import group26_database_dictionary
from flask_app.tests import run_tests

# 01. DEFINE APP

app = Flask(__name__)

# 02.DEFINE DATABASE CONNECTION

myhost = group26_database_dictionary['endpoint']
myuser = group26_database_dictionary['username']
mypassword = group26_database_dictionary['password']
myport = group26_database_dictionary['port']
mydb = group26_database_dictionary['database']

# ----RUN---- #

if __name__ == "__main__":
    print('Running')
    test_result = run_tests(host=myhost, user=myuser, password=mypassword, port=myport, db=mydb)

    # Check if the python test cases run alright
    if test_result:
        app.run(debug=True, port=5000)
