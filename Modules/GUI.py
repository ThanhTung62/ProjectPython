from DataCleaning import clean_and_save_weather_data
import os
from tkinter import *
from PIL import Image, ImageTk
import webbrowser
import time

def openYouTubeVideo1():
    """Dùng để truy cập đến một đường link"""
    webbrowser.open("https://youtu.be/bHHZEWhXJ9c?si=OMBu9f44kwcsEOww")

# Tạo file đã được clean bằng file DataCleaning
filePath = clean_and_save_weather_data()

import DataBuild 
import DataVisualLization 

def openDataBuild():
    """Gọi hàm main từ DataBuild.py để mở giao diện"""
    DataBuild.main() 

def openDataVisualLization():
    """Gọi hàm show_chart từ DataVisualLization.py"""
    DataVisualLization.create_gui()  

window = Tk()
window.geometry("800x600")

def show_data_view():
    """Hàm hiển thị giao diện Data View"""
    clear_window()
    lb1 = Label(window, text="Data View", font=('Poppins', 22, 'bold'), fg='#2c3e50', bg='#ecf0f1', padx=20, pady=10)
    lb1.pack(pady=20)
    
    # Nút để quay lại giao diện chính
    btnBack = Button(window, text="Quay lại", font=('Poppins', 18, 'bold'), command=show_main_view, bg='#3498db', fg='white', relief=SOLID, bd=2, padx=20, pady=10)
    btnBack.pack(pady=20)

def show_chart_view():
    """Hàm hiển thị giao diện Chart View"""
    clear_window()
    lb1 = Label(window, text="Chart View", font=('Poppins', 22, 'bold'), fg='#2c3e50', bg='#ecf0f1', padx=20, pady=10)
    lb1.pack(pady=20)
    
    # Nút để quay lại giao diện chính
    btnBack = Button(window, text="Quay lại", font=('Poppins', 18, 'bold'), command=show_main_view, bg='#3498db', fg='white', relief=SOLID, bd=2, padx=20, pady=10)
    btnBack.pack(pady=20)

def exit_program():
    """Hàm thoát chương trình"""
    window.quit()

def clear_window():
    """Hàm xóa tất cả các widget trên cửa sổ"""
    for widget in window.winfo_children():
        widget.destroy()

def show_main_view():
    """Hàm hiển thị giao diện chính với các nút điều khiển"""
    # Tiêu đề
    lb1 = Label(window, text="Weather in England", font=('Poppins', 25, 'bold'), fg='white', bg='green', padx=20, pady=10)
    lb1.config(bd=3, relief=SOLID)
    lb1.pack(pady=10)

    # Tạo các nút đám mây màu trắng với kiểu dáng đẹp như Figma
    btn_chart_view = Button(window, text="Xem dạng biểu đồ", bg="white", fg="green", font=('Helvetica', 16, 'bold'), command=openDataVisualLization, relief=SOLID, bd=2, padx=20, pady=10)
    btn_chart_view.place(x=10, y=190)
    btn_chart_view.bind("<Enter>", lambda e: btn_chart_view.config(bg="lightgreen", bd=4, relief=RAISED))
    btn_chart_view.bind("<Leave>", lambda e: btn_chart_view.config(bg="white", bd=2, relief=SOLID))

    btn_open_data_build = Button(window, text="Xem dạng số liệu", bg="white", fg="green", font=('Helvetica', 16, 'bold'), command=openDataBuild, relief=SOLID, bd=2, padx=20, pady=10)
    btn_open_data_build.place(x=10, y=280)
    btn_open_data_build.bind("<Enter>", lambda e: btn_open_data_build.config(bg="lightgreen", bd=4, relief=RAISED))
    btn_open_data_build.bind("<Leave>", lambda e: btn_open_data_build.config(bg="white", bd=2, relief=SOLID))

    btn_exit = Button(window, text="Thoát", bg="white", fg="green", font=('Helvetica', 16, 'bold'), command=exit_program, relief=SOLID, bd=2, padx=20, pady=10)
    btn_exit.place(x=10, y=370)
    btn_exit.bind("<Enter>", lambda e: btn_exit.config(bg="lightgreen", bd=4, relief=RAISED))
    btn_exit.bind("<Leave>", lambda e: btn_exit.config(bg="white", bd=2, relief=SOLID))

   # Create a button to open the YouTube video for weather in England
    youtube_button1 = Button(
        window,
        text="Thời tiết hôm nay ở nước Anh",
        command=openYouTubeVideo1,
        bg="white",  # Màu nền giống với nút "Thoát"
        fg="green",  # Màu chữ giống với nút "Thoát"
        font=('Helvetica', 16, 'bold'),  # Font giống với nút "Thoát"
        relief=SOLID,
        bd=2,
        padx=20,
        pady=10
    )

    # Đặt vị trí nút youtube_button1 tương tự nút btn_exit
    youtube_button1.place(x=10, y=460)  # Vị trí dưới btn_exit (y=370 + 90)

    # Thêm sự kiện khi di chuột vào và ra khỏi nút
    youtube_button1.bind("<Enter>", lambda e: youtube_button1.config(bg="lightgreen", bd=4, relief=RAISED))
    youtube_button1.bind("<Leave>", lambda e: youtube_button1.config(bg="white", bd=2, relief=SOLID))


    # Hiển thị ngày giờ hệ thống
    def update_time():
        current_time = time.strftime('%Y-%m-%d %H:%M:%S')  # Lấy thời gian hiện tại
        lb_time.config(text=current_time)  # Cập nhật nhãn với thời gian mới
        lb_time.after(1000, update_time)  # Gọi lại sau 1000ms (1 giây)

    lb_time = Label(window, font=('Poppins', 15, 'bold'), fg='white', bg='green')
    lb_time.pack(pady=10)
    update_time()

# Đường dẫn file code đang chạy
currentDir = os.path.dirname(__file__)  

# Đường dẫn đến file ảnh nền
bgImage_path = os.path.join(currentDir, '../Data/abc.png')

# Tạo hình nền từ file ảnh .ico
bgImage = Image.open(bgImage_path)
bgImage = bgImage.resize((window.winfo_screenwidth(), window.winfo_screenheight()), Image.LANCZOS)
bg_photo = ImageTk.PhotoImage(bgImage)

# Đặt ảnh làm nền
bgIabel = Label(window, image=bg_photo)
bgIabel.place(x=0, y=0, relwidth=1, relheight=1)

# Hiển thị giao diện chính
show_main_view()

# Create a frame to hold YouTube buttons
youtubeButton = Frame(window)
youtubeButton.pack(pady=10)

# Chạy vòng lặp chính
window.mainloop()

# Xóa file sau khi hoàn thành công việc
if os.path.exists(filePath):
    os.remove(filePath)
