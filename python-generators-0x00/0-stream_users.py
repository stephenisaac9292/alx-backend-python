import sqlite3

def stream_users():
    # Connect to the SQLite database
    conn = sqlite3.connect('user_data.db')
    conn.row_factory = sqlite3.Row  # This allows access by column name
    cursor = conn.cursor()

    # Execute a SELECT query
    cursor.execute("SELECT * FROM user_data")

    # Use a generator to yield one row at a time
    for row in cursor:
        # Convert the row to a dictionary
        yield dict(row)

    # Cleanup
    cursor.close()
    conn.close()
