from Backend.DAO.DatabaseConnection import get_connection
import traceback

class BranchesDAO:
    def insert_branches(self, data):
        branchesId = data.get("id")
        branchesName = data.get("name")
        branchesAddress = data.get("address")
        branchesPhone = data.get("phone_number")
        employerId = data.get("employer_id")
        enterpriseId = data.get("enterprise_id")

        connection = None
        cursor = None

        try:
            connection = get_connection()
            cursor = connection.cursor()

            query = """
                INSERT INTO BRANCHES
                (Branch_ID, Branch_name, Branch_address, Branch_phone_number, Create_at, Employer_ID, Enterprise_ID)
                VALUES (%s, %s, %s, %s, NOW(), %s, %s)
            """
            cursor.execute(query, (
                branchesId,
                branchesName,
                branchesAddress,
                branchesPhone,
                "10",
                "AI25",
            ))

            connection.commit()
            return True, "Branch inserted successfully"

        except Exception as e:
            traceback.print_exc()
            return False, f"Database Error: {e}"

        finally:
            if cursor:
                cursor.close()
            if connection and connection.is_connected():
                connection.close()
