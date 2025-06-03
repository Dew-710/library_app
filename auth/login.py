import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk  # Sử dụng để tải và hiển thị ảnh
from database.models import get_user_by_email
from roles.admin import AdminWindow
from roles.manager import ManagerWindow
from roles.staff import StaffWindow
from roles.reader import ReaderWindow

class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Đăng nhập - Thư viện")
        self.root.resizable(False, False)
        self.root.geometry("580x310")
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)

        left_frame = tk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, padx=20, pady=20, fill=tk.Y)
        tk.Label(left_frame, text="Email", font=("Arial",20)).pack(pady=5)
        self.email_entry = tk.Entry(left_frame)
        self.email_entry.pack(pady=5)
        tk.Label(left_frame, text="Mật khẩu", font=("Arial", 20)).pack(pady=5)
        self.password_entry = tk.Entry(left_frame, show="*")
        self.password_entry.pack(pady=5)
        tk.Button(left_frame, text="Đăng nhập", command=self.login).pack(pady=10)

        right_frame = tk.Frame(main_frame)
        right_frame.pack(side=tk.RIGHT, padx=0, pady=0, fill=tk.BOTH, expand=True)
        try:
            image = Image.open("logo.png")
            image = image.resize((410, 310), Image.Resampling.LANCZOS)
            self.photo = ImageTk.PhotoImage(image)
            image_label = tk.Label(right_frame, image=self.photo)
            image_label.pack(anchor="center")
        except Exception as e:
            placeholder_label = tk.Label(right_frame, text="Không thể tải ảnh", fg="red")
            placeholder_label.pack(anchor="center")
            print(f"Lỗi tải ảnh: {e}")

    def login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()
        user = get_user_by_email(email)
        if user and password == user['password']:
            self.root.destroy()
            new_root = tk.Tk()
            role = user['card_type']
            if role == 'Admin':
                AdminWindow(new_root, user)
            elif role == 'Quản lý':
                ManagerWindow(new_root, user)
            elif role == 'Nhân viên':
                StaffWindow(new_root, user)
            else:
                ReaderWindow(new_root, user)
            new_root.mainloop()
        else:
            messagebox.showerror("Lỗi", "Email hoặc mật khẩu không đúng!")