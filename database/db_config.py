import mysql.connector
from mysql.connector import Error

class connection:
    
    def __init__(self):
        try:
            self.connection = mysql.connector.connect(host='localhost',
                                                database='S-Cb_db',
                                                user='root',
                                                password='root')
            if self.connection.is_connected():
                db_Info = self.connection.get_server_info()
                print("Connected to MySQL Server version ", db_Info)
                cursor = self.connection.cursor()
                cursor.execute("select database();")
                record = cursor.fetchone()
                print("You're connected to database: ", record)

        except Error as e:
            print("Error while connecting to MySQL", e)
            
    def get_connection(self):
        #print(self.connection)
        return self.connection;
 