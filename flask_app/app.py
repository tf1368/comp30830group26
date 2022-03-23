from flask_app.methods import *
from flask_app.datadic_sql import *
from flask import Flask, render_template


# Define app
app = Flask(__name__)

@app.route("/")
@app.route("/home")
@app.route("/index")
def home():
    """Return the Home Route"""

    return render_template('index.html')

@app.route("/stations")
def stations():
    """Returns the station Json Data"""
    print("stations() in operation...\n")
    # Return the station info
    station_json = get_stationinfo(host=database_info['host'],
                                  user=database_info['username'],
                                  password=database_info['password'],
                                  port=database_info['port'],
                                  db=database_info['database'])

    print("stations() finish!\n\n")

    return station_json


# Run
if __name__ == "__main__":
    # app.run(debug=True)
    app.run(host="0.0.0.0", port=5000, debug=True)