import MySQLdb
<<<<<<< HEAD
from MySQLdb import Error
from werkzeug.security import generate_password_hash
from Backend.DAO.DatabaseConnection import get_connection
from PyQt6.QtWidgets import QMessageBox
from datetime import datetime
from Backend.Utils.EnterpriseUtilities import generate_random_enterprise_id
import re
=======
from werkzeug.security import generate_password_hash
from Backend.DAO.DatabaseConnection import get_connection
>>>>>>> a7b2c40d40f6ffa74fcff18365461ae51d32647d
import traceback

class EnterpriseDao:
	def insert_enterprise(self, data):
		enterprise_id = generate_random_enterprise_id()
		enterprise_name = data.get("enterprise_name")
		enterprise_founder = data.get("enterprise_founder")
		enterprise_address = data.get("enterprise_address")
		enterprise_phone_number = data.get("enterprise_phone_number")
		business_type = data.get("business_type")
		enterprise_industry = data.get("enterprise_industry")
		enterprise_password = data.get("enterprise_password")
		confirm_enterprise_password = data.get("confirm_enterprise_password")

		if enterprise_password != confirm_enterprise_password:
			return False, "password do not match"
		connection = None
		cursor = None
		try:
			print("Connecting")
			connection = get_connection()
			print("Connection successful.")
			cursor = connection.cursor()
			print("Cursor created.")
			query = """
			INSERT INTO ENTERPRISE
				(Enterprise_ID, Enterprise_NAME, Enterprise_FOUNDER, ADDRESS,
					Enterprise_PHONE_NUMBER,
					BUSINESS_TYPE, INDUSTRY, 
					Enterprise_password)
					VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
				"""
			print("Hello")
			cursor.execute(query, (
					enterprise_id,
					enterprise_name,
					enterprise_founder,
					enterprise_address,
					enterprise_phone_number,
					business_type,
					enterprise_industry,
					enterprise_password
				))

			connection.commit()
			print("Enterprise registered successfully")
			return True, "Enterprise registered successfully"
		except Exception as e:
			print("Can't insert data!\n")
			print(f"Error:{e}")
			return False, f"Database error: {e}"
		finally:
			if cursor is not None:
				try:
					cursor.close()
				except MySQLdb.Error:
					pass
			if connection is not None:
				try:
					connection.close()
				except MySQLdb.Error:
					pass
    def insert_enterprise(self, data):
        enterprise_id = "xo7"  # Nếu bạn muốn tự tạo mã ID
        enterprise_name = data.get("enterprise_name")
        enterprise_founder = data.get("enterprise_founder")
        enterprise_address = data.get("enterprise_address")
        enterprise_phone_number = data.get("enterprise_phone_number")
        business_type = data.get("business_type")
        enterprise_industry = data.get("enterprise_industry")
        enterprise_password = data.get("enterprise_password")
        confirm_enterprise_password = data.get("confirm_enterprise_password")

        if enterprise_password != confirm_enterprise_password:
            return False, "Passwords do not match"

        # Mã hóa mật khẩu trước khi lưu
        hashed_password = generate_password_hash(enterprise_password)

        connection = None
        cursor = None

        try:
            print("Connecting...")
            connection = get_connection()
            if not connection:
                return False, "Failed to connect to database"
            print("Connection successful.")

            cursor = connection.cursor()
            print("Cursor created.")

            query = """
                INSERT INTO ENTERPRISE
                (Enterprise_ID, Enterprise_NAME, Enterprise_FOUNDER, ADDRESS,
                 Enterprise_PHONE_NUMBER, BUSINESS_TYPE, INDUSTRY, Enterprise_password)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                enterprise_id,
                enterprise_name,
                enterprise_founder,
                enterprise_address,
                enterprise_phone_number,
                business_type,
                enterprise_industry,
                hashed_password
            ))

            connection.commit()
            print("Enterprise registered successfully")
            return True, "Enterprise registered successfully"

        except MySQLdb.Error as e:
            traceback.print_exc()
            return False, f"MySQL Error: {e}"

        except Exception as e:
            traceback.print_exc()
            return False, f"Unexpected Error: {e}"

        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
