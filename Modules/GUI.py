from DataCleaning import clean_and_save_weather_data
import os
from tkinter import *
from PIL import Image, ImageTk


import webbrowser

def openYouTubeVideo1():
    webbrowser.open("https://youtube.com/shorts/ZAdwX7ELWPY?si=Y-_O65bEmxHAGEwz")

# Tạo file đã được clean
filePath = clean_and_save_weather_data()

import DataBuild  # Import DataBuild.py để có thể gọi giao diện từ file này
import DataVisualLization  # Import DataVisualLization.py

def openDataBuild():
    DataBuild.main()  # Gọi hàm main từ DataBuild.py để mở giao diện

def openDataVisualLization():
    DataVisualLization.create_gui()  # Gọi hàm show_chart từ DataVisualLization.py

window = Tk()
window.geometry("800x600")

# Hàm hiển thị giao diện "Data View" với nút quay lại
def show_data_view():
    clear_window()
    lb1 = Label(window, text="Data View", font=('Times New Roman', 20, 'bold'))
    lb1.pack(pady=20)
    
    # Nút để quay lại giao diện chính
    btn_back = Button(window, text="Quay lại", font=('Times New Roman', 17, 'bold'), command=show_main_view)
    btn_back.pack(pady=20)

# Hàm hiển thị giao diện "Chart View" với nút quay lại
def show_chart_view():
    clear_window()
    lb1 = Label(window, text="Chart View", font=('Times New Roman', 20, 'bold'))
    lb1.pack(pady=20)
    
    # Nút để quay lại giao diện chính
    btn_back = Button(window, text="Quay lại", font=('Times New Roman', 17, 'bold'), command=show_main_view)
    btn_back.pack(pady=20)

# Hàm thoát chương trình
def exit_program():
    window.quit()

# Hàm xóa tất cả các widget trên cửa sổ
def clear_window():
    for widget in window.winfo_children():
        widget.destroy()

# Hàm hiển thị giao diện chính với các nút điều khiển
def show_main_view():
    
    # Tiêu đề
    lb1 = Label(window, text="Weather in England", font=('Times New Roman', 25, 'bold'), fg='green')
    lb1.config(bg=window.cget('bg'))
    lb1.pack(pady=10)

    # Tạo các nút đám mây màu trắng
    btn_chart_view = Button(window, text="Xem dạng biểu đồ", bg="white", fg="green", font=('Times New Roman', 17, 'bold'), command=openDataVisualLization)
    btn_chart_view.place(x=10, y=190)

    btn_open_data_build = Button(window, text="Xem dạng số liệu", bg="white", fg="green", font=('Times New Roman', 17, 'bold'), command=openDataBuild)
    btn_open_data_build.place(x=10, y=280)

    btn_exit = Button(window, text="Thoát", bg="white", fg="green", font=('Times New Roman', 17, 'bold'), command=exit_program)
    btn_exit.place(x=10, y=370)

# Đường dẫn file code đang chạy
currentDir = os.path.dirname(__file__)  

# Đường dẫn đến file ảnh nền
bg_image_path = os.path.join(currentDir, '../Data/MangHinhCho.jpg')

# Tạo hình nền từ file ảnh .ico
bg_image = Image.open(bg_image_path)
bg_image = bg_image.resize((window.winfo_screenwidth(), window.winfo_screenheight()), Image.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_image)

# Đặt ảnh làm nền
bg_label = Label(window, image=bg_photo)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# Hiển thị giao diện chính
show_main_view()

# Create a frame to hold YouTube buttons
youtube_button_frame = Frame(window)
youtube_button_frame.pack(pady=10)

# Create a button to open the YouTube video
youtube_button1 = Button(youtube_button_frame, text="Intro", command=openYouTubeVideo1)
youtube_button1.pack(side="left", padx=10)


# Chạy vòng lặp chính
window.mainloop()

# Xóa file sau khi hoàn thành công việc
if os.path.exists(filePath):
    os.remove(filePath)
