group26_database_dictionary={
                        'username':'group26'
                        ,'password':'26group1'
                        ,'database':'dbikes'
                        ,'endpoint':'dbikes.cilfi4edpsps.eu-west-1.rds.amazonaws.com'
                        ,'port':'3306'
                    }

database_schema = {
    '01_station': {
        'address': 'VARCHAR(256)'
        , 'banking': 'INTEGER'
        , 'bike_stands': 'INTEGER'
        , 'bonus': 'INTEGER'
        , 'contract_name': 'VARCHAR(256)'
        , 'name': 'VARCHAR(256)'
        , 'number': 'INTEGER'
        , 'position_lat': 'REAL'
        , 'position_long': 'REAL'
        , 'created_date': 'BIGINT'
    }
    , '01_availability': {
        'number': 'INTEGER'
        , 'available_bikes': 'INTEGER'
        , 'available_bike_stands': 'INTEGER'
        , 'last_update': 'BIGINT'
        , 'created_date': 'BIGINT'
    }

    , '01_weather': {
        'number': 'INT'
        , 'position_long': 'REAL'
        , 'position_lat': 'REAL'
        , 'weather_id': 'INTEGER'
        , 'main': 'VARCHAR(256)'
        , 'description': 'VARCHAR(500)'
        , 'icon': 'VARCHAR(20)'
        , 'icon_url': 'VARCHAR(500)'
        , 'base': 'varchar(256)'
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
        , 'datetime': 'BIGINT'
        , 'sys_id': 'INT'
        , 'sys_country': 'VARCHAR(10)'
        , 'sys_sunrise': 'BIGINT'
        , 'sys_sunset': 'BIGINT'
        , 'sys_type': 'INT'
        , 'timezone': 'INT'
        , 'id': 'BIGINT'
        , 'name': 'VARCHAR(256)'
        , 'cod': 'INT'
        , 'created_date': 'BIGINT'
    }

    , '01_forecast': {
        # Removed base, timezone, avail_update_dt, datetime, id_var, name, cod and all 'sys' entries when compared to original scraper
        # Added forecast_time_dt and forecast_time_txt to show the forecast times in readable format
        'number': 'INT'
        , 'position_long': 'REAL'
        , 'position_lat': 'REAL'
        , 'weather_id': 'INTEGER'
        , 'main': 'VARCHAR(256)'
        , 'description': 'VARCHAR(500)'
        , 'icon': 'VARCHAR(20)'
        , 'icon_url': 'VARCHAR(500)'
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

    , '02_station_avail_weather_train': {
        'number': 'INTEGER'
        , 'weather_type_id': 'INTEGER'
        , 'hour': 'INTEGER'
        , 'dayofweek': 'INTEGER'
        , 'dayofmonth': 'INTEGER'
        , 'bool_weekend': 'BOOLEAN'
        , 'bool_dayoff': 'BOOLEAN'
        , 'bool_workhour': 'BOOLEAN'
        , 'bool_commutehour': 'BOOLEAN'
        , 'bool_night': 'BOOLEAN'
        , 'available_bikes': 'REAL'  # average over everything
        , 'weather_temp_feels_like': 'REAL'  # average over everything
        , 'weather_temp': 'REAL'  # average over everything
        , 'weather_humidity': 'REAL'  # average over everything
        , 'weather_air_pressure': 'REAL'  # average over everything
        , 'created_date': 'BIGINT'
        , 'minute': 'INTEGER'
        , 'month': 'INTEGER'
        , 'year': 'INTEGER'
    }

    , '02_station_avail_weather_test': {
        'number': 'INTEGER'
        , 'weather_type_id': 'INTEGER'
        , 'hour': 'INTEGER'
        , 'dayofweek': 'INTEGER'
        , 'dayofmonth': 'INTEGER'
        , 'bool_weekend': 'BOOLEAN'
        , 'bool_dayoff': 'BOOLEAN'
        , 'bool_workhour': 'BOOLEAN'
        , 'bool_commutehour': 'BOOLEAN'
        , 'bool_night': 'BOOLEAN'
        , 'available_bikes': 'REAL'  # average over everything
        , 'weather_temp_feels_like': 'REAL'  # average over everything
        , 'weather_temp': 'REAL'  # average over everything
        , 'weather_humidity': 'REAL'  # average over everything
        , 'weather_air_pressure': 'REAL'  # average over everything
        , 'created_date': 'BIGINT'
        , 'minute': 'INTEGER'
        , 'month': 'INTEGER'
        , 'year': 'INTEGER'
    }

    , '03_user_model_entry': {
        'prediction_id': 'INTEGER NOT NULL AUTO_INCREMENT'
        , 'number': 'INTEGER'
        , 'weather_type_id': 'INTEGER'
        , 'hour': 'INTEGER'
        , 'dayofweek': 'INTEGER'
        , 'dayofmonth': 'INTEGER'
        , 'bool_weekend': 'BOOLEAN'
        , 'bool_dayoff': 'BOOLEAN'
        , 'bool_workhour': 'BOOLEAN'
        , 'bool_commutehour': 'BOOLEAN'
        , 'bool_night': 'BOOLEAN'
        , 'available_bikes': 'REAL'  # average over everything
        , 'weather_temp_feels_like': 'REAL'  # average over everything
        , 'weather_temp': 'REAL'  # average over everything
        , 'weather_humidity': 'REAL'  # average over everything
        , 'weather_air_pressure': 'REAL'  # average over everything
        , 'user_date': 'BIGINT'
        , 'created_date': 'BIGINT'
        , 'predicted_date': 'BIGINT'
        , 'model_type': 'VARCHAR(100)'
        , 'bool_correct_prediction': 'BOOLEAN'
        , 'minute': 'INTEGER'
        , 'month': 'INTEGER'
        , 'year': 'INTEGER'
    }
}
