import tkinter as tk

class Sidebar:
    def __init__(self, root, app, user):
        self.root = root
        self.app = app
        self.user = user

        tk.Label(self.root, text=f"Xin chào, {self.user['full_name']}", bg="#6B7280", fg="white", font=("Arial", 12)).pack(pady=10)

        menus = ["Trang chủ"]
        if self.user['card_type'] in ["Admin", "Quản lý", "Nhân viên", "Độc giả"]:
            menus.append("Sách")
            menus.append("Mượn - Trả")
        if self.user['card_type'] in ["Admin", "Quản lý", "Nhân viên"]:
            menus.append("Tài khoản")
            menus.append("Thống kê")

        for menu in menus:
            tk.Button(self.root, text=menu, bg="black", fg="white",width=20,height=5, command=lambda m=menu: self.on_menu_click(m)).pack(pady=5)

        tk.Button(self.root, text="Đăng xuất", bg="red", fg="white",width=20,height=5, command=self.app.logout).pack(pady=5, side=tk.BOTTOM)

    def on_menu_click(self, menu):
        if menu == "Đăng xuất":
            self.app.logout()
        else:
            self.app.show_page(menu)