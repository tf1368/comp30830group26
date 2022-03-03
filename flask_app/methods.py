import sqlalchemy as sqla
import pandas as pd
import time
import pprint
from flask_app.datadic import *


# Connect to a Database Engine

def connect_db_engine(host, user, password, port, db):
    print("Inside connect_db_engine()\n\n")

    error_code = 0
    engine = ''

    try:
        connect_statement = 'mysql+mysqlconnector://{}:{}@{}:{}/{}'.format(user, password, host, port, db)
        print(connect_statement)
        engine = sqla.create_engine(connect_statement, echo=True)

    except Exception as e:
        error_code = 999
        print(e)

    return [error_code, engine]


# Set up the Database Schema and all related functions (e.g. foreign keys, primary keys)

def setup_database(host, user, password, port, db):
    """Set up the database if it does not already exist.

    Input is the database parameters and database_dictionary
    """

    print("Inside setup_database()\n\n")

    engine_l = connect_db_engine(host, user, password, port, db)
    engine = engine_l[1]

    create_sql = """CREATE DATABASE IF NOT EXISTS {}""".format(db)

    engine.execute(create_sql)

    # Loop through every table
    for table, columns in database_schema.items():
        column_count = 0
        column_number = len(columns)
        insert_sql = ''
        insert_sql = """CREATE TABLE IF NOT EXISTS {} (\n""".format(table)
        insert_row = ''

        # for every column and type add on a statement
        for column_name, column_type in columns.items():

            # Add the statement with , in front
            if column_count > 0:
                insert_row += ",{}     {}".format(column_name, column_type)

            # First column
            else:
                insert_row += "{}     {}".format(column_name, column_type)
                column_count += 1

        insert_sql += '{})'.format(insert_row)

        # Start this madness re: creating and inserting the schema
        try:
            engine.execute(insert_sql)

        # Except for something; probably the schema
        except Exception as exc:
            print(exc)

    print('Database Schema Created Successful!')
    engine.dispose()

    return


# Get Stations


def station_table_df(host, user, password, port, db):
    """Retrieve the station table.

    Return table as dataframe
    """

    print("Inside setup_database()\n\n")

    engine_l = connect_db_engine(host, user, password, port, db)
    engine = engine_l[1]
    df = pd.DataFrame()

    # no error
    try:
        df = pd.read_sql(SQL_select_station, engine)

    except Exception as e:
        print(e)

    engine.dispose()

    return df


def get_stations_json(host, user, password, port, db):
    """Returns the stations table as a json string
    The other functions can just call this instead of re-using the code in each function"""

    engine_l = connect_db_engine(host, user, password, port, db)
    engine = engine_l[1]

    print("in get_stations_json()")
    df = pd.read_sql_table("01_station", engine)
    station_json = df.to_json(orient="records")
    print("station data type:", type(station_json))
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(station_json)
    print()
    return station_json


def requestStationData(host, user, password, port, db):
    """A function to Request Station Data and Output as Json"""

    engine_l = connect_db_engine(host, user, password, port, db)
    engine = engine_l[1]

    # Read sql database table into a dataframe
    df = pd.read_sql_table("01_station", engine)

    print(df.iloc[1])
    # Convert to JSON string
    stationJSON = df.to_json(orient="records")

    return stationJSON


def requestStationSQLAData(host, user, password, port, db):
    """A function to request Station Data using SQLAlchemy
    Returns Keys"""

    engine_l = connect_db_engine(host, user, password, port, db)
    engine = engine_l[1]

    metadata = sqla.MetaData()
    station_data = sqla.Table('01_station', metadata, autoload=True, autoload_with=engine)

    print(station_data.columns.keys())


# Get Availability


def availability_table_df(host, user, password, port, db):
    """Retrieve the station table.

    Return table as dataframe
    """

    print("Inside setup_database()\n\n")

    engine_l = connect_db_engine(host, user, password, port, db)
    engine = engine_l[1]
    df = pd.DataFrame()

    # no error
    try:
        df = pd.read_sql(SQL_select_availability, engine)

    except Exception as e:
        print(e)

    engine.dispose()

    return df


def availability_limit_df(host, user, password, port, db):
    """A function to pull the top 109 last updated availability stuff

    Returns a Json Dump of result
    """

    print("IN AVAILABILITY FUNCTION")

    engine_l = connect_db_engine(host, user, password, port, db)
    engine = engine_l[1]
    result = engine.execute(SQL_select_limit_availability)

    print("type of sql request is", type(result))

    for number, available_bikes, available_bike_stands, last_update, created_date in result:
        print("number is:", number, "available bikes is:", available_bikes, "available_bike_stands is:",
              available_bike_stands, "last update is:", last_update, "created date is:", created_date)

    # frontend=json.dumps(result)
    engine.dispose()
    return 'Check JSON DUMPS'


