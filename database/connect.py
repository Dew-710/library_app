import mysql.connector
from mysql.connector import Error
import logging

# Cấu hình logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="100106",
        database="library_management"
    )

# Kiểm tra kết nối
if __name__ == "__main__":
    connection = get_db_connection()
    if connection is None:
        print("Không thể kết nối đến cơ sở dữ liệu. Vui lòng kiểm tra lại cấu hình.")
    else:
        print("Kết nối thành công!")
        connection.close()