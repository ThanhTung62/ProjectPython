from DataCleaning import clean_and_save_weather_data
import os
from tkinter import *
from PIL import Image, ImageTk

# Tạo file đã được clean
filePath = clean_and_save_weather_data()

window = Tk()

def show_data_view():
    clear_window()
    lb1 = Label(window, text="Data View", font=('Times New Roman', 20, 'bold'))
    lb1.pack(pady=20)

def show_chart_view():
    clear_window()
    lb1 = Label(window, text="Chart View", font=('Times New Roman', 20, 'bold'))
    lb1.pack(pady=20)

def exit_program():
    window.quit()

def clear_window():
    for widget in window.winfo_children():
        widget.destroy()  # Xóa tất cả widget trên cửa sổ

# Thiết lập cửa sổ
window.title("Weather in England")
window.geometry("800x600")
window.iconbitmap(r"D:\project\python\Data\MangHinhCho.ico")  # Icon cho cửa sổ

# Tạo hình nền từ file ảnh .ico
bg_image = Image.open(r"D:\project\python\Data\MangHinhCho.ico")
bg_image = bg_image.resize((800, 600), Image.LANCZOS)  # Điều chỉnh kích thước ảnh
bg_photo = ImageTk.PhotoImage(bg_image)

# Đặt ảnh làm nền
bg_label = Label(window, image=bg_photo)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# Tiêu đề
lb1 = Label(window, text="Weather in England", font=('Times New Roman', 25, 'bold'), fg='green')
lb1.config(bg=window.cget('bg'))  # Sử dụng màu nền của cửa sổ
lb1.pack(pady=10)

# Tạo các nút
btn_data_view = Button(window, text="Xem dạng số liệu", bg="pink", fg="green", font=('Times New Roman', 17, 'bold'), command=show_data_view)
btn_data_view.place(x=10, y=100)  # Đặt vị trí nút

btn_chart_view = Button(window, text="Xem dạng biểu đồ", bg="pink", fg="green", font=('Times New Roman', 17, 'bold'), command=show_chart_view)
btn_chart_view.place(x=10, y=190)  # Đặt vị trí nút

btn_exit = Button(window, text="Thoát", bg="pink", fg="green", font=('Times New Roman', 17, 'bold'), command=exit_program)
btn_exit.place(x=10, y=280)  # Đặt vị trí nút

window.mainloop()

# Xóa file sau khi hoàn thành công việc
if os.path.exists(filePath):
    os.remove(filePath)
