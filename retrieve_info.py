import sqlite3

conn = sqlite3.connect("math_microservice.db")
cursor = conn.cursor()
cursor.execute("SELECT * FROM request_logs")
rows = cursor.fetchall()

for row in rows:
    print(row)

# cursor.execute(
#     "INSERT INTO request_logs (operation, parameters, result, timestamp) VALUES (?, ?, ?, datetime('now'))",
#     ("test_op", '{"n": 5}', "120", )
# )
# conn.commit()
# cursor.execute("SELECT * FROM request_logs")
# print(cursor.fetchall())

#conn.close()
