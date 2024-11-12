import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import ttk
import pandas as pd
import os
from DataCrud import sortData, createEntry, updateEntry, deleteEntry, readData

import webbrowser

def openYouTubeVideo1():
    webbrowser.open("https://youtube.com/shorts/-dtPT6CJREI?si=RBEJtUaq4tkRHzl2")

def openYouTubeVideo2():
    webbrowser.open("https://youtube.com/shorts/AnDWq-jA54M?si=69Fq35E5sSbijnJ2")

# Đường dẫn file code đang chạy
currentDir = os.path.dirname(__file__)  

# Đường dẫn đến file CSV ban đầu và file CSV mới
dataPath = os.path.join(currentDir, '../Data/EnglandWeather.csv')
newDataPath = os.path.join(currentDir, '../Data/EnglandWeather2.csv')

# Tải dữ liệu từ file CSV
data = pd.read_csv(newDataPath)

# Thiết lập các tùy chọn hiển thị của Pandas
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

sort_order = {col: True for col in data.columns}  # Mặc định là tăng dần (True)

def sortData(column):
    global data, sort_order
    # Sắp xếp dữ liệu theo cột và thứ tự sắp xếp
    data = data.sort_values(by=column, ascending=sort_order[column]).reset_index(drop=True)
    sort_order[column] = not sort_order[column]  # Đổi thứ tự sắp xếp cho lần nhấp tiếp theo
    updateTable()  # Cập nhật bảng hiển thị sau khi sắp xếp

def updateTable(filtered_data=None):
    # Xóa dữ liệu hiện tại từ Treeview
    for row in tree.get_children():
        tree.delete(row)

    # Sử dụng dữ liệu đã lọc nếu có, nếu không sử dụng dữ liệu gốc
    display_data = filtered_data if filtered_data is not None else data

    # Chèn dữ liệu đã cập nhật từ DataFrame vào Treeview
    for index, row in display_data.iterrows():
        tree.insert("", "end", values=[index] + list(row))

def searchDate():
    search_value = search_entry.get().strip()
    # Kiểm tra nếu ô tìm kiếm có giá trị
    if search_value:
        # Lọc dữ liệu theo giá trị trong cột "Date"
        filtered_data = data[data['Date'].astype(str).str.contains(search_value, case=False, na=False)]
        if not filtered_data.empty:
            updateTable(filtered_data)  # Cập nhật bảng với kết quả tìm kiếm
        else:
            messagebox.showinfo("Thông báo", "Không tìm thấy dữ liệu với giá trị Date đó.")
            updateTable()  # Nếu không tìm thấy, hiển thị lại toàn bộ dữ liệu
    else:
        updateTable()  # Nếu không có tìm kiếm, hiển thị lại toàn bộ dữ liệu

def main():
    window = tk.Tk()
    window.title("Weather Data Management")
    window.state('zoomed')  # Mở cửa sổ toàn màn hình
    
    # Thiết lập màu nền tổng thể và hình ảnh thời tiết
    window.configure(bg="#e3f2fd")  # Bầu trời xanh nhạt

    def exitApp():
        # Ẩn cửa sổ chính
        window.withdraw()

    # Tạo style cho Treeview
    style = ttk.Style(window)
    style.theme_use("clam")
    
    # Cập nhật màu sắc cho Treeview theo chủ đề thời tiết
    style.configure("Treeview", 
                    background="#ffffff",  # Nền bảng trắng
                    foreground="#212529",  # Màu chữ đen xám
                    rowheight=25,
                    fieldbackground="#ffffff",  # Nền trắng cho các ô
                    borderwidth=2,  
                    relief="solid")  
    
    # Tiêu đề với màu xanh trời cho phù hợp chủ đề thời tiết
    style.configure("Treeview.Heading", 
                    background="#1e88e5",  # Màu nền xanh dương
                    foreground="white",  
                    font=("Arial", 10, "bold"))  

    style.map('Treeview', 
              background=[('selected', '#64b5f6')],  # Màu xanh nhẹ khi chọn dòng
              foreground=[('selected', '#ffffff')])  

    # Tạo widget Treeview để hiển thị dữ liệu
    frame = ttk.Frame(window)
    frame.pack(fill="both", expand=True, padx=20, pady=20)

    global tree
    tree = ttk.Treeview(frame, columns=["Index"] + list(data.columns), show="headings", height=15)
    tree.pack(side="left", fill="both", expand=True)

    # Thêm thanh cuộn cho Treeview
    scrollbar_y = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar_y.set)
    scrollbar_y.pack(side="right", fill="y")

    # Thiết lập tiêu đề cột
    tree.heading("Index", text="Index")
    tree.column("Index", width=50, anchor='center')
    # for col in data.columns:
    #     tree.heading(col, text=col)
    #     tree.column(col, width=100, anchor='center')
    for col in data.columns:
        tree.heading(col, text=col, command=lambda _col=col: sortData(_col))  # Gán sự kiện nhấp vào cột
        tree.column(col, width=100, anchor='center')


    # Tải dữ liệu ban đầu vào bảng
    updateTable()

    # Tạo ô tìm kiếm và nút tìm kiếm
    search_frame = ttk.Frame(window)
    search_frame.pack(pady=10)
    
    search_label = ttk.Label(search_frame, text="Find date:", background="#e3f2fd")
    search_label.pack(side="left", padx=10)

    global search_entry
    search_entry = ttk.Entry(search_frame)
    search_entry.pack(side="left", padx=10)

    search_button = ttk.Button(search_frame, text="Find", command=searchDate)
    search_button.pack(side="left", padx=10)

    # Tạo các nút cho từng thao tác
    button_frame = ttk.Frame(window)
    button_frame.pack(pady=10)

    create_button = ttk.Button(button_frame, text="Create", command=lambda: (updateTable(createEntry(data))))
    create_button.pack(side="left", padx=10)

    update_button = ttk.Button(button_frame, text="Update", command=lambda: (updateEntry(data), updateTable(data)))
    update_button.pack(side="left", padx=10)

    delete_button = ttk.Button(button_frame, text="Delete", command=lambda: (updateTable(deleteEntry(data))))
    delete_button.pack(side="left", padx=10)

    read_button = ttk.Button(button_frame, text="Info", command=lambda: readData(data))
    read_button.pack(side="left", padx=10)

    exit_button = ttk.Button(button_frame, text="Exit", command=exitApp)
    exit_button.pack(side="left", padx=10)

    show_all_button = ttk.Button(search_frame, text="Show all", command=lambda: updateTable())
    show_all_button.pack(side="left", padx=10)

    # Trong hàm main, thêm các nút vào giao diện:
    youtube_button_frame = ttk.Frame(window)
    youtube_button_frame.pack(pady=10)

    # Tạo nút mở video YouTube 1
    youtube_button1 = ttk.Button(youtube_button_frame, text="Rain", command=openYouTubeVideo1)
    youtube_button1.pack(side="left", padx=10)

    # Tạo nút mở video YouTube 2
    youtube_button2 = ttk.Button(youtube_button_frame, text="Snow", command=openYouTubeVideo2)
    youtube_button2.pack(side="left", padx=10)

    window.mainloop()  # Bắt đầu vòng lặp chính của GUI

    

if __name__ == "__main__":
    main()  # Gọi hàm main để chạy ứng dụng