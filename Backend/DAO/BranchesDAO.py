import re

from Backend.DAO.DatabaseConnection import get_connection
import MySQLdb
import traceback
from Backend.DAO.EmployerDAO import EmployerDAO
from Backend.DAO.EnterpriseDAO import EnterpriseDao

import pandas as pd

class BranchesDAO:
    def insert_branches(self, data, enterprise_id, employer_id):
        branchesName = data.get("name")
        branchesAddress = data.get("address")
        branchesPhone = data.get("phone_number").strip()

        connection = None
        cursor = None

        # if not branchesPhone.isdigit() or len(branchesPhone) != 10:
        #     return False, "Invalid phone number format"
        def is_valid_phoneNum(phone_number):
            return bool(re.fullmatch(r"[0-9]{10}",branchesPhone))

        if not all([branchesName, branchesAddress, branchesPhone]):
            return False, "All fields are required"

        if not is_valid_phoneNum(branchesPhone):
            return False, "Invalid phone number format"

        def branch_name_exists(branch_name):
            conn_test = None
            cursor_test = None
            try:
                conn_test = get_connection()
                cursor_test = conn_test.cursor()
                query = "SELECT 1 FROM BRANCHES WHERE Branch_name = %s"
                cursor_test.execute(query, (branch_name,))
                return cursor_test.fetchone() is not None
            finally:
                if cursor:
                    cursor.close()
                if connection:
                    connection.close()

        if branch_name_exists(branchesName):
            return False, f"Branch name {branchesName} already exits"

        try:
            connection = get_connection()
            if not connection:
                return False, "Failed to connect to database"

            cursor = connection.cursor()
            query = """
                INSERT INTO BRANCHES
                (Branch_name, Branch_address, Branch_phone_number, Create_at, Employer_ID, Enterprise_ID)
                VALUES (%s, %s, %s, NOW(), %s, %s)
            """
            cursor.execute(query, (
                branchesName,
                branchesAddress,
                branchesPhone,
                employer_id,
                enterprise_id
            ))

            connection.commit()
            return True, "Branch inserted successfully"

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

    def remove_branches(self, data):
        branchesID = data.get("id")
        employerId = data.get("employer_id")
        enterpriseId = data.get("enterprise_id")

        connection = None
        cursor = None

        try:
            connection = get_connection()
            if not connection:
                return False, "Failed to connect to database"

            # Xóa bản ghi trong BRANCHES
            cursor = connection.cursor()
            query = """
                DELETE FROM BRANCHES WHERE Branch_ID = %s
            """
            cursor.execute(query, (branchesID,))

            if cursor4.rowcount == 0:
                return False, "No branch found with given Branch_ID"

            connection.commit()
            return True, "Branch deleted successfully"

        except MySQLdb.Error as e:
            print(f"SQL Error Code: {e.args[0]}, Message: {e.args[1]}")
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
    def update_branches(self,data):
        branchId = data.get("id")
        branchesName = data.get("name")
        branchesAddress = data.get("address")
        branchesPhone = data.get("phone_number").strip()
        connection = None
        cursor = None

        def found_branch_id(branchID):
            conn_test = None
            cursor_test = None
            try:
                conn_test = get_connection()
                cursor_test = conn_test.cursor()
                query = "SELECT 1 FROM BRANCHES WHERE Branch_ID = %s"
                cursor_test.execute(query, (branchID,))
                return cursor_test.fetchone() is not None
            finally:
                if cursor_test:
                    cursor_test.close()
                if conn_test:
                    conn_test.close()
        if not found_branch_id(branchId):
            return False, "Branch Id not found."



        def is_valid_phoneNum(phone_number):
            return bool(re.fullmatch(r"[0-9]{10}", branchesPhone))

        if not is_valid_phoneNum(branchesPhone):
            return False, "Invalid phone number format"

        def branch_name_exists(branch_name):
            conn_test = None
            cursor_test = None
            try:
                conn_test = get_connection()
                cursor_test = conn_test.cursor()
                query = "SELECT 1 FROM BRANCHES WHERE Branch_name = %s"
                cursor_test.execute(query, (branch_name,))
                return cursor_test.fetchone() is not None
            finally:
                if cursor_test:
                    cursor_test.close()
                if conn_test:
                    conn_test.close()

        if branch_name_exists(branchesName):
            return False, f"Branch name {branchesName} already exits"

        try:
            connection = get_connection()
            if not connection:
                return False, "Failed to connect to database"

            cursor = connection.cursor()
            query = """
                        UPDATE BRANCHES
                        SET Branch_name = %s, Branch_address = %s, Branch_phone_number = %s
                        WHERE Branch_ID = %s
                    """
            cursor.execute(query, (
                branchesName,
                branchesAddress,
                branchesPhone,
                branchId,
            ))

            connection.commit()
            return True, "Branch updated successfully"

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
    def get_branches_by_enterprise_employer(self, enterprise_id, employer_id):
        connection = None
        cursor = None
        try:
            connection = get_connection()
            cursor = connection.cursor()

            query = """
                        SELECT * FROM BRANCHES
                        WHERE Enterprise_ID = %s AND Employer_ID = %s
                    """

            cursor.execute(query, (enterprise_id, employer_id))
            rows = cursor.fetchall()
            columns = [col[0] for col in cursor.description]
            df = pd.DataFrame(rows, columns=columns)

            return df.to_dict(orient="records")
        except Exception as e:
            print(f"ERROR in get_product_sales_data: {e}")
            traceback.print_exc()
            return []

        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
