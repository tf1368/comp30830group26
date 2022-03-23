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

    'forecast':{

                                'number': 'INT'
                                ,'position_long':'REAL'
                                ,'position_lat':'REAL'
                                ,'weather_id':'INTEGER'
                                ,'main':'VARCHAR(256)'
                                ,'description':'VARCHAR(500)'
                                ,'icon':'VARCHAR(20)'

                                ,'temp':'REAL'
                                ,'feels_like':'REAL'
                                ,'temp_min':'REAL'
                                ,'temp_max':'REAL'
                                ,'pressure':'INT'
                                ,'humidity':'INT'
                                ,'visibility':'INT'
                                ,'wind_speed':'REAL'
                                ,'wind_degree':'INT'
                                ,'clouds_all':'INT'
                                ,'forecast_time_ts':'BIGINT'
                                ,'forecast_time_dt':'DATETIME'
                                ,'created_date':'BIGINT'
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
# https://pro.openweathermap.org/data/2.5/forecast/hourly?lat=35&lon=139&appid=9e8e9b03bd9760816f4f624a692d09c4



}
