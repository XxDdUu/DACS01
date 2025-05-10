import MySQLdb
from Backend.DAO.Constant import DB_CONFIG, PYAPP_DB_CONFIG

def get_connection():
    connection = None
    try:
        print("Trying to connect...")
        connection = MySQLdb.connect(
            host='127.0.0.1',
            user='root',
            passwd='mypassword',  # MySQLdb dùng 'passwd' thay vì 'password'
            db='qldtcnch',
            port=3306,
            charset='utf8mb4'  # Thiết lập charset khi kết nối
        )

        # Tự động commit (MySQLdb không có `autocommit` như mysql-connector)
        connection.autocommit(True)

        print("Database connected!")
        return connection

    except MySQLdb.Error as e:
        print(f"[Connection error] {e}")
        import traceback
        traceback.print_exc()
        return None
