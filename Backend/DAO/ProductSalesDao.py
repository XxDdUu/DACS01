from Backend.DAO.DatabaseConnection import get_connection
import MySQLdb
import traceback

class ProductSalesDAO:
    def add_ProductSales(self, data):
        sale_Id = data.get("id")
        product_id =  data.get("product_id")
        branch_id = data.get("branch_id")
        sale_date =  data.get("date")
        quantity_sold =  data.get("quantity_sold")
        sale_amount_raw = data.get("amount").strip()

        connection = None
        cursor = None

        #Kiểm tra và ép kiểu giá
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
            query = """
                INSERT INTO PRODUCT_SALES
                (SALE_ID, Product_ID, Branch_ID, SALE_DATE, QUANTITY_SOLD, SALE_AMOUNT)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                sale_Id,
                product_id,
                branch_id,
                sale_date,
                quantity_sold,
                sale_amount
            ))

            connection.commit()
            return True, "Product_Sales add successfully"

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
        sale_amount_raw = data.get("amount").strip()

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
            query = """
                DELETE FROM product_sales 
                WHERE SALE_ID = %s AND Product_ID = %s AND Branch_ID = %s
            """
            cursor.execute(query, (
                sale_Id,
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
        sale_amount_raw = data.get("amount").strip()

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
            return True, "Product_Sales updated successfully"

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
