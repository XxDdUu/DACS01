import MySQLdb
from werkzeug.security import generate_password_hash, check_password_hash
from Backend.DAO.DatabaseConnection import get_connection
from PyQt6.QtWidgets import QMessageBox
from MySQLdb import Error
from datetime import datetime
import re
import traceback

from Backend.Model.Employer import Employer


class EmployerDAO:
    def insert_employer(self, data):
        username = data.get("username")
        email = data.get("email")
        phone_number = data.get("phone_number")
        enterprise_id = data.get("enterprise_id")
        enterprise_password_employer = data.get("enterprise_password_employer")
        dateofbirth = data.get("date_of_birth")
        password = data.get("password")
        confirm_password = data.get("confirm_password")
        # Validation

        if password != confirm_password:
            return False, "Passwords do not match"

        if not all([username, email, phone_number, enterprise_id, enterprise_password_employer, dateofbirth, password]):
            return False, "All fields are required"
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return False, "Invalid email format"

        connection = None
        cursor = None
        try:
            connection = get_connection()
            if not connection:
                return False, "Failed to connect to DB"
            cursor = connection.cursor()
            query = """
                SELECT Enterprise_password from ENTERPRISE where Enterprise_ID = %s
            """
            cursor.execute(query, (enterprise_id,))
            result = cursor.fetchone()
            if result:
                stored_hashed_pass = result[0]
                if not check_password_hash(stored_hashed_pass, enterprise_password_employer):
                    return False, ("Wrong password for enterprise: " + enterprise_id)
            else:
                return False, "Enterprise id not found"

        except MySQLdb.Error as e:
            traceback.print_exc()
            return False, f"Database Error: {e}"
        except Exception as e:
            traceback.print_exc()
            return False, f"Unexpected error: {e}"
        try:
            hashed_password = generate_password_hash(password)
            connection = get_connection()
            if not connection:
                return False, "Failed to connect to DB"

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

        except MySQLdb.Error as e:
            traceback.print_exc()
            return False, f"Database Error: {e}"
        except ValueError:
            return False, "Invalid date format! Use yyyy-mm-dd"
        except Exception as e:
            print(f"[Unhandled Error] {e}")
            traceback.print_exc()
            return False, f"Unexpected error: {e}"
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

    def check_loginUser(self, data):
        identifier = data.get("identifier")
        password = data.get("password")
        connection = None
        cursor = None
        print(identifier + " " + password)
        if not all([identifier, password]):
            return False, "All fields are required", None
        try:
            connection = get_connection()
            if not connection:
                return False, "Failed to connect to DB", None

            cursor = connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("""SELECT * FROM EMPLOYER WHERE 
                Employer_Email = %s OR Employer_Phone_Number = %s LIMIT 1""",
                           (identifier, identifier))
            result = cursor.fetchone()
            print("Query result:", result)
            if result:
                stored_hashed_pass = result["Employer_password"]
                if check_password_hash(stored_hashed_pass, password):
                    employer_data = Employer(
                        ID=result["Employer_ID"],
                        username=result["Employer_name"],
                        create_at_time = result["Create_at"],
                        phone_number=result["Employer_Phone_Number"],
                        email=result["Employer_Email"],
                        date_of_birth=result["DOB"],
                        enterprise_id=result["Enterprise_ID"]
                    )
                    print("Login successfully!")
                    return True, "Login successfully!", employer_data
                else:
                    return False, "Password does not match!", None
            else:
                return False, "Wrong email or phone_number!", None

        except MySQLdb.Error as e:
            traceback.print_exc()
            return False, f"Database Error: {e}", None
        except Exception as e:
            traceback.print_exc()
            return False, f"Unexpected error: {e}", None
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    def edit_username(self, data):
        username = data.get("username")
        employer_id = data.get("employer_id")
        enterprise_id = data.get("enterprise_id")

        connection = None
        cursor = None

        try:
            connection = get_connection()
            if not connection:
                return False, "Failed to connect to database"
            cursor = connection.cursor()
            query = """
                UPDATE EMPLOYER 
                SET Employer_name = %s 
                WHERE Enterprise_ID = %s AND Employer_ID = %s
                            """
            cursor.execute(query, (
                username,
                enterprise_id,
                employer_id
            ))
            connection.commit()
            return True, "Edit successfully"

        except MySQLdb.Error as e:
            traceback.print_exc()
            return False, f"Database Error: {e}"

        except Exception as e:
            traceback.print_exc()
            return False, f"Unexpected Error: {e}"

        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    def edit_dateBirth_Email_phoneNum(self, data):
        datebirth = data.get("date_of_birth")
        email = data.get("email")
        phoneNumber = data.get("phone_number")
        enterprise_id = data.get("enterprise_id")
        employer_id = data.get("employer_id")

        connection = None
        cursor = None

        try:
            connection = get_connection()
            if not connection:
                return False, "Failed to connect to database"
            cursor = connection.cursor()
            query = """
                        UPDATE EMPLOYER 
                        SET DOB = %s, Employer_Email = %s, Employer_Phone_Number = %s
                        WHERE Enterprise_ID = %s AND Employer_ID = %s
                                    """
            cursor.execute(query, (
                datebirth,
                email,
                phoneNumber,
                enterprise_id,
                employer_id
            ))
            connection.commit()
            return True, "Edit successfully"

        except MySQLdb.Error as e:
            traceback.print_exc()
            return False, f"Database Error: {e}"

        except Exception as e:
            traceback.print_exc()
            return False, f"Unexpected Error: {e}"

        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
