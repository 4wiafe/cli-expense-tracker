from database.connection import get_connection

connection = get_connection()

print("Databse connected successfully")
print(connection)

connection.close()
