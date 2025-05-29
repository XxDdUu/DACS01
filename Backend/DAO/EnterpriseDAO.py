import MySQLdb
from MySQLdb import Error
from werkzeug.security import generate_password_hash
from Backend.DAO.DatabaseConnection import get_connection
from PyQt6.QtWidgets import QMessageBox
from datetime import datetime
from Backend.Utils.EnterpriseUtilities import generate_random_enterprise_id
from Backend.Model.Enterprise import Enterprise
import re
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

		if not all([enterprise_name, enterprise_founder, enterprise_address, enterprise_phone_number,
			business_type, enterprise_industry, enterprise_password, confirm_enterprise_password]):
			return False, "All fields are required"

		if enterprise_password != confirm_enterprise_password:
			return False, "Password do not match"
		connection = None
		cursor = None
		try:
			hashed_password_enterprise = generate_password_hash(enterprise_password)

			print("Connecting")
			connection = get_connection()
			print("Connection successful.")
			cursor = connection.cursor()
			print("Cursor created.")
			query = """
			INSERT INTO ENTERPRISE
				(Enterprise_ID, Enterprise_NAME, Enterprise_FOUNDER, ADDRESS,
					Enterprise_PHONE_NUMBER,
					BUSINESS_TYPE, INDUSTRY, Enterprise_password)
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
					hashed_password_enterprise
				))

			connection.commit()
			print("Enterprise registered successfully")
			return True, "Enterprise registered successfully"
		except Exception as e:
			print("Can't insert data!\n")
			print(f"Error:{e}")
			return False, f"Database error: {e}"
		except MySQLdb.Error as err:
			if err.errno == errorcode.ER_DUP_ENTRY:
				return False, f"Duplicate entry phone_number detected: {err}"
			else:
				print(f"Other database error: {err}")
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
	def get_employer_enterprise_data(self, enterprise_id):
		connection = None
		cursor = None
		try:
			connection = get_connection()
			if not connection:
				return None
			cursor = connection.cursor()
			query = """SELECT * FROM ENTERPRISE WHERE Enterprise_ID = %s"""
			cursor.execute(query, (enterprise_id,))
			result = cursor.fetchone()

			enterprise_data = Enterprise(
				ID =  enterprise_id,
				name = result[1],
				founder = result[2],
				address = result[3],
				phone_number = result[4],
				type = result[5],
				industry = result[6]
				)
			return enterprise_data
		except Exception as e:
			print(f"DAO ERROR: {e}")
			return None
		finally:
			if cursor:
				cursor.close()
			if connection:
				connection.close()


