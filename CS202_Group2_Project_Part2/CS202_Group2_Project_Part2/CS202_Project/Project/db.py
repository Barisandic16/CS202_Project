import mysql.connector

def get_db_connection():
    conn = mysql.connector.connect(
        host='localhost',
        port = 3306,
        user='root',
        password='Utkubaris9703',
        database='FOOD_SYSTEM'
    )
    conn.cmd_reset_connection()  # ✅ prevent unread result inheritance
    return conn
