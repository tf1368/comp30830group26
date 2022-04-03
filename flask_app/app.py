import pandas as pd
import sqlalchemy as sqla
from flask import Flask, render_template
from flask_app.datadic_sql import *

# Define app
app = Flask(__name__)


# Connect to a database engine
def connect_db_engine(host, user, password, port, db):
    print("connect_db_engine() in operation...\n")
    engine = ''

    try:
        connection = 'mysql+mysqldb://{}:{}@{}:{}/{}'.format(user, password, host, port, db)
        print(connection)
        engine = sqla.create_engine(connection, echo=True)

    except Exception as e:
        print(e)

    print("connect_db_engine() finish!\n\n")
    return engine


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

    try:
        # Connect to the RDS database
        engine = connect_db_engine(host=database_info['host'],
                                   user=database_info['username'],
                                   password=database_info['password'],
                                   port=database_info['port'],
                                   db=database_info['database'])

        sql_statement = "SELECT s.number, s.name, s.address, s.position_lat, " \
                        "s.position_long, a.available_bike_stands, a.available_bikes, " \
                        "MAX(from_unixtime(a.last_update)) AS 'last_update_time', a.created_date AS 'created_date' " \
                        "FROM availability as a " \
                        "INNER JOIN station as s " \
                        "ON s.number = a.number " \
                        "GROUP BY s.number " \
                        "ORDER BY s.number;"
        df = pd.read_sql(sql_statement, engine)
        # Turn the data into the json
        data_json = df.to_json(orient="records")

    except Exception as e:
        print(e)

    print("stations() finish!\n\n")

    return data_json


# noinspection PyCallingNonCallable
@app.route('/hourly/<int:station_number>')
def hourly(station_number):
    """Returns the hourly Json Data"""

    print("hourly() in operation...\n")

    try:
        # Connect to the RDS database
        engine = connect_db_engine(host=database_info['host'],
                                   user=database_info['username'],
                                   password=database_info['password'],
                                   port=database_info['port'],
                                   db=database_info['database'])

        sql_statement = "SELECT a.number,s.name," \
                        "avg(a.available_bike_stands) as Avg_bike_stands," \
                        "avg(a.available_bikes) as Avg_bikes_avail," \
                        "EXTRACT(HOUR FROM from_unixtime(a.last_update)) as Hourly " \
                        "FROM availability as a " \
                        "JOIN station as s " \
                        "ON s.number = a.number " \
                        "WHERE a.number = %(station_id)s " \
                        "GROUP BY EXTRACT(HOUR FROM from_unixtime(a.last_update)) " \
                        "ORDER BY EXTRACT(HOUR FROM from_unixtime(a.last_update)) asc"

        df = pd.read_sql(sql_statement, engine, params = {'station_id':station_number})
        # Turn the data into the json
        data_json = df.to_json(orient="records")

    except Exception as e:
        print(e)

    print("hourly() finish!\n\n")

    return data_json


@app.route('/daily/<int:station_number>')
def daily(station_number):
    """Returns the hourly Json Data"""

    print("daily() in operation...\n")

    try:
        # Connect to the RDS database
        engine = connect_db_engine(host=database_info['host'],
                                   user=database_info['username'],
                                   password=database_info['password'],
                                   port=database_info['port'],
                                   db=database_info['database'])

        sql_statement = "SELECT s.name, avg(a.available_bike_stands) as Avg_bike_stands, " \
                        "avg(a.available_bikes) as Avg_bikes_free, " \
                        "DAYNAME(from_unixtime(a.last_update)) as DayName " \
                        "FROM availability as a " \
                        "JOIN station as s " \
                        "ON s.number = a.number " \
                        "WHERE s.number = %(station_id)s " \
                        "GROUP BY s.name , DayName " \
                        "ORDER BY s.name , DayName;"

        df = pd.read_sql(sql_statement, engine, params = {'station_id':station_number})
        # Turn the data into the json
        data_json = df.to_json(orient="records")

    except Exception as e:
        print(e)

    print("daily() finish!\n\n")

    return data_json


@app.route('/current_weather')
def current_weather():
    """Returns the current weather Json Data of Dublin"""

    print("current_weather() in operation...\n")

    try:
        # Connect to the RDS database
        engine = connect_db_engine(host=database_info['host'],
                                   user=database_info['username'],
                                   password=database_info['password'],
                                   port=database_info['port'],
                                   db=database_info['database'], )

        sql_statement = "SELECT w.number,w.position_long,w.position_lat," \
                        "w.main,w.description,w.icon,w.temp,w.feels_like," \
                        "FROM_UNIXTIME(w.created_date) " \
                        "FROM (SELECT w.number,MAX(w.created_date) as created_date FROM weather as w GROUP BY w.number) as max_weath " \
                        "INNER JOIN weather as w " \
                        "ON max_weath.created_date = w.created_date AND max_weath.number = w.number"

        df = pd.read_sql(sql_statement, engine)
        # Turn the data into the json
        data_json = df.to_json(orient="records")

    except Exception as e:
        print(e)

    print("current_weather() finish!\n\n")

    return data_json

@app.route("/weather_forecast")
def weather_forecast():
    """Returns the weather forecast Json Data of Dublin"""

    print("weather_forecast() in operation...\n")

    try:
        # Connect to the RDS database
        engine = connect_db_engine(host=database_info['host'],
                                   user=database_info['username'],
                                   password=database_info['password'],
                                   port=database_info['port'],
                                   db=database_info['database'], )

        sql_statement = "SELECT f.number,f.main," \
                        "avg(f.feels_like) as Avg_temp," \
                        "avg(f.wind_speed) as Avg_wind_speed," \
                        "date(from_unixtime(f.forecast_time_dt)) as Daily " \
                        "FROM forecast as f " \
                        "WHERE f.number = 2 " \
                        "GROUP BY date(from_unixtime(f.forecast_time_dt)) " \
                        "ORDER BY date(from_unixtime(f.forecast_time_dt)) desc"


        df = pd.read_sql(sql_statement, engine)
        # Turn the data into the json
        data_json = df.to_json(orient="records")

    except Exception as e:
        print(e)

    print("forecast_weather() finish!\n\n")

    return data_json


# Run
if __name__ == "__main__":
    # app.run(debug=True)
    app.run(host="0.0.0.0", port=5000, debug=True)
