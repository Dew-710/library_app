import mysql.connector
from database.connect import get_db_connection

def get_user_by_email(email):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user

# Các hàm khác (get_books, add_user, v.v.) giữ nguyên nếu không liên quan đến mật khẩu

def add_user(full_name, email, password, card_type):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (full_name, email, password, card_type) VALUES (%s, %s, %s, %s)",
                   (full_name, email, password, card_type))  # Không mã hóa password
    conn.commit()
    cursor.close()
    conn.close()

def get_users():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, full_name, email, card_type FROM users")
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return users

def get_books():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT b.id, b.title, b.author, c.name as category, b.quantity, b.location FROM books b LEFT JOIN categories c ON b.category_id = c.id")
    books = cursor.fetchall()
    cursor.close()
    conn.close()
    return books

def get_book_by_id(book_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT b.id, b.title, b.author, c.name as category, b.quantity, b.location FROM books b LEFT JOIN categories c ON b.category_id = c.id WHERE b.id = %s", (book_id,))
    book = cursor.fetchone()
    cursor.close()
    conn.close()
    return book

def add_book(title, author, category_id, quantity, location):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO books (title, author, category_id, quantity, location) VALUES (%s, %s, %s, %s, %s)",
                   (title, author, category_id, quantity, location))
    conn.commit()
    cursor.close()
    conn.close()

def update_book(book_id, title, author, category_id, quantity, location):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE books SET title = %s, author = %s, category_id = %s, quantity = %s, location = %s WHERE id = %s",
                   (title, author, category_id, quantity, location, book_id))
    conn.commit()
    cursor.close()
    conn.close()

def delete_book(book_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM books WHERE id = %s", (book_id,))
    conn.commit()
    cursor.close()
    conn.close()

def get_categories():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, name FROM categories")
    categories = cursor.fetchall()
    cursor.close()
    conn.close()
    return categories

def get_borrow_records():
    conn = get_db_connection()
    if not conn:
        return []
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT br.id, br.user_id, br.book_id, br.borrow_date, br.due_date, br.return_date,
               u.full_name AS user_name, b.title AS book_title
        FROM borrow_records br
        JOIN users u ON br.user_id = u.id
        JOIN books b ON br.book_id = b.id
    """)
    records = cursor.fetchall()
    cursor.close()
    conn.close()
    return records if records else []

def get_borrowed_books_today():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT b.title, COUNT(br.id) as count
        FROM borrow_records br
        JOIN books b ON br.book_id = b.id
        WHERE DATE(br.borrow_date) = CURDATE()
        GROUP BY b.id, b.title
    """)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data
def update_borrow_record(borrow_id, return_date):
    conn = get_db_connection()
    if not conn:
        return False
    cursor = conn.cursor()
    cursor.execute("UPDATE borrow_records SET return_date = %s WHERE id = %s", (return_date, borrow_id))
    conn.commit()
    cursor.close()
    conn.close()
    return True