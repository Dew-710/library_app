MariaDB [library_management]> -- BẢNG NGƯỜI DÙNG
MariaDB [library_management]> CREATE TABLE users (
    ->     id INT PRIMARY KEY AUTO_INCREMENT,
    ->     full_name VARCHAR(100) NOT NULL,
    ->     gender ENUM('Nam', 'Nữ', 'Khác'),
    ->     address VARCHAR(255),
    ->     phone VARCHAR(20),
    ->     email VARCHAR(100) UNIQUE,
    ->     password VARCHAR(255) NOT NULL,
    ->     card_issue_date DATE,
    ->     card_type ENUM('Admin', 'Quản lý', 'Nhân viên', 'Độc giả') DEFAULT 'Độc giả'
    -> ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
Query OK, 0 rows affected (0,005 sec)

MariaDB [library_management]> 
MariaDB [library_management]> -- BẢNG THỂ LOẠI SÁCH
MariaDB [library_management]> CREATE TABLE categories (
    ->     id INT PRIMARY KEY AUTO_INCREMENT,
    ->     name VARCHAR(100) UNIQUE NOT NULL
    -> ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
Query OK, 0 rows affected (0,005 sec)

MariaDB [library_management]> 
MariaDB [library_management]> -- BẢNG SÁCH
MariaDB [library_management]> CREATE TABLE books (
    ->     id INT PRIMARY KEY AUTO_INCREMENT,
    ->     title VARCHAR(255) NOT NULL,
    ->     author VARCHAR(100),
    ->     category_id INT,
    ->     quantity INT DEFAULT 0,
    ->     location VARCHAR(100),
    ->     CONSTRAINT fk_books_category FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE SET NULL ON UPDATE CASCADE
    -> ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
Query OK, 0 rows affected (0,005 sec)

MariaDB [library_management]> 
MariaDB [library_management]> -- BẢNG LỊCH SỬ MƯỢN TRẢ
MariaDB [library_management]> CREATE TABLE borrow_records (
    ->     id INT PRIMARY KEY AUTO_INCREMENT,
    ->     user_id INT,
    ->     book_id INT,
    ->     borrow_date DATE,
    ->     return_date DATE,
    ->     due_date DATE,
    ->     CONSTRAINT fk_borrow_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE,
    ->     CONSTRAINT fk_borrow_book FOREIGN KEY (book_id) REFERENCES books(id) ON DELETE CASCADE ON UPDATE CASCADE
    -> ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
Query OK, 0 rows affected (0,006 sec)

MariaDB [library_management]> 
MariaDB [library_management]> -- Thêm tài khoản mẫu
MariaDB [library_management]> INSERT INTO users (full_name, gender, address, phone, email, password, card_issue_date, card_type)
    -> VALUES 
    -> ('Admin Root', 'Nam', 'Tòa nhà A', '0123456789', 'admin@library.com', '123456', CURDATE(), 'Admin'),
    -> ('Admin Three', 'Nam', 'Tòa nhà B', '0981654321', 'admin3@library.com', 'admin123', CURDATE(), 'Admin');
Query OK, 2 rows affected (0,001 sec)
Records: 2  Duplicates: 0  Warnings: 0

MariaDB [library_management]> 
MariaDB [library_management]> -- Thêm các thể loại mẫu
MariaDB [library_management]> INSERT INTO categories (name) VALUES 
    -> ('Văn học'), 
    -> ('Khoa học'), 
    -> ('Lịch sử'),
    -> ('Sách khoa học và viễn tưởng'), 
    -> ('Tài liệu tham khảo'), 
    -> ('Tiểu thuyết'),
    -> ('Sách Công Nghệ'),
    -> ('Sách Hướng Dẫn'),
    -> ('Sách Ngoại Ngữ');
Query OK, 9 rows affected (0,001 sec)
Records: 9  Duplicates: 0  Warnings: 0

MariaDB [library_management]> 
MariaDB [library_management]> -- Chỉnh sửa tên thể loại (nếu cần)
MariaDB [library_management]> UPDATE categories SET name = 'Sách giáo khoa' WHERE name = 'Văn học';
Query OK, 1 row affected (0,001 sec)
Rows matched: 1  Changed: 1  Warnings: 0

MariaDB [library_management]> UPDATE categories SET name = 'Truyện tranh' WHERE name = 'Khoa học';
Query OK, 1 row affected (0,001 sec)
Rows matched: 1  Changed: 1  Warnings: 0

MariaDB [library_management]> UPDATE categories SET name = 'Sách thiếu nhi' WHERE name = 'Lịch sử';
Query OK, 1 row affected (0,001 sec)
Rows matched: 1  Changed: 1  Warnings: 0

MariaDB [library_management]> 
MariaDB [library_management]> -- Cập nhật borrow_records nếu cần
MariaDB [library_management]> UPDATE borrow_records 
    -> SET borrow_date = '2025-05-25', due_date = '2025-06-08' 
    -> WHERE borrow_date IS NULL OR due_date IS NULL;
Query OK, 0 rows affected (0,000 sec)
Rows matched: 0  Changed: 0  Warnings: 0

MariaDB [library_management]> 
MariaDB [library_management]> -- SELECT kiểm tra
MariaDB [library_management]> SELECT * FROM users;
+----+-------------+--------+-------------+------------+--------------------+----------+-----------------+-----------+
| id | full_name   | gender | address     | phone      | email              | password | card_issue_date | card_type |
+----+-------------+--------+-------------+------------+--------------------+----------+-----------------+-----------+
|  1 | Admin Root  | Nam    | Tòa nhà A   | 0123456789 | admin@library.com  | 123456   | 2025-06-04      | Admin     |
|  2 | Admin Three | Nam    | Tòa nhà B   | 0981654321 | admin3@library.com | admin123 | 2025-06-04      | Admin     |
+----+-------------+--------+-------------+------------+--------------------+----------+-----------------+-----------+
2 rows in set (0,000 sec)

MariaDB [library_management]> SELECT * FROM categories;
+----+--------------------------------------+
| id | name                                 |
+----+--------------------------------------+
|  7 | Sách Công Nghệ                       |
|  1 | Sách giáo khoa                       |
|  8 | Sách Hướng Dẫn                       |
|  4 | Sách khoa học và viễn tưởng          |
|  9 | Sách Ngoại Ngữ                       |
|  3 | Sách thiếu nhi                       |
|  5 | Tài liệu tham khảo                   |
|  6 | Tiểu thuyết                          |
|  2 | Truyện tranh                         |
+----+--------------------------------------+
9 rows in set (0,000 sec)

MariaDB [library_management]> SELECT * FROM books;
Empty set (0,000 sec)

MariaDB [library_management]> SELECT * FROM borrow_records;
Empty set (0,000 sec)

MariaDB [library_management]> -- Giả sử các category_id lần lượt từ 1 đến 9 cho các thể loại đã thêm ở trên
MariaDB [library_management]> INSERT INTO books (title, author, category_id, quantity, location) VALUES
    -> ('Dế Mèn Phiêu Lưu Ký', 'Tô Hoài', 1, 5, 'A1'),
    -> ('Harry Potter và Hòn Đá Phù Thủy', 'J.K. Rowling', 6, 4, 'A2'),
    -> ('Tôi Thấy Hoa Vàng Trên Cỏ Xanh', 'Nguyễn Nhật Ánh', 1, 3, 'A3'),
    -> ('Sapiens: Lược Sử Loài Người', 'Yuval Noah Harari', 2, 2, 'B1'),
    -> ('Lập Trình Python Cho Người Mới Bắt Đầu', 'Nguyễn Văn A', 7, 7, 'B2'),
    -> ('English Grammar In Use', 'Raymond Murphy', 9, 6, 'B3');
Query OK, 6 rows affected (0,011 sec)
Records: 6  Duplicates: 0  Warnings: 0

MariaDB [library_management]> 


