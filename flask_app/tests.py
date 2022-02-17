from flask_app.methods import *

def connection_test(host,user,password,port,db):
    """Test if a connection to the database was established"""
    connection_result=connect_db_engine(host,user,password,port,db)
    
    test_result=True
    #Error Value returned in the method
    if connection_result[0]==1:
        test_result=False

    return test_result
