import mysql.connector
from mysql.connector import Error

def stream_users(connection):
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='mysql',
            password='admin',
            database='ALX_prodev'
        )
        cursor = connection.cursor(dictionationary=True)
        cursor.execute("SELECT * FROM user_data")

        for row in cursor:
            yield row
    except Error as e:
        print(f"Error: {e}")
    finally:
        if connection.is_connected()
            cursor.close()
            connection.close()