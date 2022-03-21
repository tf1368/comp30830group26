from flask_app import app
from flask import render_template
import json
from flask_app.methods import *


@app.route("/")
@app.route("/home")
@app.route("/index")
def home():
    """Return the Home Route"""
    station_data = station_availability_last_update_df(host = database_info['host'],
                                                             user = database_info['username'],
                                                             password = database_info['password'],
                                                             port = database_info['port'],
                                                             db = database_info['database'])

    # Turn the dataframe into the json
    station_data_json = station_data.to_json(orient="records")

    # Load the json into the front end
    stationData = json.loads(station_data_json)
    # This sorts the list station dictionaries by name so the selector will be ordered alphabetically
    stationDataSorted = sorted(stationData, key=lambda i: i['name'])

    # Convert all station names to title case
    for station in stationDataSorted:
        station['name'] = station['name'].title()
    return render_template('index.html', station_data=stationDataSorted)


@app.route("/stations")
def station():
    """Return the station Json Data"""

    # Return the station info
    station = station_availability_last_update_df(host = database_info['host'],
                                                  user = database_info['username'],
                                                  password = database_info['password'],
                                                  port = database_info['port'],
                                                  db = database_info['database'])

    # Turn it into json
    station_data_json = station.to_json(orient="records")

    # Convert all names to title case
    # First convert to a dictionary to make for easier looping
    stationDataDict = json.loads(station_data_json)
    for station in stationDataDict:
        station['name'] = station['name'].title()

    # Convert back to a json string before returning
    station_data_json = json.dumps(stationDataDict)

    return station_data_json


@app.route("/availability")
def availability_request():
    """Return a dataframe of the station and availability data"""

    result = station_availability_last_update_df(host = database_info['host'],user = database_info['username'],
                                                 password = database_info['password'],port = database_info['port'],
                                                 db = database_info['database'])

    return result


@app.route("/current_weather")
def current_weather_request():
    """Return JSON string of current weather-type"""

    result = weather_last_update_df(host = database_info['host'],user = database_info['username'],
                                    password = database_info['password'],port = database_info['port'],
                                    db = database_info['database'])
    weather_desc = result[["main", "icon"]]
    weather_mode = weather_desc.mode()
    weather_mode = weather_mode.to_json(orient="records")

    return weather_mode