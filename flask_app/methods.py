import sqlalchemy as sqla
import pandas as pd

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


def get_stationinfo(host, user, password, port, db):

    try:
        # Connect to the RDS database
        engine = connect_db_engine(host, user, password, port, db)

        print("get_stationinfo() in operation...\n")

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

    print("get_stationinfo() finish!\n\n")
    return data_json


def get_hourly_data(host, user, password, port, db, station_number):
    try:
        # Connect to the RDS database
        engine = connect_db_engine(host, user, password, port, db)

        print("get_hourly_data() in operation...\n")

        sql_statement = "SELECT s.name, count(a.number)," \
                        "avg(a.available_bike_stands) as Avg_bike_stands," \
                        "avg(a.available_bikes) as Avg_bikes_avail," \
                        "EXTRACT(HOUR FROM from_unixtime(a.last_update)) as Hourly " \
                        "FROM availability as a " \
                        "JOIN station as s " \
                        "ON s.number = a.number " \
                        "WHERE a.number = ${station_number}" \
                        "GROUP BY EXTRACT(HOUR FROM from_unixtime(a.last_update)) " \
                        "ORDER BY EXTRACT(HOUR FROM from_unixtime(a.last_update)) "

        df = pd.read_sql(sql_statement, engine)
        # Turn the data into the json
        data_json = df.to_json(orient="records")

    except Exception as e:
        print(e)

    print("get_hourly_data() finish!\n\n")

    return data_json


def get_current_weather(host, user, password, port, db):
    try:
        # Connect to the RDS database
        engine = connect_db_engine(host, user, password, port, db)

        print("get_current_weather() in operation...\n")

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

    print("get_current_weather() finish!\n\n")

    return data_json

