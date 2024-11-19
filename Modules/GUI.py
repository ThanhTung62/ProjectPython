from DataCleaning import clean_and_save_weather_data
import os
from tkinter import *
from PIL import Image, ImageTk
import DataBuild 
import DataVisualLization 

import webbrowser

def openYouTubeVideo1():
    """Dùng để truy cập đến một đường link"""
    webbrowser.open("https://youtu.be/bHHZEWhXJ9c?si=OMBu9f44kwcsEOww")

# Tạo file đã được clean bằng file DataCleaning
filePath = clean_and_save_weather_data()

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
    lb1 = Label(window, text="Data View", font=('Times New Roman', 20, 'bold'))
    lb1.pack(pady=20)
    
    # Nút để quay lại giao diện chính
    btnBack = Button(window, text="Quay lại", font=('Times New Roman', 17, 'bold'), command=show_main_view)
    btnBack.pack(pady=20)

def show_chart_view():
    """Hàm hiển thị giao diện Chart View"""
    clear_window()
    lb1 = Label(window, text="Chart View", font=('Times New Roman', 20, 'bold'))
    lb1.pack(pady=20)
    
    # Nút để quay lại giao diện chính
    btnBack = Button(window, text="Quay lại", font=('Times New Roman', 17, 'bold'), command=show_main_view)
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
bgImage_path = os.path.join(currentDir, '../Data/MangHinhCho.jpg')

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

# Create a button to open the YouTube video
youtube_button1 = Button(
    youtubeButton,
    text="Thời tiết hôm nay ở nước Anh",
    command=openYouTubeVideo1,
    bg="lightblue",  # Nền xanh nhạt
    fg="black",      # Chữ màu trắng
    font=("Arial", 12, "bold")  # Chữ to hơn một chút (12 và đậm)
)
youtube_button1.pack(side="left", padx=10)

# Chạy vòng lặp chính
window.mainloop()

# Xóa file sau khi hoàn thành công việc
if os.path.exists(filePath):
    os.remove(filePath)