from itertools import product

from Backend.DAO.DatabaseConnection import get_connection
import MySQLdb
import traceback
import pandas as pd

class ProductDAO:
    def insert_product(self, data):
        productName = data.get("name")
        price_raw = data.get("price", "").strip()
        productAmount = data.get("amount")
        branchID = data.get("branch_id")

        connection = None
        cursor = None

        # Kiểm tra và ép kiểu giá
        try:
            if not all([productName, price_raw, productAmount, branchID]):
                return False, "All fields are required"
            productPrice = float(price_raw)
            if productPrice <= 0:
                return False, "Invalid price: must be greater than 0"
        except ValueError:
            return False, f"Invalid price format: '{price_raw}'"

        try:
            connection = get_connection()
            if not connection:
                return False, "Failed to connect to database"

            cursor = connection.cursor()
            query = """
                INSERT INTO PRODUCT
                (Product_NAME, PRICE, AMOUNT, Branch_ID)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, (
                productName,
                productPrice,         # đã ép kiểu float
                productAmount,
                branchID
            ))

            connection.commit()
            return True, "Product inserted successfully"

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
    def remove_product(self, data):
        productId = data.get("id")
        productName = data.get("name")
        price_raw = data.get("price", "").strip()
        productAmount = data.get("amount")
        branchID = data.get("branch_id")

        connection = None
        cursor = None

        try:
            connection = get_connection()
            if not connection:
                return False, "Failed to connect to database"
            cursor1 = connection.cursor()
            query = """
                DELETE FROM PRODUCT_SALES WHERE Product_ID = %s AND Branch_ID = %s
                    """
            cursor1.execute(query, (
                productId,
                branchID
            ))
            cursor2 = connection.cursor()
            query = """
                DELETE FROM PRODUCT WHERE Product_ID = %s AND Branch_ID = %s
            """
            cursor2.execute(query, (
                productId,
                branchID
            ))
            connection.commit()
            return True, "Product deleted successfully"

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
    def update_product(self, data):
        productId = data.get("id")
        productName = data.get("name")
        price_raw = data.get("price", "").strip()
        productAmount = data.get("amount")
        branchID = data.get("branch_id")

        connection = None
        cursor = None

        # Kiểm tra và ép kiểu giá
        try:
            productPrice = float(price_raw)
            if productPrice <= 0:
                return False, "Invalid price: must be greater than 0"
        except ValueError:
            return False, f"Invalid price format: '{price_raw}'"

        try:
            connection = get_connection()
            if not connection:
                return False, "Failed to connect to database"

            cursor = connection.cursor()
            query = """
                UPDATE PRODUCT 
                SET Product_ID = %s, Product_NAME = %s, PRICE = %s, AMOUNT = %s
                WHERE Product_ID = %s AND Branch_ID = %s
            """
            cursor.execute(query, (
                productId,
                productName,
                productPrice,
                productAmount,
                productId,
                branchID
            ))

            connection.commit()
            return True, "Product updated successfully"

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
    def get_product_by_account(self,emp_ID , ent_ID):
        connection = None
        cursor = None
        try:
            connection = get_connection()
            cursor = connection.cursor()

            query = """
                SELECT p.* FROM PRODUCT p
                JOIN BRANCHES b ON p.Branch_ID = b.Branch_ID
                WHERE b.Employer_ID = %s AND b.Enterprise_ID = %s 
            """

            cursor.execute(query, (emp_ID, ent_ID))
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

