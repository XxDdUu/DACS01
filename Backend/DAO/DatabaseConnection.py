import mysql.connector
from mysql.connector import Error
from Backend.DAO.Constant import DB_CONFIG, PYAPP_DB_CONFIG

def get_connection():
	try:
		print("Trying to connect...")
		connection = mysql.connector.connect(
			host='127.0.0.1',
			user='root',
			password='12345678',
			database='QLDTCNCH',
			port=3306,
			connect_timeout=5
		)
		
		if connection.is_connected():
			# Set charset and autocommit AFTER connection
			connection.set_charset_collation('utf8mb4')
			connection.autocommit = True
			print("✅ Database connected.")
			return connection
		else:
			raise Error("Connection failed.")

	except Error as e:
		print(f"❌ [Connection error] {e}")
		import traceback
		traceback.print_exc()  # 🛠 Show full stack trace
		return None