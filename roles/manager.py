import tkinter as tk
from tkinter import ttk, messagebox
from ui.sidebar import Sidebar
from database.models import get_books, get_book_by_id, add_book, update_book, get_borrow_records, get_borrowed_books_today, get_categories, get_db_connection, get_users, delete_book
from utils.charts import create_borrow_chart
from datetime import datetime, timedelta, date
from auth.register import RegisterWindow

class ManagerWindow:
    def __init__(self, root, user):
        self.root = root
        self.user = user
        self.root.title("Quản lý- Thư viện")

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
        tk.Button(search_frame, text="Thêm sách", command=self.add_book, bg="green", fg="white").grid(row=2, column=2, padx=5, pady=5)
        tk.Button(search_frame, text="Cập nhật", command=self.edit_book, bg="green", fg="white").grid(row=2, column=3, padx=5, pady=5)
        tk.Button(search_frame, text="Xóa sách", command=self.delete_book_gui, bg="red", fg="white").grid(row=2,column=4,padx=5,pady=5)
        tk.Button(search_frame, text="Mượn sách", command=self.borrow_book, bg="blue", fg="white").grid(row=2, column=5, padx=5, pady=5)

        self.detail_frame = tk.LabelFrame(books_frame, text="Chi tiết sách")
        self.detail_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
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
        self.accounts_tree = ttk.Treeview(accounts_frame, columns=("ID", "Họ Tên", "Email", "Loại thẻ"), show="headings")
        self.accounts_tree.heading("ID", text="ID")
        self.accounts_tree.heading("Họ Tên", text="Họ Tên")
        self.accounts_tree.heading("Email", text="Email")
        self.accounts_tree.heading("Loại thẻ", text="Loại thẻ")
        self.accounts_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        tk.Button(accounts_frame, text="Đăng ký tài khoản", command=lambda: RegisterWindow(tk.Toplevel(self.root), self.user, self.load_users), bg="green", fg="white").pack(pady=5)
        tk.Button(accounts_frame, text="Xóa tài khoản", command=self.delete_user_gui, bg="red", fg="white").pack(pady=5)
        self.load_users()
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
        self.load_borrow_records()
        self.pages["Mượn - Trả"] = borrow_frame

        # Thêm tab Thống kê với nhãn và biểu đồ
        self.stats_frame = tk.Frame(self.main_frame, bg="white")
        self.stats_label = tk.Label(self.stats_frame, text="Thống kê mượn sách trong ngày", font=("Arial", 14), bg="white")
        self.stats_label.pack(pady=10)
        today = datetime.now().date()
        today_str = today.strftime('%d/%m/%Y')
        borrowed_books_today = get_borrowed_books_today()
        num_borrowed_today = len(borrowed_books_today) if borrowed_books_today else 0
        self.stats_count_label = tk.Label(
            self.stats_frame,
            text=f"Số sách mượn ngày {today_str}: {num_borrowed_today} cuốn",
            font=("Arial", 12),
            bg="white"
        )
        self.stats_count_label.pack(pady=5)
        create_borrow_chart(self.stats_frame)
        self.pages["Thống kê"] = self.stats_frame

    def update_stats_page(self):
        """Cập nhật lại nội dung của tab Thống kê"""
        for widget in self.stats_frame.winfo_children():
            widget.destroy()
        self.stats_label = tk.Label(self.stats_frame, text="Thống kê mượn sách trong ngày", font=("Arial", 14), bg="white")
        self.stats_label.pack(pady=10)
        today = datetime.now().date()
        today_str = today.strftime('%d/%m/%Y')
        borrowed_books_today = get_borrowed_books_today()
        num_borrowed_today = len(borrowed_books_today) if borrowed_books_today else 0
        self.stats_count_label = tk.Label(
            self.stats_frame,
            text=f"Số sách mượn ngày {today_str}: {num_borrowed_today} cuốn",
            font=("Arial", 12),
            bg="white"
        )
        self.stats_count_label.pack(pady=5)
        create_borrow_chart(self.stats_frame)

    def show_page(self, page_name):
        for frame in self.pages.values():
            frame.pack_forget()
        self.pages[page_name].pack(fill=tk.BOTH, expand=True)

    def load_books(self):
        for item in self.books_tree.get_children():
            self.books_tree.delete(item)
        books = get_books()
        for book in books:
            self.books_tree.insert("", tk.END, values=(book['id'], book['title'], book['author'], book['category'], book['quantity'], book['location']))

    def search_books(self):
        for item in self.books_tree.get_children():
            self.books_tree.delete(item)
        books = get_books()
        book_id = self.book_id_entry.get().strip()
        book_title = self.book_title_entry.get().strip().lower()
        book_author = self.book_author_entry.get().strip().lower()
        category = self.category_var.get().strip()
        filtered_books = books
        if book_id:
            filtered_books = [b for b in filtered_books if str(b['id']) == book_id]
        if book_title:
            filtered_books = [b for b in filtered_books if all(char in b['title'].lower() for char in book_title)]
        if book_author:
            filtered_books = [b for b in filtered_books if all(char in b['author'].lower() for char in book_author)]
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
        if not records:
            return
        current_date = datetime.now().date()
        for record in records:
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
        conn = get_db_connection()
        if not conn:
            messagebox.showerror("Lỗi", "Không thể kết nối cơ sở dữ liệu!")
            return
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT book_id FROM borrow_records WHERE id = %s", (borrow_id,))
            result = cursor.fetchone()
            if not result:
                messagebox.showerror("Lỗi", "Bản ghi mượn không tồn tại!")
                return
            book_id = result['book_id']
            cursor.execute("UPDATE borrow_records SET return_date = %s WHERE id = %s", (datetime.now().date(), borrow_id))
            cursor.execute("UPDATE books SET quantity = quantity + 1 WHERE id = %s", (book_id,))
            conn.commit()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi trả sách: {e}")
            conn.rollback()
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

    def add_book(self):
        add_window = tk.Toplevel(self.root)
        add_window.title("Thêm sách")
        add_window.geometry("300x400")

        tk.Label(add_window, text="Tên sách:").pack(pady=5)
        title_entry = tk.Entry(add_window)
        title_entry.pack(pady=5)

        tk.Label(add_window, text="Tác giả:").pack(pady=5)
        author_entry = tk.Entry(add_window)
        author_entry.pack(pady=5)

        tk.Label(add_window, text="Thể loại:").pack(pady=5)
        category_var = tk.StringVar()
        categories = get_categories()
        category_names = [cat['name'] for cat in categories]
        category_menu = ttk.Combobox(add_window, textvariable=category_var, values=category_names)
        category_menu.pack(pady=5)
        if category_names:
            category_menu.current(0)
        else:
            messagebox.showwarning("Cảnh báo", "Không có thể loại nào. Vui lòng thêm thể loại trước!")

        tk.Label(add_window, text="Số lượng:").pack(pady=5)
        quantity_entry = tk.Entry(add_window)
        quantity_entry.pack(pady=5)

        tk.Label(add_window, text="Vị trí:").pack(pady=5)
        location_entry = tk.Entry(add_window)
        location_entry.pack(pady=5)

        tk.Button(add_window, text="Lưu", command=lambda: self.save_book(add_window, title_entry.get(), author_entry.get(), category_var.get(), quantity_entry.get(), location_entry.get()), bg="green", fg="white").pack(pady=10)

    def save_book(self, window, title, author, category_name, quantity, location):
        try:
            if not title or not author or not category_name or not quantity or not location:
                messagebox.showerror("Lỗi", "Vui lòng điền đầy đủ thông tin!")
                return
            category = next((cat for cat in get_categories() if cat['name'] == category_name), None)
            if not category:
                messagebox.showerror("Lỗi", "Thể loại không hợp lệ!")
                return
            add_book(title, author, category['id'], int(quantity), location)
            self.load_books()
            window.destroy()
            messagebox.showinfo("Thành công", "Thêm sách thành công!")
        except ValueError:
            messagebox.showerror("Lỗi", "Số lượng phải là số!")

    def edit_book(self):
        selected_item = self.books_tree.selection()
        if not selected_item:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một cuốn sách!")
            return
        book_id = self.books_tree.item(selected_item[0])['values'][0]
        book = get_book_by_id(book_id)
        if not book:
            messagebox.showerror("Lỗi", "Không tìm thấy sách!")
            return

        edit_window = tk.Toplevel(self.root)
        edit_window.title("Cập nhật sách")
        edit_window.geometry("300x300")

        tk.Label(edit_window, text="Tên sách:").pack(pady=5)
        title_entry = tk.Entry(edit_window)
        title_entry.insert(0, book['title'])
        title_entry.pack(pady=5)

        tk.Label(edit_window, text="Tác giả:").pack(pady=5)
        author_entry = tk.Entry(edit_window)
        author_entry.insert(0, book['author'])
        author_entry.pack(pady=5)

        tk.Label(edit_window, text="Thể loại:").pack(pady=5)
        category_var = tk.StringVar()
        category_menu = ttk.Combobox(edit_window, textvariable=category_var, values=[cat['name'] for cat in get_categories()])
        category_menu.pack(pady=5)
        category_menu.set(book['category'])

        tk.Label(edit_window, text="Số lượng:").pack(pady=5)
        quantity_entry = tk.Entry(edit_window)
        quantity_entry.insert(0, book['quantity'])
        quantity_entry.pack(pady=5)

        tk.Label(edit_window, text="Vị trí:").pack(pady=5)
        location_entry = tk.Entry(edit_window)
        location_entry.insert(0, book['location'])
        location_entry.pack(pady=5)

        tk.Button(edit_window, text="Cập nhật", command=lambda: self.update_book(edit_window, book_id, title_entry.get(), author_entry.get(), category_var.get(), quantity_entry.get(), location_entry.get()), bg="green", fg="white").pack(pady=10)

    def update_book(self, window, book_id, title, author, category_name, quantity, location):
        try:
            if not title or not author or not category_name or not quantity or not location:
                messagebox.showerror("Lỗi", "Vui lòng điền đầy đủ thông tin!")
                return
            category = next((cat for cat in get_categories() if cat['name'] == category_name), None)
            if not category:
                messagebox.showerror("Lỗi", "Thể loại không hợp lệ!")
                return
            update_book(book_id, title, author, category['id'], int(quantity), location)
            self.load_books()
            window.destroy()
            messagebox.showinfo("Thành công", "Cập nhật sách thành công!")
        except ValueError:
            messagebox.showerror("Lỗi", "Số lượng phải là số!")

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

        borrow_window = tk.Toplevel(self.root)
        borrow_window.title("Mượn sách")
        borrow_window.geometry("300x200")

        tk.Label(borrow_window, text="Chọn người mượn:").pack(pady=5)
        users = get_users()
        # Chỉ hiển thị nhân viên và độc giả trong danh sách người mượn
        filtered_users = [user for user in users if user['card_type'].lower() in ['nhân viên', 'độc giả']]
        user_var = tk.StringVar()
        user_menu = ttk.Combobox(borrow_window, textvariable=user_var, values=[user['full_name'] for user in filtered_users])
        user_menu.pack(pady=5)
        if filtered_users:
            user_menu.current(0)
        else:
            messagebox.showwarning("Cảnh báo", "Không có nhân viên hoặc độc giả nào để mượn sách!")
            borrow_window.destroy()
            return

        tk.Button(borrow_window, text="Xác nhận mượn", command=lambda: self.confirm_borrow(borrow_window, book_id, user_var.get(), filtered_users), bg="blue", fg="white").pack(pady=10)

    def confirm_borrow(self, window, book_id, user_name, users):
        if not user_name:
            messagebox.showerror("Lỗi", "Vui lòng chọn người mượn!")
            return
        user = next((u for u in users if u['full_name'] == user_name), None)
        if not user:
            messagebox.showerror("Lỗi", "Không tìm thấy người mượn!")
            return
        # Đảm bảo chỉ nhân viên hoặc độc giả được mượn sách
        if user['card_type'].lower() not in ['nhân viên', 'độc giả']:
            messagebox.showerror("Lỗi", "Chỉ nhân viên hoặc độc giả mới có thể mượn sách!")
            return

        conn = get_db_connection()
        if not conn:
            messagebox.showerror("Lỗi", "Không thể kết nối cơ sở dữ liệu!")
            return
        cursor = conn.cursor()
        try:
            borrow_date = datetime.now().date()
            due_date = borrow_date + timedelta(days=14)
            cursor.execute(
                "INSERT INTO borrow_records (user_id, book_id, borrow_date, due_date) VALUES (%s, %s, %s, %s)",
                (user['id'], book_id, borrow_date, due_date)
            )
            cursor.execute("UPDATE books SET quantity = quantity - 1 WHERE id = %s", (book_id,))
            conn.commit()
            messagebox.showinfo("Thành công", f"Mượn sách thành công!\nNgày mượn: {borrow_date.strftime('%d/%m/%Y')}\nHạn trả: {due_date.strftime('%d/%m/%Y')}")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi mượn sách: {e}")
            conn.rollback()
        finally:
            cursor.close()
            conn.close()

        self.load_books()
        self.load_borrow_records()
        self.update_stats_page()  # Cập nhật tab Thống kê sau khi mượn sách
        window.destroy()

    def load_users(self):
        for item in self.accounts_tree.get_children():
            self.accounts_tree.delete(item)
        users = get_users()
        # Lọc chỉ hiển thị nhân viên và độc giả, loại bỏ Admin và Quản lý
        filtered_users = [user for user in users if user['card_type'].lower() in ['nhân viên', 'độc giả']]
        for user in filtered_users:
            self.accounts_tree.insert("", tk.END, values=(user['id'], user['full_name'], user['email'], user['card_type']))

    def logout(self):
        self.root.destroy()
        new_root = tk.Tk()
        from auth.login import LoginWindow
        LoginWindow(new_root)
        new_root.mainloop()

    def delete_book_gui(self):
        selected_item = self.books_tree.selection()
        if not selected_item:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một cuốn sách để xóa!")
            return
        book_id = self.books_tree.item(selected_item[0])['values'][0]
        book_title = self.books_tree.item(selected_item[0])['values'][1]
        if messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn xóa sách có tên: {book_title}?"):
            try:
                delete_book(book_id)
                self.load_books()
                messagebox.showinfo("Thành công", "Xóa sách thành công!")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Lỗi khi xóa sách: {e}")

    def delete_user_gui(self):
        selected_item = self.accounts_tree.selection()
        if not selected_item:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một tài khoản để xóa!")
            return
        user_id = self.accounts_tree.item(selected_item[0])['values'][0]
        user_name = self.accounts_tree.item(selected_item[0])['values'][1]
        if messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn xóa tài khoản có tên: {user_name}?"):
            try:
                # Giả sử bạn đã có hàm delete_user trong database.models
                conn = get_db_connection()
                if not conn:
                    messagebox.showerror("Lỗi", "Không thể kết nối cơ sở dữ liệu!")
                    return
                cursor = conn.cursor()
                cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
                conn.commit()
                cursor.close()
                conn.close()
                self.load_users()
                messagebox.showinfo("Thành công", "Xóa tài khoản thành công!")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Lỗi khi xóa tài khoản: {e}")