def availability_recentUpdate(host, user, password, port, db):
    """Availability from SQL Alchemy Most recent Update limiting 109"""

    engine_l = connect_db_engine(host, user, password, port, db)
    engine = engine_l[1]

    try:
        engine.connect()

    except Exception as E:
        print(E)

    metadata = sqla.MetaData()
    availability_data = sqla.Table('01_availability', metadata, autoload=True, autoload_with=engine)
    query = sqla.select([availability_data]).order_by(sqla.desc(availability_data.columns.created_date)).limit(109)
    df = pd.read_sql_query(query, engine)
    print(df.iloc[:10])
    try:
        engine.dispose()
    except:
        df = pd.DataFrame()

    return df


# Get Station and Availability Data


def station_availability_df(host, user, password, port, db):
    """Retrieve the station table.

    Return table as dataframe
    """

    print("Inside setup_database()\n\n")

    engine_l = connect_db_engine(host, user, password, port, db)
    engine = engine_l[1]
    df = pd.DataFrame()

    # no error
    df = pd.read_sql(SQL_select_station_avail, engine)

    engine.dispose()

    return df


def station_availability_last_update_table_df(host, user, password, port, db):
    """Retrieve the station table.

    Return table as dataframe
    """

    print("Inside setup_database()\n\n")

    engine_l = connect_db_engine(host, user, password, port, db)
    engine = engine_l[1]
    df = pd.DataFrame()

    # no error
    try:
        df = pd.read_sql(SQL_select_station_avail_latest_update, engine)

    except Exception as e:
        print(e)

    engine.dispose()

    return df


# Get Station and Availability And Weather Data

def station_availability_weather_table_df(host, user, password, port, db):
    """This function pulls the station, weather, availability data.

    Note: This is very time intensive. Use this to pass to other summary functions"""

    print("Inside pull_station_weather_availability_data(host,user,password,port,scraper)")

    # Possible Errors
    error_dictionary = {0: 'No Error'
        , 1: 'The database failed to connect'
        , 2: "The query is not a valid string"
        , 3: "The returned database is empty"
        , 999: 'Uncaught exception'
                        }

    # Set up a default value to return
    data_df = pd.DataFrame()

    error_code = 0

    # Configure the SQL statement
    sql_statement = SQL_select_station_avail_weather

    time_statement = "The retrieval from the database took: {} (ns)"

    # Begin try
    try:
        engine_l = connect_db_engine(host, user, password, port, db)
        engine = engine_l[1]

        # No error connecting to engine
        if engine_l[0] == 0:

            # String
            if type(sql_statement) == str and len(sql_statement) > 0:

                # Begin counter
                start_time = time.perf_counter_ns()
                data_df = pd.read_sql(sql_statement, engine)
                end_time = time.perf_counter_ns()
                engine.dispose()

                # Performance measurement
                print(time_statement.format(end_time - start_time))

                # Dataframe is empty
                if len(data_df) == 0:
                    error_code = 3
                    error_message = error_dictionary[error_code]

            # Invalid SQL Statement
            else:
                error_code = 2
                error_message = error_dictionary[error_code]

        else:
            error_code = 1
            error_message = error_dictionary[error_code]

    except Exception as e:
        error_code = 999
        print("Unexpected failure: {}".format(e))

    return data_df


def station_availability_weather_table_latest_df(host, user, password, port, db):
    """Retrieve the station table.

    Return table as dataframe
    """

    print("Inside setup_database()\n\n")

    engine_l = connect_db_engine(host, user, password, port, db)
    engine = engine_l[1]
    df = pd.DataFrame()

    # no error
    df = pd.read_sql(
        SQL_select_avail_weather_conditional.format(SQL_select_availability_last_update, SQL_select_weather), engine)

    engine.dispose()

    return df


def availability_table_for_station_df(host, user, password, port, db, station_no):
    """Retrieve the station table.

    Return table as dataframe
    """

    print("Inside setup_database()\n\n")

    engine_l = connect_db_engine(host, user, password, port, db)
    engine = engine_l[1]
    df = pd.DataFrame()

    # no error
    try:
        df = pd.read_sql(SQL_select_availability_where_number.format(station_no), engine)

    except Exception as e:
        print(e)

    engine.dispose()

    return df


def weather_last_update_df(host, user, password, port, db):
    """Retrieve weather last update.
    Return table as dataframe
    """

    print("Inside setup_database()\n\n")

    engine_l = connect_db_engine(host, user, password, port, db)
    engine = engine_l[1]
    df = pd.DataFrame()

    # no error
    try:
        df = pd.read_sql(SQL_select_weather_last_update, engine)

    except Exception as e:
        print(e)

    engine.dispose()

    return df

