# from mysql.connector import Error
# from werkzeug.security import generate_password_hash
# from Backend.DAO.DatabaseConnection import get_connection
# from PyQt6.QtWidgets import QMessageBox
# from mysql.connector import Error
# from datetime import datetime
# import re
# import traceback
#
#
# class EnterpriseDao:
#     try:
#         connection = get_connection()
#         cursor = connection.cursor()
#
#         query = """
#             INSERT INTO ENTERPRISE
#             (Enterprise_ID, Enterprise_NAME, Enterprise_FOUNDER, ADDRESS, Enterprise_PHONE_NUMBER, BUSINESS_TYPE, INDUSTRY)
#             VALUES (%s, %s, %s, %s, %s, %s, %s)
#         """
#         values = (
#             "ENT001",  # Enterprise_ID
#             "Tech Solutions Vietnam",  # Enterprise_NAME
#             "Nguyễn Văn Anh",  # Enterprise_FOUNDER
#             "123 Lê Lợi, Quận 1, TP.HCM",  # ADDRESS
#             "0903123456",  # Enterprise_PHONE_NUMBER
#             "Công nghệ thông tin",  # BUSINESS_TYPE
#             "Phần mềm"  #INDUSTRY
#         )
#
#         cursor.execute(query, values)
#         connection.commit()
#         print("Enterprise registered successfully")
#
#     except Exception as e:
#         print("Can't insert data!\n")
#         print(f"Error:{e}")
#     finally:
#         if cursor:
#             cursor.close()
#         if connection.is_connected():
#             connection.close()
