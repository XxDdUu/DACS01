from Backend.DAO.DatabaseConnection import get_connection
import MySQLdb
import traceback

class RevenueDAO:
    def create_revenue(self, data):
        revenueId = data.get("id")
        revenueDate =  data.get("date")
        revenue_raw = data.get("amount").strip()
        branchID = data.get("branch_id")

        connection = None
        cursor = None

        if not all([revenueId,revenueDate,revenue_raw,branchID]):
            return False, "All fields are required to add"
        #Kiểm tra và ép kiểu giá
        try:
            revenueAmount = float(revenue_raw)
            if revenueAmount <= 0:
                return False, "Invalid price: must be greater than 0"
        except ValueError:
            return False, f"Invalid price format: '{revenue_raw}'"
        try:
            connection = get_connection()
            if not connection:
                return False, "Failed to connect to database"

            cursor = connection.cursor()
            query = """
                INSERT INTO REVENUE
                (Revenue_ID, Revenue_date, Amount, Branch_ID)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, (
                revenueId,
                revenueDate,         # đã ép kiểu float
                revenueAmount,
                branchID
            ))

            connection.commit()
            return True, "Revenue inserted successfully"

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
    def remove_revenue(self, data):
        revenueId = data.get("id")
        revenueDate = data.get("date")
        revenue_raw = data.get("amount").strip()
        branchID = data.get("branch_id")

        connection = None
        cursor = None

        # Kiểm tra và ép kiểu giá
        try:
            revenueAmount = float(revenue_raw)
            if revenueAmount <= 0:
                return False, "Invalid price: must be greater than 0"
        except ValueError:
            return False, f"Invalid price format: '{revenue_raw}'"

        try:
            connection = get_connection()
            if not connection:
                return False, "Failed to connect to database"

            cursor2 = connection.cursor()
            query = """
                DELETE FROM REVENUE WHERE Revenue_ID = %s AND Revenue_date = %s AND Branch_ID = %s
            """
            cursor2.execute(query, (
                revenueId,
                revenueDate,
                branchID,
            ))

            connection.commit()
            return True, "Revenue deleted successfully"

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
    def update_revenue(self, data):
        revenueId = data.get("id")
        revenueDate = data.get("date")
        revenue_raw = data.get("amount").strip()
        branchID = data.get("branch_id")

        connection = None
        cursor = None

        # Kiểm tra và ép kiểu giá
        try:
            revenueAmount = float(revenue_raw)
            if revenueAmount <= 0:
                return False, "Invalid price: must be greater than 0"
        except ValueError:
            return False, f"Invalid price format: '{revenue_raw}'"

        try:
            connection = get_connection()
            if not connection:
                return False, "Failed to connect to database"

            cursor = connection.cursor()
            query = """
                UPDATE PRODUCT 
                SET Revenue_date = %s, AMOUNT = %s 
                WHERE Branch_ID = %s AND Revenue_ID = %s,
            """
            cursor.execute(query, (
                revenueDate,
                revenueAmount,
                branchID,
                revenueId
            ))

            connection.commit()
            return True, "Revenue updated successfully"

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
