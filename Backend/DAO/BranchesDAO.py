import re

from Backend.DAO.DatabaseConnection import get_connection
import MySQLdb
import traceback
from Backend.DAO.EmployerDAO import EmployerDAO
from Backend.DAO.EnterpriseDAO import EnterpriseDao

class BranchesDAO:
    def insert_branches(self, data):
        branchesName = data.get("name")
        branchesAddress = data.get("address")
        branchesPhone = data.get("phone_number").strip()
        employerId = data.get("employer_id") or "2"         # fallback nếu None
        enterpriseId = data.get("enterprise_id") or "ENT_VTX22NH"   # fallback nếu None

        connection = None
        cursor = None

        # if not branchesPhone.isdigit() or len(branchesPhone) != 10:
        #     return False, "Invalid phone number format"
        def is_valid_phoneNum(phone_number):
            return bool(re.fullmatch(r"[0-9]{10}",branchesPhone))

        if not all([branchesName, branchesAddress, branchesPhone, employerId, enterpriseId]):
            return False, "All fields are required"

        if not is_valid_phoneNum(branchesPhone):
            print(f"Phone input raw: '{data.get('phone_number')}'")
            print(f"Phone after strip: '{branchesPhone}'")
            print(f"Phone length: {len(branchesPhone)}")
            print(f"Digits only: {branchesPhone.isdigit()}")
            print([ord(c) for c in branchesPhone])  # In mã unicode từng ký tự
            return False, "Invalid phone number format"

        def branch_name_exists(branch_name):
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
                employerId,
                enterpriseId
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
        # branchesName = data.get("name")
        # branchesAddress = data.get("address")
        # branchesPhone = data.get("phone_number").strip()
        employerId = data.get("employer_id") or "2"         # fallback nếu None
        enterpriseId = data.get("enterprise_id") or "ENT_VTX22NH"   # fallback nếu None

        connection = None
        cursor = None

        # if not branchesPhone.isdigit() or len(branchesPhone) != 10:
        #     return False, "Invalid phone number format"
        # def is_valid_phoneNum(phone_number):
        #     return bool(re.fullmatch(r"[0-9]{10}",branchesPhone))
        #
        # if not is_valid_phoneNum(branchesPhone):
        #     print(f"Phone input raw: '{data.get('phone_number')}'")
        #     print(f"Phone after strip: '{branchesPhone}'")
        #     print(f"Phone length: {len(branchesPhone)}")
        #     print(f"Digits only: {branchesPhone.isdigit()}")
        #     print([ord(c) for c in branchesPhone])  # In mã unicode từng ký tự
        #     return False, "Invalid phone number format"
        #
        # def branch_name_exists(branch_name):
        #     try:
        #         conn_test = get_connection()
        #         cursor_test = conn_test.cursor()
        #         query = "SELECT 1 FROM BRANCHES WHERE Branch_name = %s"
        #         cursor_test.execute(query, (branch_name,))
        #         return cursor_test.fetchone() is not None
        #     finally:
        #         if cursor:
        #             cursor.close()
        #         if connection:
        #             connection.close()
        #
        # if branch_name_exists(branchesName):
        #     return False, f"Branch name {branchesName} already exits"
        #
        try:
            connection = get_connection()
            if not connection:
                return False, "Failed to connect to database"

            cursor = connection.cursor()
            query = """
                DELETE FROM BRANCHES WHERE Branch_ID = %s
            """
            cursor.execute(query, (
                branchesID
            ))

            connection.commit()
            return True, "Branch deleted successfully"

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
    def update_branches(self,data):
        branchId = data.get("id")
        branchesName = data.get("name")
        branchesAddress = data.get("address")
        branchesPhone = data.get("phone_number").strip()
        employerId = data.get("employer_id") or "2"  # fallback nếu None
        enterpriseId = data.get("enterprise_id") or "ENT_VTX22NH"  # fallback nếu None

        connection = None
        cursor = None

        def is_valid_phoneNum(phone_number):
            return bool(re.fullmatch(r"[0-9]{10}", branchesPhone))

        if not is_valid_phoneNum(branchesPhone):
            print(f"Phone input raw: '{data.get('phone_number')}'")
            print(f"Phone after strip: '{branchesPhone}'")
            print(f"Phone length: {len(branchesPhone)}")
            print(f"Digits only: {branchesPhone.isdigit()}")
            print([ord(c) for c in branchesPhone])  # In mã unicode từng ký tự
            return False, "Invalid phone number format"

        def branch_name_exists(branch_name):
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
                       UPDATE BRANCHES
                       SET Branch_name = %s, Branch_address = %s, Branch_phone_number = %s
                       WHERE Employer_ID = %s AND Enterprise_ID = %s AND Branch_ID = %s
                   """
            cursor.execute(query, (
                branchesName,
                branchesAddress,
                branchesPhone,
                employerId,
                enterpriseId,
                branchId
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


