import MySQLdb
from MySQLdb import Error
from Backend.DAO.Constant import DB_CONFIG, PYAPP_DB_CONFIG

def get_connection():
	try:
		connection = MySQLdb.connect(**DB_CONFIG)
		if connection:
			connection.set_character_set('utf8mb4')
			connection.autocommit = True
			return connection
		else:
			raise Error("Connection failed.")

	except MySQLdb.Error as e:
		import traceback
		traceback.print_exc()
		return None
