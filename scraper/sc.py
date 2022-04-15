import requests as rq
import sqlalchemy as sqla
import datetime as dt
import time
import pymysql

pymysql.install_as_MySQLdb()

# Dictionary for convenience
database_info = {'username': 'group26',
                 'password': '26group1',
                 'database': 'dbikes',
                 'host': 'dbbikes.ccllddmzhx5q.us-east-1.rds.amazonaws.com',
                 'port': '3306'}

database_schema = {
    'station': {'address': 'VARCHAR(256)',
                'banking': 'INT',
                'bike_stands': 'INT',
                'bonus': 'INT',
                'contract_name': 'VARCHAR(256)',
                'name': 'VARCHAR(256)', 'number': 'INTEGER',
                'position_lat': 'DOUBLE',
                'position_long': 'DOUBLE',
                'created_date': 'BIGINT'},
    'availability': {'number': 'INT',
                     'available_bikes': 'INT',
                     'available_bike_stands': 'INT',
                     'last_update': 'BIGINT',
                     'created_date': 'BIGINT'},
    'weather': {'number': 'INT',
                'position_long': 'DOUBLE',
                'position_lat': 'DOUBLE',
                'weather_id': 'INT',
                'main': 'VARCHAR(256)',
                'description': 'VARCHAR(500)',
                'icon': 'VARCHAR(20)',
                'icon_url': 'VARCHAR(500)',
                'base': 'VARCHAR(256)',
                'temp': 'DOUBLE',
                'feels_like': 'DOUBLE',
                'temp_min': 'DOUBLE',
                'temp_max': 'DOUBLE',
                'pressure': 'INT',
                'humidity': 'INT',
                'visibility': 'INT',
                'wind_speed': 'DOUBLE',
                'wind_degree': 'INT',
                'clouds_all': 'INT',
                'datetime': 'BIGINT',
                'sys_type': 'INT',
                'sys_id': 'INT',
                'sys_country': 'VARCHAR(10)',
                'sys_sunrise': 'BIGINT',
                'sys_sunset': 'BIGINT',
                'sys_type': 'INT',
                'timezone': 'INT',
                'id': 'BIGINT',
                'name': 'VARCHAR(256)',
                'cod': 'INT',
                'created_date': 'BIGINT',
                'availability_last_update': 'BIGINT'},
    # cheng !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    '01_forecast': {

        'number': 'INT'
        , 'position_long': 'REAL'
        , 'position_lat': 'REAL'
        , 'weather_id': 'INTEGER'
        , 'main': 'VARCHAR(256)'
        , 'description': 'VARCHAR(500)'
        , 'icon': 'VARCHAR(20)'

        , 'temp': 'REAL'
        , 'feels_like': 'REAL'
        , 'temp_min': 'REAL'
        , 'temp_max': 'REAL'
        , 'pressure': 'INT'
        , 'humidity': 'INT'
        , 'visibility': 'INT'
        , 'wind_speed': 'REAL'
        , 'wind_degree': 'INT'
        , 'clouds_all': 'INT'
        , 'forecast_time_ts': 'BIGINT'
        , 'forecast_time_dt': 'DATETIME'
        , 'created_date': 'BIGINT'
    }

}

API_info = {
    'DublinBikesAPI': {'Service Provider': 'JCDecaux', 'API Reason': 'Dublin Bikes', 'Security': 'secret',
                       'URL': {'Station': 'https://api.jcdecaux.com/vls/v1/stations',
                               'Contract': 'https://api.jcdecaux.com/vls/v1/contracts',
                               'Park of Contract': 'https://api.jcdecaux.com/parking/v1/contracts/{}/parks',
                               'Park Info': 'https://api.jcdecaux.com/parking/v1/contracts/{}/parks/{}'},
                       'API Key': 'fe21977da86c9f91c9368f54324b41446a413c10'},
    'OpenWeatherAPI': {'Service Provider': 'OpenWeatherMap', 'API Reason': 'Weather Data', 'Security': 'secret',
                       'URL': {'weather_at_coord': 'http://api.openweathermap.org/data/2.5/weather'},
                       'API Key': '4387022fe20300335656359a13903a56'},
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    'OpenWeatherforecastAPI': {'Service Provider': 'OpenWeatherMap', 'API Reason': 'Weather Data', 'Security': 'secret',
                               'URL': {'weather_at_coord': 'https://pro.openweathermap.org/data/2.5/forecast/hourly'},
                               'API Key': '9e8e9b03bd9760816f4f624a692d09c4'}
    # https://pro.openweathermap.org/data/2.5/forecast/hourly?lat={lat}&lon={lon}&appid={API key}
    # api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API key}
    # https://pro.openweathermap.org/data/2.5/forecast/hourly?lat=35&lon=139&appid=9e8e9b03bd9760816f4f624a692d09c4

}


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


