from mysql.connector import Error
from werkzeug.security import generate_password_hash, check_password_hash

from Backend.DAO.DatabaseConnection import get_connection
from PyQt6.QtWidgets import QMessageBox
from mysql.connector import Error
from datetime import datetime
import re
class EmployerDAO:
    def insert_employer(self, data):
        username = data.get("username")
        email = data.get("email")
        phone_number = data.get("phone_number")
        enterprise_id = data.get("enterprise_id")
        dateofbirth = data.get("date_of_birth")
        password = data.get("password")
        confirm_password = data.get("confirm_password")
        connection = None
        cursor = None
        # Validation
        if password != confirm_password:
            return False, "Passwords do not match"

        if not all([username, email, phone_number, enterprise_id, dateofbirth, password]):
            return False, "All fields are required"
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return False, "Invalid email format"

        try:
            hashed_password = generate_password_hash(password)
            connection = get_connection()
            cursor = connection.cursor()
            query = """
                INSERT INTO EMPLOYER
                (Employer_name, Employer_Phone_Number, Employer_Email, DOB, Create_at, Employer_password, Enterprise_ID)
                VALUES (%s, %s, %s, %s, NOW(), %s, %s)
            """
            cursor.execute(query, (
                username,
                phone_number,
                email,
                dateofbirth,
                hashed_password,
                enterprise_id
            ))
            connection.commit()
            return True, "Employer registered successfully"

        except Error as e:
            return False, f"Database Error: {e}"
        except ValueError:
            return False, "Invalid date format! Use yyyy-mm-dd"
        except Exception as e:
            print(f"[Unhandled Error] {e}") 
            return False, f"Unexpected error: {e}"

        finally:
            if cursor:
                cursor.close()
            if connection.is_connected():
                connection.close()
    def check_loginUser(self,data):
        username = data.get("username")
        password = data.get("password")
        connection = None
        cursor = None
        try:
            hashed_password = generate_password_hash(password)
            connection = get_connection()
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM employer WHERE Employer_name = %s", (username,))
            result = cursor.fetchone()
            connection.commit()
            if result:
                stored_hashed_pass = result[5]
                if check_password_hash(stored_hashed_pass,password):
                    # from Backend.Controller.MainController import MainController
                    # enterApp = MainController()
                    # enterApp.login_window.switch_to_dashboardApp = enterApp.show_dashboardApp()
                    return True, "Login successfully!"
                else:
                    return False,"Password does not match!"
            else:
                return False, "User account not found"
        except Error as e:
            traceback.print_exc()
            return False, f"Database Error: {e}"
        except ValueError:
            return False, "Invalid date format! Use yyyy-mm-dd"
        except Exception as e:
            print(f"[Unhandled Error] {e}")
            traceback.print_exc()
            return False, f"Unexpected error: {e}"

        finally:
            if cursor:
                cursor.close()
            if connection.is_connected():
                connection.close()