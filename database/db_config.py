import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv()

class connection:
    def __init__(self):
        try:
            # Use Railway's env variables if they exist, otherwise fallback to local
            self.connection = mysql.connector.connect(
                host=os.getenv("MYSQLHOST", "localhost"),
                user=os.getenv("MYSQLUSER", "root"),
                password=os.getenv("MYSQLPASSWORD", "root"),
                database=os.getenv("MYSQLDATABASE", "S-Cb_db"),
                port=int(os.getenv("MYSQLPORT", 3306))
            )
            if self.connection.is_connected():
                print("Successfully connected to the database!")

        except Error as e:
            print(f"Error while connecting to MySQL: {e}")
            self.connection = None
            
    def get_connection(self):
        return self.connection