# Set up database schema
def setup_db(host, user, password, port, db):
    """function to set up the database if it does not exist."""

    print("setup_db() in operation\n\n")

    engine = connect_db_engine(host, user, password, port, db)
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # !!!!!!!!!!!!!!!!
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


# Request Dublin Bike Data
def request_dbike_data():
    """function to request Dublin bike data from JCDecaux"""

    print("request_dbike_data() in operation...\n")

    dbikes_url = API_info['DublinBikesAPI']['URL']['Station']
    dbikes_key = API_info['DublinBikesAPI']['API Key']
    dbikes_contract = 'dublin'

    # Start to request
    try:
        request_response = rq.get(dbikes_url, params={"apiKey": dbikes_key, "contract": dbikes_contract})
        # Convert the request object to json
        json_text = request_response.json()

    except Exception as e:
        json_text = ''
        print(e)

    print("request_dbike_data() finish!\n\n")

    return json_text


# Request weather data
def request_weather_data(latitude, longitude):
    """function to request weather data from OpenWeather."""

    print("request_weather_data() in operation...\n")

    key = API_info['OpenWeatherAPI']['API Key']
    url = API_info['OpenWeatherAPI']['URL']['weather_at_coord']

    # Start to Request
    try:
        request_response = rq.get(url, params={"lat": latitude, "lon": longitude, "appid": key})
        json_text = request_response.json()

    except Exception as e:
        json_text = ''
        print(e)

    print("request_weather_data() finish!\n\n")

    return json_text


# test！！！！！！！！！！！！！！！！！！！！！！！！！
def request_weatherforecast_data(latitude, longitude):
    """function to request weather data from OpenWeather."""

    print("request_weatherforecast_data()!!!!!bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb!!!!!!!!!!!!!!!!!!!!!! in operation...\n")

    key = API_info['OpenWeatherforecastAPI']['API Key']
    url = API_info['OpenWeatherforecastAPI']['URL']['weather_at_coord']

    # Start to Request
    try:
        request_response = rq.get(url, params={"lat": latitude, "lon": longitude, "appid": key})
        json_text = request_response.json()

    except Exception as e:
        json_text = ''
        print(e)

    print("request_weatherforecast_data()!!!!!!!!!!!!!!!!!!!!!!!aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa finish!\n\n")

    return json_text


# ！！！！！！！！！！！！！

# Retrieve the unique station numbers from the station table
def existing_station(engine):
    """function to check which station are already in the database"""

    print("existing_station() in operation...\n")

    station_list = []

    try:
        result = engine.execute("""SELECT number FROM station""")
        rows = result.fetchall()

        for station_number in rows:
            print(station_number)
            station_list += [station_number[0]]

        result.close()

    except Exception as e:
        station_list = []
        print(e)

    print("existing_station() finish!\n\n")

    return station_list


