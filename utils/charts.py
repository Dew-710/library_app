import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.ticker import MultipleLocator
from database.models import get_borrowed_books_today
import tkinter as tk

def create_borrow_chart(parent):
    borrowed_books = get_borrowed_books_today()
    book_titles = [book['title'] for book in borrowed_books]
    borrow_counts = [round(book['count']) for book in borrowed_books]  # Làm tròn thành số nguyên

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(book_titles, borrow_counts)
    ax.set_title("Thống kê mượn sách trong ngày")
    ax.set_xlabel("Tên sách")
    ax.set_ylabel("Số lượng mượn")
    plt.xticks(rotation=45, ha="right")

    # Đặt giới hạn trục Y bắt đầu từ 0
    ax.set_ylim(bottom=0)

    # Đảm bảo trục Y chỉ hiển thị số nguyên, bước nhảy là 1 (0, 1, 2, 3,...)
    ax.yaxis.set_major_locator(MultipleLocator(1))

    canvas = FigureCanvasTkAgg(fig, master=parent)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)