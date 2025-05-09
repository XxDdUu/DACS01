import mysql.connector
from mysql.connector import Error
from Backend.DAO.Constant import DB_CONFIG, PYAPP_DB_CONFIG

def get_connection():
	try:
		connection = mysql.connector.connect(**PYAPP_DB_CONFIG)
		if connection.is_connected():
			return connection
		else:
			raise Error("connection failed")
	except Error as e:
		print(f"[Connection error] {e}")
		raise