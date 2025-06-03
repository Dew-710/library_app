import tkinter as tk
from tkinter import messagebox
from database.models import add_user,get_user_by_email

class RegisterWindow:
    def __init__(self, root, user, callback=None):
        self.root = root
        self.user = user  # Người dùng hiện tại để kiểm tra phân quyền
        self.callback = callback  # Thêm callback để gọi lại sau khi đăng ký
        self.root.title("Đăng ký tài khoản")
        self.root.geometry("300x400")

        tk.Label(root, text="Họ tên:").pack(pady=5)
        self.full_name_entry = tk.Entry(root)
        self.full_name_entry.pack(pady=5)

        tk.Label(root, text="Email:").pack(pady=5)
        self.email_entry = tk.Entry(root)
        self.email_entry.pack(pady=5)

        tk.Label(root, text="Mật khẩu:").pack(pady=5)
        self.password_entry = tk.Entry(root, show="*")  # Ẩn ký tự mật khẩu
        self.password_entry.pack(pady=5)

        tk.Label(root, text="Nhập lại mật khẩu:").pack(pady=5)
        self.password_again_entry = tk.Entry(root, show="*")  # Ẩn ký tự mật khẩu
        self.password_again_entry.pack(pady=5)

        tk.Label(root, text="Loại tài khoản:").pack(pady=5)
        self.card_type_var = tk.StringVar()
        allowed_types = self.get_allowed_card_types()
        if not allowed_types:
            messagebox.showerror("Lỗi", "Bạn không có quyền tạo tài khoản!")
            self.root.destroy()
            return
        self.card_type_menu = tk.OptionMenu(root, self.card_type_var, *allowed_types)
        self.card_type_menu.pack(pady=5)
        self.card_type_var.set(allowed_types[0])

        tk.Button(root, text="Đăng ký", command=self.register).pack(pady=10)

    def get_allowed_card_types(self):
        role = self.user['card_type']
        if role == "Admin":
            return ["Quản lý", "Nhân viên", "Độc giả"]
        elif role == "Quản lý":
            return ["Nhân viên", "Độc giả"]
        elif role == "Nhân viên":
            return ["Độc giả"]
        else:  # Độc giả
            return []

    def register(self):
        full_name = self.full_name_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()
        card_type = self.card_type_var.get()
        password_again = self.password_again_entry.get()

        email_temp=get_user_by_email(email)
        if email_temp:
            messagebox.showerror("Lỗi","Email đã tồn tại")
            return

        if not email.endswith("@gmail.com"):
            messagebox.showerror("Lỗi","Email phải có đuổi là @gmail.com")
            return

        if not full_name or not email or not password or not card_type:
            messagebox.showerror("Lỗi", "Vui lòng điền đầy đủ thông tin!")
            return
        if card_type not in self.get_allowed_card_types():
            messagebox.showerror("Lỗi", "Bạn không có quyền tạo loại tài khoản này!")
            return
        if password != password_again:
            messagebox.showerror("Lỗi", "Mật khẩu không khớp!")
            return

        try:
            add_user(full_name, email, password, card_type)
            messagebox.showinfo("Thành công", "Tạo tài khoản thành công!")
            if self.callback:  # Gọi callback nếu được cung cấp
                self.callback()
            self.root.destroy()
        except mysql.connector.errors.IntegrityError:
            messagebox.showerror("Lỗi", "Email đã tồn tại!")