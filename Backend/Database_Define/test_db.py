# test_db.py
import mysql.connector
from mysql.connector import Error

print("Trying to connect...")

try:
    connection = mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        password='12345678',
        database='QLDTCNCH',
        port=3306,
        connect_timeout=5
    )
    connection.set_charset_collation('utf8mb4')
    connection.autocommit = True
    print("✅ Connected successfully!")

except Error as e:
    print("❌ Connection error:", str(e))

finally:
    if 'connection' in locals() and connection.is_connected():
        connection.close()
        print("🔌 Connection closed.")