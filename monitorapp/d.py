import pyodbc 

# def conn():
#     # driver = 'ODBC Driver 17 for SQL Server'
#     # print(driver)
#     # server = '103.230.39.245'
#     # print(server)
#     # username = 'stagingadmin'
#     # print(username)
#     # password = 'StagingAdmin@123#'
#     # print(password)
#     # db = 'RawDBCommsTool'
#     # print(db)

    
#     connection = pyodbc.connect("DRIVER={ODBC Driver 17 for SQL Server};SERVER=103.230.39.245;DATABASE=RAWDBFMSV12;UID=stagingadmin;PWD=StagingAdmin@123#", autocommit=True)
#     # conn1 = pyodbc.connect(driver=driver, server=server, database=db,
#     #                         uid=username, pwd=password)
#     # print("0")
#     my_cursor = connection.cursor()  
#     print("SQL Server connection successful")
    
        
#     return my_cursor

# d = conn()

def connection():
    driver = "ODBC Driver 17 for SQL Server"
    server = "103.230.38.205"
    username = "stagingadmin"
    password = "StagingAdmin@123#"
    db = "RawDBCommsTool"
    
    conn = pyodbc.connect(driver=driver, server=server, database=db,
                            uid = username, pwd=password,)
    my_cursor = conn.cursor()  
    print("SQL Server connection successful")
   
        
    return my_cursor

d = connection()