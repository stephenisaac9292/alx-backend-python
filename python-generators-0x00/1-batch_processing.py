import mysql.connector
from mysql.connector import Error

def stream_users_in_batches(batch_size):
    connection = mysql.connector.connect(
        host='localhost',
        user='mysql',
        password='admin',
        database='ALX_prodev'
    )
    cursor = connection.cursor(dictionary=True)
    offset = 0
    while True:
        cursor.execute("SELECT * FROM user_data LIMIT %s OFFSET %s", (batch_size, offset))
        rows = cursor.fetchall()
        if not rows:
            break
        for row in rows:
            yield row
        offset += batch_size
    cursor.close()
    connection.close()

def batch_processing(batch_size):
    for batch in stream_users_in_batches(batch_size):
        filtered = [user for user in batch if user['age'] > 25]
        for user in filtered:
            print(f"User: {user['name']}, Age: {user['name']}")


def main():
    # Step 1: Choose a batch size
    batch_size = 10

    # Step 2: Stream and process users in batches
    batch_processing(batch_size) # this triggers everything

if __name__ == "__main__":
    main()