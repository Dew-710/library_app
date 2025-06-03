import tkinter as tk
from tkinter import ttk, messagebox
from ui.sidebar import Sidebar
from database.models import get_books, get_book_by_id, get_borrow_records, get_borrowed_books_today, get_categories, get_db_connection
from utils.charts import create_borrow_chart
from datetime import datetime, timedelta, date

class ReaderWindow:
    def __init__(self, root, user):
        self.root = root
        self.user = user
        self.root.title("Độc giả - Thư viện")


        self.root.state('zoomed')


        self.root.resizable(False, False)
        sidebar_frame = tk.Frame(self.root, width=200, bg="#6B7280")
        sidebar_frame.pack(side=tk.LEFT, fill=tk.Y)
        Sidebar(sidebar_frame, self, user)

        self.main_frame = tk.Frame(self.root, bg="white")
        self.main_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.pages = {}
        self.init_pages()
        self.show_page("Trang chủ")

    def init_pages(self):
        home_frame = tk.Frame(self.main_frame, bg="Gray")
        welcome_label = tk.Label(home_frame, text="Welcome To Library", font=("Arial", 60), bg="Gray")
        welcome_label.pack(expand=True)
        self.pages["Trang chủ"] = home_frame

        books_frame = tk.Frame(self.main_frame, bg="white")
        self.books_tree = ttk.Treeview(books_frame, columns=("Mã Sách", "Tên Sách", "Tác Giả", "Thể Loại", "Số Lượng", "Vị trí"), show="headings")
        self.books_tree.heading("Mã Sách", text="Mã Sách")
        self.books_tree.heading("Tên Sách", text="Tên Sách")
        self.books_tree.heading("Tác Giả", text="Tác Giả")
        self.books_tree.heading("Thể Loại", text="Thể Loại")
        self.books_tree.heading("Số Lượng", text="Số Lượng")
        self.books_tree.heading("Vị trí", text="Vị trí")
        self.books_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.books_tree.bind("<<TreeviewSelect>>", self.on_book_select)

        search_frame = tk.LabelFrame(books_frame, text="Thiết lập thông tin tìm kiếm")
        search_frame.pack(fill=tk.X, padx=5, pady=5)
        tk.Label(search_frame, text="Mã sách:").grid(row=0, column=0, padx=5)
        self.book_id_entry = tk.Entry(search_frame)
        self.book_id_entry.grid(row=0, column=1, padx=5)
        tk.Label(search_frame, text="Tên sách:").grid(row=0, column=2, padx=5)
        self.book_title_entry = tk.Entry(search_frame)
        self.book_title_entry.grid(row=0, column=3, padx=5)
        tk.Label(search_frame, text="Tác giả:").grid(row=1, column=0, padx=5, pady=5)
        self.book_author_entry = tk.Entry(search_frame)
        self.book_author_entry.grid(row=1, column=1, padx=5, pady=5)
        tk.Label(search_frame, text="Thể loại:").grid(row=1, column=2, padx=5, pady=5)
        self.category_var = tk.StringVar()
        self.category_menu = ttk.Combobox(search_frame, textvariable=self.category_var, values=[cat['name'] for cat in get_categories()])
        self.category_menu.grid(row=1, column=3, padx=5, pady=5)
        tk.Button(search_frame, text="Tìm kiếm", command=self.search_books, bg="yellow", fg="black").grid(row=2, column=0, padx=5, pady=5)
        tk.Button(search_frame, text="Xem tất cả", command=self.load_books, bg="green", fg="white").grid(row=2, column=1, padx=5, pady=5)
        tk.Button(search_frame, text="Mượn sách", command=self.borrow_book, bg="blue", fg="white").grid(row=2, column=2, padx=5, pady=5)

        self.detail_frame = tk.LabelFrame(books_frame, text="Chi tiết sách")
        self.detail_frame.pack(fill=tk.X, padx=5, pady=5)
        tk.Label(self.detail_frame, text="Mã sách:").grid(row=0, column=0, padx=5, pady=2)
        self.detail_id = tk.Label(self.detail_frame, text="")
        self.detail_id.grid(row=0, column=1, padx=5, pady=2)
        tk.Label(self.detail_frame, text="Tên sách:").grid(row=1, column=0, padx=5, pady=2)
        self.detail_title = tk.Label(self.detail_frame, text="")
        self.detail_title.grid(row=1, column=1, padx=5, pady=2)
        tk.Label(self.detail_frame, text="Tác giả:").grid(row=2, column=0, padx=5, pady=2)
        self.detail_author = tk.Label(self.detail_frame, text="")
        self.detail_author.grid(row=2, column=1, padx=5, pady=2)
        tk.Label(self.detail_frame, text="Thể Loại:").grid(row=3, column=0, padx=5, pady=2)
        self.detail_category = tk.Label(self.detail_frame, text="")
        self.detail_category.grid(row=3, column=1, padx=5, pady=2)
        tk.Label(self.detail_frame, text="Số lượng:").grid(row=4, column=0, padx=5, pady=2)
        self.detail_quantity = tk.Label(self.detail_frame, text="")
        self.detail_quantity.grid(row=4, column=1, padx=5, pady=2)
        tk.Label(self.detail_frame, text="Vị trí:").grid(row=5, column=0, padx=5, pady=2)
        self.detail_location = tk.Label(self.detail_frame, text="")
        self.detail_location.grid(row=5, column=1, padx=5, pady=2)

        self.load_books()
        self.pages["Sách"] = books_frame

        accounts_frame = tk.Frame(self.main_frame, bg="white")
        tk.Label(accounts_frame, text="Bạn không có quyền xem danh sách tài khoản.").pack(pady=20)
        self.pages["Tài khoản"] = accounts_frame

        borrow_frame = tk.Frame(self.main_frame, bg="white")
        self.borrow_tree = ttk.Treeview(borrow_frame, columns=("Mã Mượn", "Tên Người Mượn", "Tên Sách", "Ngày Mượn", "Hạn Trả", "Ngày Trả", "Trạng Thái"), show="headings")
        self.borrow_tree.heading("Mã Mượn", text="Mã Mượn")
        self.borrow_tree.heading("Tên Người Mượn", text="Tên Người Mượn")
        self.borrow_tree.heading("Tên Sách", text="Tên Sách")
        self.borrow_tree.heading("Ngày Mượn", text="Ngày Mượn")
        self.borrow_tree.heading("Hạn Trả", text="Hạn Trả")
        self.borrow_tree.heading("Ngày Trả", text="Ngày Trả")
        self.borrow_tree.heading("Trạng Thái", text="Trạng Thái")
        self.borrow_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.borrow_tree.bind("<<TreeviewSelect>>", self.on_borrow_select)

        self.return_button = tk.Button(borrow_frame, text="Trả sách", command=self.return_book, bg="red", fg="white", state='disabled')
        self.return_button.pack(pady=5)
        self.pages["Mượn - Trả"] = borrow_frame

        stats_frame = tk.Frame(self.main_frame, bg="white")
        tk.Label(stats_frame, text="Thống kê mượn sách trong ngày", font=("Arial", 14)).pack(pady=10)

        # Thêm phần hiển thị số sách mượn trong ngày và ngày hiện tại
        today = datetime.now().date()
        today_str = today.strftime('%d/%m/%Y')  # Định dạng ngày: 27/05/2025
        borrowed_books_today = get_borrowed_books_today()
        num_borrowed_today = len(borrowed_books_today) if borrowed_books_today else 0
        stats_label = tk.Label(
            stats_frame,
            text=f"Số sách mượn ngày {today_str}: {num_borrowed_today} cuốn",
            font=("Arial", 12),
            bg="white"
        )
        stats_label.pack(pady=5)

        create_borrow_chart(stats_frame)
        self.pages["Thống kê"] = stats_frame

    def show_page(self, page_name):
        for frame in self.pages.values():
            frame.pack_forget()
        self.pages[page_name].pack(fill=tk.BOTH, expand=True)
        if page_name == "Mượn - Trả":
            self.load_borrow_records()

    def load_books(self):
        for item in self.books_tree.get_children():
            self.books_tree.delete(item)
        books = get_books()
        if not books:
            messagebox.showinfo("Thông báo", "Không có sách nào trong thư viện!")
            return
        for book in books:
            self.books_tree.insert("", tk.END, values=(book['id'], book['title'], book['author'], book['category'], book['quantity'], book['location']))

    def search_books(self):
        for item in self.books_tree.get_children():
            self.books_tree.delete(item)
        books = get_books()
        if not books:
            messagebox.showinfo("Thông báo", "Không có sách nào trong thư viện!")
            return
        book_id = self.book_id_entry.get().strip()
        book_title = self.book_title_entry.get().strip().lower()
        book_author = self.book_author_entry.get().strip().lower()
        category = self.category_var.get().strip()
        filtered_books = books
        if book_id:
            filtered_books = [b for b in filtered_books if str(b['id']) == book_id]
        if book_title:
            filtered_books = [b for b in filtered_books if book_title in b['title'].lower()]
        if book_author:
            filtered_books = [b for b in filtered_books if book_author in b['author'].lower()]
        if category:
            filtered_books = [b for b in filtered_books if b['category'] == category]
        if not filtered_books:
            messagebox.showinfo("Thông báo", "Không tìm thấy sách phù hợp!")
        for book in filtered_books:
            self.books_tree.insert("", tk.END, values=(book['id'], book['title'], book['author'], book['category'], book['quantity'], book['location']))

    def load_borrow_records(self):
        for item in self.borrow_tree.get_children():
            self.borrow_tree.delete(item)
        records = get_borrow_records()
        print(f"Records from get_borrow_records: {records}")
        if not records:
            messagebox.showinfo("Thông báo", "Không có bản ghi mượn nào trong hệ thống.")
            return
        current_date = datetime.now().date()
        user_id = self.user['id']
        print(f"Current user_id: {user_id}")
        for record in records:
            print(f"Record user_id: {record.get('user_id')}")
            if record.get('user_id') == user_id:
                borrow_date = record.get('borrow_date')
                due_date = record.get('due_date')
                return_date = record.get('return_date')

                borrow_date_str = borrow_date.strftime('%Y-%m-%d') if isinstance(borrow_date, (datetime, date)) else str(borrow_date) if borrow_date else "N/A"
                due_date_str = due_date.strftime('%Y-%m-%d') if isinstance(due_date, (datetime, date)) else str(due_date) if due_date else "N/A"
                return_date_str = return_date.strftime('%Y-%m-%d') if isinstance(return_date, (datetime, date)) else str(return_date) if return_date else "Chưa trả"

                if return_date:
                    status = "Đã trả"
                else:
                    status = "Không xác định"
                    if due_date:
                        try:
                            due_date_obj = due_date if isinstance(due_date, (datetime, date)) else datetime.strptime(str(due_date), '%Y-%m-%d').date()
                            if current_date > due_date_obj:
                                status = "Quá hạn"
                            else:
                                status = "Chưa trả"
                        except (ValueError, TypeError) as e:
                            print(f"Lỗi xử lý ngày: {e}, due_date: {due_date}")

                self.borrow_tree.insert("", tk.END, values=(
                    record.get('id', 'N/A'),
                    record.get('user_name', 'N/A'),
                    record.get('book_title', 'N/A'),
                    borrow_date_str,
                    due_date_str,
                    return_date_str,
                    status
                ))
        if not self.borrow_tree.get_children():
            messagebox.showinfo("Thông báo", "Bạn chưa mượn sách nào.")

    def on_borrow_select(self, event):
        selected_item = self.borrow_tree.selection()
        if not selected_item:
            self.return_button.config(state='disabled')
        else:
            self.return_button.config(state='normal')

    def return_book(self):
        selected_item = self.borrow_tree.selection()
        if not selected_item:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một bản ghi mượn để trả!")
            return
        borrow_id = self.borrow_tree.item(selected_item[0])['values'][0]
        print(f"Selected borrow_id: {borrow_id}")  # Gỡ lỗi
        conn = get_db_connection()
        if not conn:
            messagebox.showerror("Lỗi", "Không thể kết nối cơ sở dữ liệu!")
            return
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT book_id FROM borrow_records WHERE id = %s", (borrow_id,))
            result = cursor.fetchone()
            print(f"Query result for borrow_id {borrow_id}: {result}")
            if not result:
                messagebox.showerror("Lỗi", "Bản ghi mượn không tồn tại!")
                cursor.close()
                conn.close()
                return
            book_id = result['book_id']
            print(f"Book ID to return: {book_id}")
            cursor.execute("UPDATE borrow_records SET return_date = %s WHERE id = %s", (datetime.now().date(), borrow_id))
            cursor.execute("UPDATE books SET quantity = quantity + 1 WHERE id = %s", (book_id,))
            conn.commit()
            print("Database updated successfully.")
        except Exception as e:
            print(f"Error returning book: {e}")
            conn.rollback()
            messagebox.showerror("Lỗi", f"Lỗi khi trả sách: {e}")
            cursor.close()
            conn.close()
            return
        finally:
            cursor.close()
            conn.close()

        self.load_borrow_records()
        self.load_books()
        messagebox.showinfo("Thành công", "Trả sách thành công!")

    def on_book_select(self, event):
        selected_item = self.books_tree.selection()
        if selected_item:
            book_id = self.books_tree.item(selected_item[0])['values'][0]
            book = get_book_by_id(book_id)
            if book:
                self.detail_id.config(text=book['id'])
                self.detail_title.config(text=book['title'])
                self.detail_author.config(text=book['author'])
                self.detail_category.config(text=book['category'])
                self.detail_quantity.config(text=book['quantity'])
                self.detail_location.config(text=book['location'])

    def view_book_details(self):
        selected_item = self.books_tree.selection()
        if not selected_item:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một cuốn sách!")
            return

    def borrow_book(self):
        selected_item = self.books_tree.selection()
        if not selected_item:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một cuốn sách để mượn!")
            return
        book_id = self.books_tree.item(selected_item[0])['values'][0]
        book = get_book_by_id(book_id)
        if not book or book['quantity'] <= 0:
            messagebox.showerror("Lỗi", "Sách không có sẵn để mượn!")
            return

        conn = get_db_connection()
        if not conn:
            messagebox.showerror("Lỗi", "Không thể kết nối cơ sở dữ liệu!")
            return
        cursor = conn.cursor()
        borrow_date = datetime.now().date()
        due_date = borrow_date + timedelta(days=14)
        try:
            cursor.execute(
                "INSERT INTO borrow_records (user_id, book_id, borrow_date, due_date) VALUES (%s, %s, %s, %s)",
                (self.user['id'], book_id, borrow_date, due_date)
            )
            cursor.execute("UPDATE books SET quantity = quantity - 1 WHERE id = %s", (book_id,))
            conn.commit()
            print(f"Inserted borrow record for user_id: {self.user['id']}, book_id: {book_id}")
        except Exception as e:
            print(f"Error inserting borrow record: {e}")
            conn.rollback()
            messagebox.showerror("Lỗi", f"Lỗi khi mượn sách: {e}")
            cursor.close()
            conn.close()
            return
        finally:
            cursor.close()
            conn.close()

        self.load_books()
        self.load_borrow_records()
        messagebox.showinfo("Thành công", "Mượn sách thành công! Vui lòng kiểm tra ở mục 'Mượn - Trả'.")

    def logout(self):
        self.root.destroy()
        new_root = tk.Tk()
        from auth.login import LoginWindow
        LoginWindow(new_root)
        new_root.mainloop()