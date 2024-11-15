import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import ttk
import pandas as pd
import os
from DataCrud import sortData, createEntry, updateEntry, deleteEntry, readData

import webbrowser

def openYouTubeVideo1():
    webbrowser.open("https://youtu.be/H43glfbQEh4?si=XEcJG55kZ8x5ySaZ")

def openYouTubeVideo2():
    webbrowser.open("https://youtu.be/sApvDcSNUkw?si=KI9KxdiEkokcnZZ9")

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

def showRowInfo(event):
    # Lấy dòng mà người dùng nhấp vào (index đầu tiên)
    selected_item = tree.selection()
    if selected_item:
        row_data = tree.item(selected_item)["values"]
        index = row_data[0]  # Lấy index của dòng được chọn
        row_details = row_data[1:]  # Lấy các giá trị khác của dòng

        # Hiển thị thông tin vắng tắt trong một cửa sổ nhỏ (popup)
        info_text = f"Index: {index}\n"
        info_text += "\n".join([f"{col}: {val}" for col, val in zip(data.columns, row_details)])
        
        messagebox.showinfo("Thông tin dòng", info_text)

#Chức năng thể hiện tóm tắt thông tin:
def showRowInfo(event):
    # Lấy dòng mà người dùng nhấp vào (index đầu tiên)
    selected_item = tree.selection()
    if selected_item:
        row_data = tree.item(selected_item)["values"]
        index = row_data[0]  # Lấy index của dòng được chọn
        row_details = row_data[1:]  # Lấy các giá trị khác của dòng

        # Hiển thị thông tin vắn tắt trong một cửa sổ nhỏ (popup)
        info_text = f"Index: {index}\n"
        info_text += "\n".join([f"{col}: {val}" for col, val in zip(data.columns, row_details)])
        
        messagebox.showinfo("Thông tin dòng", info_text)



def main():
    window = tk.Tk()
    window.title("Weather Data Management")
    window.state('zoomed')  # Mở cửa sổ toàn màn hình

    window.configure(bg="#e3f2fd")  # Bầu trời xanh nhạt

    def exitApp():
        window.withdraw()

    style = ttk.Style(window)
    style.theme_use("clam")

    style.configure("Treeview", 
                    background="#ffffff",
                    foreground="#212529",
                    rowheight=25,
                    fieldbackground="#ffffff", 
                    borderwidth=2,  
                    relief="solid")  
    
    style.configure("Treeview.Heading", 
                    background="#1e88e5",  
                    foreground="white",  
                    font=("Arial", 10, "bold"))

    style.map('Treeview', 
              background=[('selected', '#64b5f6')],
              foreground=[('selected', '#ffffff')])  

    frame = ttk.Frame(window)
    frame.pack(fill="both", expand=True, padx=20, pady=20)

    global tree
    tree = ttk.Treeview(frame, columns=["Index"] + list(data.columns), show="headings", height=15)
    tree.pack(side="left", fill="both", expand=True)

    scrollbar_y = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar_y.set)
    scrollbar_y.pack(side="right", fill="y")

    tree.heading("Index", text="Index")
    tree.column("Index", width=50, anchor='center')
    
    for col in data.columns:
        tree.heading(col, text=col, command=lambda _col=col: sortData(_col))
        tree.column(col, width=100, anchor='center')

    updateTable()

    #Chức năng thể hiện tóm tắt thông tin:
    tree.bind("<Double-1>", showRowInfo)

    search_frame = ttk.Frame(window)
    search_frame.pack(pady=10)
    
    search_label = ttk.Label(search_frame, text="Find date:", background="#e3f2fd")
    search_label.pack(side="left", padx=10)

    global search_entry
    search_entry = ttk.Entry(search_frame)
    search_entry.pack(side="left", padx=10)

    search_button = ttk.Button(search_frame, text="Find", command=searchDate)
    search_button.pack(side="left", padx=10)

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

    youtube_button_frame = ttk.Frame(window)
    youtube_button_frame.pack(pady=10)

    youtube_button1 = ttk.Button(youtube_button_frame, text="Tiếng mưa rơi ở nước Anh cực chill", command=openYouTubeVideo1)
    youtube_button1.pack(side="left", padx=10)

    youtube_button2 = ttk.Button(youtube_button_frame, text="Cảnh vật nưóc Anh dưới tuyết tuyệt đẹp", command=openYouTubeVideo2)
    youtube_button2.pack(side="left", padx=10)

    window.mainloop()

if __name__ == "__main__":
    main()
