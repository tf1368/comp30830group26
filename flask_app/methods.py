import sqlalchemy as sqla
import pandas as pd
import time
from flask_app.datadic_sql import *


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


def setup_db(host, user, password, port, db):
    """function to set up the database if it does not exist."""

    print("setup_db() in operation\n\n")

    engine = connect_db_engine(host, user, password, port, db)

    create_sql = f"""CREATE DATABASE IF NOT EXISTS {db}"""

    engine.execute(create_sql)

    # Loop through every table
    for table, columns in database_schema.items():
        insert_sql = f"""CREATE TABLE IF NOT EXIST {table}"""
        insert_row = ''
        column_count = 0

        # Add on a statement for every column and type
        for column_name, column_type in columns.items():

            if column_count > 0:
                insert_row += ",{}{}".format(column_name, column_type)
                # First column do not need , in front
            else:
                insert_row += "{}{}".format(column_name, column_type)
                column_count += 1
                insert_sql += '{}'.format(insert_row)

        # Start creating and inserting the schema
        try:
            engine.execute(insert_sql)

        except Exception as e:
            print(e)

    print('Database Schema Created, have fun!')
    engine.dispose()

    return


# Get Stations
def station_df(host, user, password, port, db):
    """Retrieve the station table and return table as dataframe"""

    print("station_table_df() in operation...\n")

    engine = connect_db_engine(host, user, password, port, db)
    df = pd.DataFrame()

    try:
        df = pd.read_sql(SQL_select_station, engine)

    except Exception as e:
        print(e)

    engine.dispose()

    return df


# Get Availability
def availability_df(host, user, password, port, db):
    """Retrieve the availability table and return table as dataframe"""

    print("availability_table_df() in operation...\n")

    engine = connect_db_engine(host, user, password, port, db)
    df = pd.DataFrame()

    try:
        df = pd.read_sql(SQL_select_availability, engine)

    except Exception as e:
        print(e)

    engine.dispose()

    return df


# Get Station and Availability Data
def station_availability_df(host, user, password, port, db):
    """Retrieve the station and availability table and return table as dataframe"""

    print("availability_table_df() in operation...\n")

    engine = connect_db_engine(host, user, password, port, db)

    df = pd.read_sql(SQL_select_station_avail, engine)

    engine.dispose()

    return df


def station_availability_last_update_df(host, user, password, port, db):
    """Retrieve the station and last update availability info for each station and return table as dataframe"""

    print("station_availability_last_update_df() in operation...\n")

    engine = connect_db_engine(host, user, password, port, db)
    df = pd.DataFrame()

    try:
        df = pd.read_sql(SQL_select_station_avail_latest_update, engine)

    except Exception as e:
        print(e)

    engine.dispose()

    return df


# Get Station and Availability And Weather Data
def station_availability_weather_df(host, user, password, port, db):
    """This function pulls the station, weather, availability data.(time intensive)"""

    print("station_availability_weather_df() in operation...\n")

    # Set up a default value to return
    data_df = pd.DataFrame()

    time_statement = "The retrieval from the database took: {} (ns)"

    # Begin try
    try:
        engine = connect_db_engine(host, user, password, port, db)

        start_time = time.perf_counter_ns()
        data_df = pd.read_sql(SQL_select_station_avail_weather, engine)
        end_time = time.perf_counter_ns()
        engine.dispose()

        print(time_statement.format(end_time - start_time))

    except Exception as e:
        print(e)

    return data_df


def station_availability_weather_latest_df(host, user, password, port, db):
    """Retrieve the availability and weather table on condition. Return table as dataframe"""

    print("station_availability_weather_latest_df() in operation...\n")

    engine = connect_db_engine(host, user, password, port, db)

    df = pd.read_sql(
        SQL_select_avail_weather_conditional.format(SQL_select_availability_last_update, SQL_select_weather), engine)

    engine.dispose()

    return df


def availability_table_for_station_df(host, user, password, port, db, station_no):
    """Retrieve the availability table.Return table as dataframe"""

    print("availability_table_for_station_df() in operation...\n")

    engine = connect_db_engine(host, user, password, port, db)
    df = pd.DataFrame()

    try:
        df = pd.read_sql(SQL_select_availability_where_number.format(station_no), engine)

    except Exception as e:
        print(e)

    engine.dispose()

    return df


def weather_last_update_df(host, user, password, port, db):
    """Retrieve weather last update.Return table as dataframe
    """

    print("weather_last_update_df() in operation...\n")

    engine = connect_db_engine(host, user, password, port, db)
    df = pd.DataFrame()

    try:
        df = pd.read_sql(SQL_select_weather_last_update, engine)

    except Exception as e:
        print(e)

    engine.dispose()

    return df

