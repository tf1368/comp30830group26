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
                        "MAX(a.last_update) AS 'current_availability' " \
                        "FROM availability as a " \
                        "INNER JOIN station as s " \
                        "ON s.number = a.number " \
                        "GROUP BY s.number " \
                        "ORDER BY s.number;"

        df = pd.read_sql(sql_statement, engine)

    except Exception as e:
        print(e)


    # Turn the data into the json
    data_json = df.to_json(orient="records")

    print("get_stationinfo() finish!\n\n")
    return data_json