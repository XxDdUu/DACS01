from Backend.DAO.DatabaseConnection import get_connection
import MySQLdb
import traceback

class BranchesDAO:
    def insert_branches(self, data):
        branchesName = data.get("name")
        branchesAddress = data.get("address")
        branchesPhone = data.get("phone_number")
        employerId = data.get("employer_id") or "10"         # fallback nếu None
        enterpriseId = data.get("enterprise_id") or "AI25"   # fallback nếu None

        connection = None
        cursor = None

        if not branchesPhone.isdigit() or len(branchesPhone) != 10:
            return False, "Invalid phone number format"

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
