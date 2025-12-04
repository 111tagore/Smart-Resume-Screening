# db.py
import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
load_dotenv()

def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            port=int(os.getenv("DB_PORT", 3306)),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )
        return conn
    except Error as e:
        print("Error connecting to MySQL", e)
        raise
