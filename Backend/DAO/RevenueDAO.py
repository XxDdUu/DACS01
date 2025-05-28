from Backend.DAO.DatabaseConnection import get_connection
import MySQLdb
import traceback
import pandas as pd

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
    def get_revenue_data(self,emp_id,ent_id):
        connection = None
        cursor = None
        try:
            connection = get_connection()
            cursor = connection.cursor()
            query1 = """
            INSERT INTO REVENUE(Branch_ID, Revenue_date, Amount)
            SELECT DISTINCT p.Branch_ID, ps.SALE_DATE, SUM(ps.SALE_AMOUNT)
            FROM PRODUCT p
            JOIN PRODUCT_SALES ps ON ps.Product_ID = p.Product_ID 
            JOIN BRANCHES b ON b.Branch_ID = p.Branch_ID
            WHERE b.Employer_ID = %s AND b.Enterprise_ID = %s
            GROUP BY p.Branch_ID, ps.SALE_DATE
            ON DUPLICATE KEY UPDATE 
            Revenue_date = VALUES(Revenue_date),
            Amount = VALUES(Amount);
            """
            cursor.execute(query1,(emp_id,ent_id))

            query2 = """
                UPDATE REVENUE r
                JOIN (
                    SELECT 
                        p.Branch_ID,
                        ps.SALE_DATE as Revenue_Date ,
                        SUM(ps.SALE_AMOUNT) AS total_revenue
                    FROM PRODUCT p
                    JOIN PRODUCT_SALES ps ON ps.Product_ID = p.Product_ID
                    JOIN BRANCHES b on b.Branch_ID = p.Branch_ID
                    WHERE b.Employer_ID = %s AND b.Enterprise_ID = %s
                    GROUP BY p.Branch_ID, ps.SALE_DATE
                    ) AS sub 
                    ON r.Branch_ID = sub.Branch_ID AND r.Revenue_date = sub.Revenue_date
                    SET r.Amount = sub.total_revenue;
            """
            cursor.execute(query2,(emp_id,ent_id))
            connection.commit()

            query3 = """
           SELECT r.* FROM REVENUE r
                        JOIN BRANCHES b ON r.Branch_ID = b.Branch_ID
                        WHERE b.Employer_ID = %s AND b.Enterprise_ID = %s ;
                    """
            cursor.execute(query3, (emp_id, ent_id))

            rows = cursor.fetchall()
            columns = [col[0] for col in cursor.description]
            df = pd.DataFrame(rows, columns=columns)
            return df.to_dict(orient="records")

        except Exception as e:
            print(f"ERROR in get_product_by_account: {e}")
            traceback.print_exc()
            return []

        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
