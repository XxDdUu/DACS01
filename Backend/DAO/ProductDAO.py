from Backend.DAO.DatabaseConnection import get_connection
import MySQLdb
import traceback

class ProductDAO:
    def insert_product(self, data):
        productName = data.get("name")
        price_raw = data.get("price") #ép kiểu cho price
        productPrice = float(price_raw) if price_raw not in (None, '', 'null') else 0.0
        productAmount = data.get("amount")
        branchID = data.get("branchID")         # fallback nếu None

        connection = None
        cursor = None

        if not price_raw or not price_raw.replace('.', '', 1).isdigit():
            return False, "Invalid price"

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
                productPrice,
                productAmount,
                branchID
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
