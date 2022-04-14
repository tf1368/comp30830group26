import pandas as pd
import sqlalchemy as sqla
from flask import Flask, render_template
import json
import pickle
import numpy

# Dictionary for convenience
database_info = {'username': 'group26',
                 'password': '26group1',
                 'database': 'dbikes',
                 'host': 'dbbikes.ccllddmzhx5q.us-east-1.rds.amazonaws.com',
                 'port': '3306'}

# Define app
app = Flask(__name__, template_folder='templates')


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


@app.route("/about")
def about():
    """Return the about Route"""

    return render_template('about.html')


@app.route("/nearest")
def near():
    """Return the near Route"""

    return render_template('nearest.html')


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

        df = pd.read_sql(sql_statement, engine, params={'station_id': station_number})
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

        df = pd.read_sql(sql_statement, engine, params={'station_id': station_number})
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


@app.route("/weather_forecast_time")
def weather_forecast_time():
    """Returns the weather forecast time Json Data of Dublin, prepare for prediction"""

    print("weather_forecast_time() in operation...\n")

    try:
        # Connect to the RDS database
        engine = connect_db_engine(host=database_info['host'],
                                   user=database_info['username'],
                                   password=database_info['password'],
                                   port=database_info['port'],
                                   db=database_info['database'], )

        sql_statement = "SELECT f.number," \
                        "f.temp," \
                        "f.pressure," \
                        "f.humidity," \
                        "f.visibility," \
                        "f.wind_speed," \
                        "f.wind_degree," \
                        "f.clouds_all," \
                        "from_unixtime(f.forecast_time_dt) as Daily " \
                        "FROM forecast as f " \
                        "WHERE f.number = 2 " \
                        "GROUP BY from_unixtime(f.forecast_time_dt) " \
                        "ORDER BY from_unixtime(f.forecast_time_dt) desc"

        df = pd.read_sql(sql_statement, engine)
        # Turn the data into the json
        data_json = df.to_json(orient="records")

    except Exception as e:
        print(e)

    print("weather_forecast_time() finish!\n\n")

    return data_json


@app.route('/prediction/<int:station_number>/<time>')
def predict(station_number, time):
    print("predict() in operation...\n")

    # Connect to the RDS database
    engine = connect_db_engine(host=database_info['host'],
                               user=database_info['username'],
                               password=database_info['password'],
                               port=database_info['port'],
                               db=database_info['database'])

    sql_statement1 = "SELECT s.number, s.name, s.address, s.bike_stands, s.position_lat, " \
                     "s.position_long, a.available_bike_stands, a.available_bikes, " \
                     "MAX(from_unixtime(a.last_update)) AS 'last_update_time', a.created_date AS 'created_date' " \
                     "FROM availability as a " \
                     "INNER JOIN station as s " \
                     "ON s.number = a.number " \
                     "WHERE s.number = %(station_id)s " \
                     "GROUP BY s.number " \
                     "ORDER BY s.number;"
    df1 = pd.read_sql(sql_statement1, engine, params={'station_id': station_number})

    sql_statement2 = "SELECT f.number,f.main," \
                     "avg(f.temp) as Avg_temp," \
                     "avg(f.pressure) as Avg_pressure," \
                     "avg(f.humidity) as Avg_humidity," \
                     "avg(f.visibility) as Avg_visibility," \
                     "avg(f.wind_speed) as Avg_wind_speed," \
                     "avg(f.wind_degree) as Avg_wind_degree," \
                     "avg(f.clouds_all) as Avg_clouds_all," \
                     "date(from_unixtime(f.forecast_time_dt)) as Daily " \
                     "FROM forecast as f " \
                     "WHERE f.number = 2 " \
                     "GROUP BY date(from_unixtime(f.forecast_time_dt)) " \
                     "ORDER BY date(from_unixtime(f.forecast_time_dt)) desc"

    df2 = pd.read_sql(sql_statement2, engine)

    sql_statement3 = "SELECT f.number," \
                     "f.temp," \
                     "f.pressure," \
                     "f.humidity," \
                     "f.visibility," \
                     "f.wind_speed," \
                     "f.wind_degree," \
                     "f.clouds_all," \
                     "from_unixtime(f.forecast_time_dt) as Daily " \
                     "FROM forecast as f " \
                     "WHERE f.number = 2 and f.forecast_time_dt = %(time)s " \
                     "GROUP BY from_unixtime(f.forecast_time_dt) " \
                     "ORDER BY from_unixtime(f.forecast_time_dt) desc"

    df3 = pd.read_sql(sql_statement3, engine, params={'time': time})

    f = open('rfc2.pickle', 'rb')
    rfc1 = pickle.load(f)
    f.close()
    availability_prediction = rfc1.predict([[station_number, df1["bike_stands"], df1["position_lat"],df1["position_long"], 0.965926, 0.258819, df3["temp"],df3["pressure"], df3["humidity"],df3["visibility"], df3["wind_speed"],df3["wind_degree"], df3["clouds_all"], True]])
    prediction_list = availability_prediction.tolist()
    prediction_dict = {"bikes": prediction_list[0]}
    result = json.dumps(prediction_dict)

    # prediction_list = []
    # for i in [3,2,1,0]:
    #availability_prediction = rfc1.predict([[station_number, df1["bike_stands"], df1["position_lat"],
                                             #df1["position_long"], 0.965926, 0.258819, df2.loc[i:i, "Avg_temp"],
                                             #df2.loc[i:i, "Avg_pressure"], df2.loc[i:i, "Avg_humidity"],
                                             #df2.loc[i:i, "Avg_visibility"], df2.loc[i:i, "Avg_wind_speed"],
                                             #df2.loc[i:i, "Avg_wind_degree"], df2.loc[i:i, "Avg_clouds_all"], True]])
    # print(availability_prediction)
    # prediction_list.append(availability_prediction[0])


    # print(prediction_list)
    # prediction_dict = {"Day1": prediction_list[0],"Day2":prediction_list[1],"Day3":prediction_list[2],"Day4":prediction_list[3]}
    # print(prediction_dict)
    # result = json.dumps(prediction_dict, cls=NpEncoder)

    print("predict() finish!\n\n")

    return result


class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (numpy.int_, numpy.intc, numpy.intp, numpy.int8,
                            numpy.int16, numpy.int32, numpy.int64, numpy.uint8,
                            numpy.uint16, numpy.uint32, numpy.uint64)):
            return int(obj)
        elif isinstance(obj, (numpy.float_, numpy.float16, numpy.float32, numpy.float64)):
            return float(obj)
        elif isinstance(obj, (numpy.ndarray,)):  # add this line
            return obj.tolist()  # add this line
        return json.JSONEncoder.default(self, obj)


# Run
if __name__ == "__main__":
    # app.run(debug=True)
    app.run(host="0.0.0.0", port=5000, debug=True)
