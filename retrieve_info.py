import sqlite3

conn = sqlite3.connect("math_microservice.db")
cursor = conn.cursor()
cursor.execute("SELECT * FROM request_logs")
rows = cursor.fetchall()

for row in rows:
    print(row)

# Close the database connection
conn.close()
