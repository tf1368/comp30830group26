import sqlalchemy as sqla
from sqlalchemy import create_engine
from flask_app.datadic import database_schema


# Connect to a Database Engine

def connect_db_engine(host, user, password, port, db):
    print("Inside connect_db_engine()\n\n")

    error_code = 0
    engine = ''

    error_dictionary = {0: 'No Error', 1: 'One of the parameters is wrong', 999: 'Uncaught exception'}

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

    print('Database Schema Created, have fun!')
    engine.dispose()

    return