# Insert data to station, availability and weather table
def insert_station_static_data(bike_json, existing_station, engine):
    """function to insert the data into the database"""

    print("insert_station_static_values() in operation\n\n")
    engine.execute('''DELETE FROM dbikes.forecast''')
    station_list = existing_station
    datetime_now = dt.datetime.now()
    created_date = dt.datetime.timestamp(datetime_now)

    for entry in bike_json:

        address = entry['address']
        name = entry['name']
        contract_name = entry['contract_name']
        banking = int(entry['banking'])
        bonus = int(entry['bonus'])
        bike_stands = entry['bike_stands']
        available_bike_stands = entry['available_bike_stands']
        available_bikes = entry['available_bikes']
        number = entry['number']
        position_lat = entry['position']['lat']
        position_lng = entry['position']['lng']
        last_update = entry['last_update'] / 1000

        # Insert data to station table
        station_insert = '''INSERT INTO station (address, banking, bike_stands, bonus, contract_name, name, number, position_lat
                                                ,position_long, created_date)
                            VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) '''

        if number not in station_list:
            station_data = (
            address, banking, bike_stands, bonus, contract_name, name, number, position_lat, position_lng
            , created_date)
            engine.execute(station_insert, station_data)
            print("station insert finish!\n\n")

        # Insert data to availability table
        availability_insert = '''INSERT INTO availability (number, available_bikes, available_bike_stands, last_update, created_date)
                                VALUES(%s,%s,%s,%s,%s)'''

        availability_data = (number, available_bikes, available_bike_stands, last_update, created_date)

        engine.execute(availability_insert, availability_data)
        print("availability insert finish!\n\n")

        # Insert data to weather table             zmx的
        weather_json = request_weather_data(latitude=str(position_lat), longitude=str(position_lng))

        #               zmx的
        weather_insert = '''INSERT INTO weather(number, position_long, position_lat, weather_id, main, description, icon, base,temp
                                                ,feels_like, temp_min, temp_max, pressure, humidity, visibility, wind_speed, wind_degree
                                                ,clouds_all, datetime, sys_type, sys_id, sys_country, sys_sunrise, sys_sunset
                                                ,timezone, id, name, cod, created_date, availability_last_update)
                            VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
        # !!!!!!!!!!!!

        weather_data = (number,
                        weather_json['coord']['lon'],
                        weather_json['coord']['lat'],
                        weather_json['weather'][0]['id'],
                        weather_json['weather'][0]['main'],
                        weather_json['weather'][0]['description'],
                        weather_json['weather'][0]['icon'],
                        weather_json['base'],
                        weather_json['main']['temp'],
                        weather_json['main']['feels_like'],
                        weather_json['main']['temp_min'],
                        weather_json['main']['temp_max'],
                        weather_json['main']['pressure'],
                        weather_json['main']['humidity'],
                        weather_json['visibility'],
                        weather_json['wind']['speed'],
                        weather_json['wind']['deg'],
                        weather_json['clouds']['all'],
                        weather_json['dt'],
                        weather_json['sys']['type'],
                        weather_json['sys']['id'],
                        weather_json['sys']['country'],
                        weather_json['sys']['sunrise'],
                        weather_json['sys']['sunset'],
                        weather_json['timezone'],
                        weather_json['id'],
                        weather_json['name'],
                        weather_json['cod'],
                        created_date,
                        last_update)

        # ---------------------------------------------
        # !!!!!!!!!!         cyp的
        weatherforecast_json = request_weatherforecast_data(latitude=str(position_lat), longitude=str(position_lng))
        for each_hour_data in weatherforecast_json['list']:
            # Loops through every forecast time at three hour intervals for the next 5 days for the current coordinates and saves it in the database
            forecast_time_dt = each_hour_data['dt']
            forecast_time_txt = each_hour_data['dt_txt']
            weather_id = each_hour_data['weather'][0]['id']
            main = each_hour_data['weather'][0]['main']
            description = each_hour_data['weather'][0]['description']
            icon = each_hour_data['weather'][0]['icon']

            temp = each_hour_data['main']['temp']
            feels_like = each_hour_data['main']['feels_like']
            temp_min = each_hour_data['main']['temp_min']
            temp_max = each_hour_data['main']['temp_max']
            pressure = each_hour_data['main']['pressure']
            humidity = each_hour_data['main']['humidity']
            visibility = each_hour_data['visibility']

            wind_speed = each_hour_data['wind']['speed']
            wind_degree = each_hour_data['wind']['deg']

            clouds_all = each_hour_data['clouds']['all']

            #  weather_insert = '''
      #      DELETE FROM tb_courses_new;
            weatherforecast_insert = '''INSERT INTO forecast(number, position_long, position_lat, weather_id, main, description, icon, temp
                                                    ,feels_like, temp_min, temp_max, pressure, humidity, visibility, wind_speed, wind_degree
                                                    ,clouds_all, forecast_time_dt, forecast_time_txt,created_date)
                                VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
            #   weather_values =
            # !!!  这里有个list
            weatherforecast_data = (number
                                    , position_lng
                                    , position_lat
                                    , weather_id
                                    , main
                                    , description
                                    , icon

                                    , temp
                                    , feels_like
                                    , temp_min
                                    , temp_max
                                    , pressure
                                    , humidity
                                    , visibility
                                    , wind_speed
                                    , wind_degree
                                    , clouds_all
                                    , forecast_time_dt
                                    , forecast_time_txt
                                    , created_date)
           # print(weatherforecast_data)
            engine.execute(weatherforecast_insert, weatherforecast_data)
            print("weather forcaset  insert finish!aaaaaaaaaaaaaaaaaaaaaaaaccccccccccccccccccccccccccccccccccc\n\n")


        engine.execute(weather_insert, weather_data)
        print("weather insert finish!ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo\n\n")

    return


# Wrapper function to pull the data and store it into a database
def main():
    """Main Function"""

    print("main() in operation\n\n")

    #while True:

        # Pull it every five minutes
    try:
            print("\n-------------------------------\n")
            print('''Starting: The time now is: {}'''.format(dt.datetime.now()))

            mysql_engine = connect_db_engine(database_info['host'],
                                             database_info['username'],
                                             database_info['password'],
                                             database_info['port'],
                                             database_info['database'])
            existing_station_list = existing_station(mysql_engine)
            bike_json = request_dbike_data()
            insert_station_static_data(bike_json, existing_station_list, mysql_engine)
            mysql_engine.dispose()

            print("Start to sleep for 5 minutes!\n")
        #    time.sleep(5 * 60)
            print('\n-------zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz-----------------------\n')

    except Exception as e:
            print(e)

    return


# Run Main
if __name__ == '__main__':
    main()

# git clone repo_url
# git add file_name/path to file from root
# git commit -m "my message abput the commit"
# git push
