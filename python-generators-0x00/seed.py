import mysql.connector
from mysql.connector import Error
import pandas as pd
import requests
from io import StringIO
import uuid

def connect_db():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='mysql',
            password='admin',
        )
        if connection.is_connected():
            print("Connected to MySQL Server")
            return connection
    except Error as e:
        print(f"Error connecting to MySQL Server: {e}")
    return None

def create_database(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
        print("Database 'ALX_prodev' is ready.")
    except mysql.connector.Error as e:
        print(f"Error creating database: {e}")

def connect_to_prodev():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='mysql',
            password='admin',
            database='ALX_prodev'
        ) 
        if connection.is_connected():
            print("Connected to ALX_prodev database")
            return connection
    except mysql.connector.Error as e:
        print(f"Error connecting to ALX_prodev database: {e}")
    return None

def create_table(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_data (
                user_id CHAR(36) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                age DECIMAL NOT NULL,
                INDEX (user_id)
            );
        """)
        print("Table 'user_data' is ready.")
    except mysql.connector.Error as e:
        print(f"Error creating table: {e}")

def load_csv_from_url(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            csv_data = StringIO(response.text)
            df = pd.read_csv(csv_data)
            print("CSV data loaded successfully.")
            return df
        else:
            print(f"Failed to load CSV data. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error loading CSV data: {e}")
    return None  

def insert_data(connection, dataframe):
    try:
        cursor = connection.cursor()
        inserted_count = 0

        for _, row in dataframe.iterrows():
            cursor.execute("SELECT 1 FROM user_data WHERE email = %s", (row['email'],))
            exists = cursor.fetchone()

            if not exists:
                user_id = str(uuid.uuid4())
                cursor.execute("""
                    INSERT INTO user_data (user_id, name, email, age)
                    VALUES (%s, %s, %s, %s);
                """, (user_id, row['name'], row['email'], row['age']))
                inserted_count += 1

        connection.commit()
        print(f"Data inserted successfully. Rows added: {inserted_count}")
    except mysql.connector.Error as e:
        print(f"Error inserting data: {e}")
        connection.rollback()

def main():
    server_conn = connect_db()
    if server_conn:
        create_database(server_conn)
        server_conn.close()

    db_conn = connect_to_prodev()
    if db_conn:
        create_table(db_conn)
        url = "https://s3.amazonaws.com/alx-intranet.hbtn.io/uploads/misc/2024/12/3888260f107e3701e3cd81af49ef997cf70b6395.csv?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIARDDGGGOUSBVO6H7D%2F20250701%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20250701T220126Z&X-Amz-Expires=86400&X-Amz-SignedHeaders=host&X-Amz-Signature=2c54fe5885b54b2c377a28fd746e31f695ac05b4295b81e5b40a200e698c740d"  # ✅ Replace with a real URL
        df = load_csv_from_url(url)

        if df is not None:
            insert_data(db_conn, df)

        db_conn.close()

if __name__ == "__main__":
    main()
