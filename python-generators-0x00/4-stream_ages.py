# 4-stream_ages.py
import seed

def stream_user_ages():
    conn = seed.connect_to_prodev()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT age FROM user_data")
    for row in cursor:
        yield row["age"]
    cursor.close()
    conn.close()

def compute_average_age():
    total = 0
    count = 0
    for age in stream_user_ages():
        total += age
        count += 1
    print(f"Average age of users: {total / count if count else 0}")

if __name__ == "__main__":
    compute_average_age()
