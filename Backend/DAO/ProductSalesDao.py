from Backend.DAO.DatabaseConnection import get_connection
import MySQLdb
import traceback
import numpy as np

class ProductSalesDAO:
    def add_ProductSales(self, data):
        sale_id = data.get("id")
        product_id =  data.get("product_id")
        branch_id = data.get("branch_id")
        sale_date =  data.get("date")
        quantity_sold =  data.get("quantity_sold")

        connection = None
        cursor = None

        try:
            connection = get_connection()
            if not connection:
                return False, "Failed to connect to database"

            cursor = connection.cursor()

            # Generate product_sales
            query = """SELECT PRICE, Product_NAME FROM PRODUCT WHERE Product_ID = %s"""
            cursor.execute(query, (product_id,))
            result = cursor.fetchone()

            if not result:
                return False, f"Product id {product_id} not found."

            price = float(result[0])
            productName = result[1]

            quantity_sold = int(quantity_sold)
            sale_amount = np.multiply(price, quantity_sold)  # Simple multiplication instead of np.multiply

            # Check if product is out of stock
            cursor.execute("SELECT Amount FROM PRODUCT WHERE Product_ID = %s", (product_id,))
            stock = cursor.fetchone()[0]

            if stock < quantity_sold:
                return False, f"Not enough stock. Available: {stock}, Requested: {quantity_sold}"

            # Decrease the product's stock amount
            cursor.execute("""

                        UPDATE PRODUCT
                        SET Amount = Amount - %s
                        WHERE Product_ID = %s
                    """, (quantity_sold, product_id))

            # Insert the sale record into PRODUCT_SALES
            query = """
                        INSERT INTO PRODUCT_SALES
                        (Product_ID, Branch_ID, SALE_DATE, QUANTITY_SOLD, SALE_AMOUNT)
                        VALUES (%s, %s, %s, %s, %s)
                    """
            cursor.execute(query, (
                product_id,
                branch_id,
                sale_date,
                quantity_sold,
                sale_amount
            ))

            # Commit the transaction
            connection.commit()
            return True, f"Added product {productName} sale information successfully"

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

    def remove_ProductSales(self, data):
        sale_Id = data.get("id")
        product_id = data.get("product_id")
        branch_id = data.get("branch_id")
        sale_date = data.get("date")
        quantity_sold = data.get("quantity_sold")
        # sale_amount_raw = data.get("amount").strip()

        connection = None
        cursor = None

        # # Kiểm tra và ép kiểu giá
        # try:
        #     sale_amount = float(sale_amount_raw)
        #     if sale_amount <= 0:
        #         return False, "Invalid price: must be greater than 0"
        # except ValueError:
        #     return False, f"Invalid price format: '{sale_amount_raw}'"
        try:
            connection = get_connection()
            if not connection:
                return False, "Failed to connect to database"

            cursor = connection.cursor()
            query = """
                DELETE FROM product_sales 
                WHERE Product_ID = %s AND Branch_ID = %s
            """
            cursor.execute(query, (
                # sale_Id,
                product_id,
                branch_id,
            ))

            connection.commit()
            return True, "Product_Sales removed successfully"

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
    def update_ProductSales(self, data):
        sale_Id = data.get("id")
        product_id = data.get("product_id")
        branch_id = data.get("branch_id")
        sale_date = data.get("date")
        quantity_sold = data.get("quantity_sold")
        sale_amount_raw = data.get("amount_total")

        connection = None
        cursor = None

        # Kiểm tra và ép kiểu giá
        try:
            sale_amount = float(sale_amount_raw)
            if sale_amount <= 0:
                return False, "Invalid price: must be greater than 0"
        except ValueError:
            return False, f"Invalid price format: '{sale_amount_raw}'"

        try:
            connection = get_connection()
            if not connection:
                return False, "Failed to connect to database"

            cursor = connection.cursor()
            query = """SELECT PRICE, Product_NAME FROM PRODUCT WHERE Product_ID = %s"""
            cursor.execute(query, (product_id,))
            result = cursor.fetchone()

            if not result:
                return False, f"Product id {product_id} not found."

            price = float(result[0])
            productName = result[1]

            quantity_sold = int(quantity_sold)
            sale_amount = np.multiply(price, quantity_sold)

            query = """
                UPDATE product_sales 
                SET SALE_DATE = %s, QUANTITY_SOLD = %s, SALE_AMOUNT = %s
                WHERE SALE_ID = %s AND Product_ID = %s AND Branch_ID = %s
            """
            cursor.execute(query, (
                sale_date,
                quantity_sold,
                sale_amount,
                sale_Id,
                product_id,
                branch_id
            ))

            connection.commit()
            return True, f"Updated product {productName} sale information successfully"

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
