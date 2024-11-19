import tkinter as tk
from tkinter import messagebox, simpledialog, Toplevel, Label, Button, ttk
import pandas as pd
import os
from DataCrud import createEntry, updateEntry, deleteEntry, readData, getData
import webbrowser

def openYouTubeVideo1():
    """Dùng để truy cập đến một đường link"""
    webbrowser.open("https://youtu.be/H43glfbQEh4?si=XEcJG55kZ8x5ySaZ")

def openYouTubeVideo2():
    """Dùng để truy cập đến một đường link"""
    webbrowser.open("https://youtu.be/sApvDcSNUkw?si=KI9KxdiEkokcnZZ9")

# Thiết lập các tùy chọn hiển thị của Pandas
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

data = getData()
sortOrder = {col: True for col in data.columns}  # Mặc định là tăng dần (True)

def sortData(column):
    """Click lần đầu là sort tăng dần, click cái nữa là giảm dần"""
    #Biến toàn cục
    global sortOrder,data

    # Sắp xếp dữ liệu theo cột và thứ tự sắp xếp hiện tại
    data = data.sort_values(by=column, ascending=sortOrder[column]).reset_index(drop=True)

    # Đổi thứ tự sắp xếp cho lần nhấp tiếp theo
    sortOrder[column] = not sortOrder[column]
    
    # Cập nhật bảng sau khi sắp xếp
    updateTable(data)

def updateTable(filtered_data=None):
    data = getData()
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
    data = getData()
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
    """Gọi ra 1 cửa sổ hiện vắn tắt thông tin"""
    selected_item = tree.selection()
    if selected_item:
        #lấy danh sách các giá trị từ các cột của hàng được chọn
        row_data = tree.item(selected_item)["values"]
        
        # Tạo số thứ tự (STT) từ chỉ số của item trong treeview
        stt_value = row_data[0]  # Lấy giá trị của cột "Ngày" làm giá trị cho cột STT
        
        # Lấy giá trị cột "Ngày" (là cột thứ hai trong row_data sau cột STT)
        date_value = row_data[1]  # Lấy cột "Ngày" từ dòng đã chọn
        
        # Các giá trị còn lại từ dòng đã chọn (bỏ cột "Ngày")
        row_details = row_data[2:]  # Bỏ cột "Ngày" ra khỏi dữ liệu

        # Tạo chuỗi thông tin để hiển thị
        info_text = f"Thông tin thời tiết:\n\n"
        info_text += f"STT: {stt_value}\n"  # Hiển thị số thứ tự lấy từ cột "Ngày"
        info_text += f"Ngày: {date_value}\n"  # Hiển thị ngày từ cột "Ngày"
        
        # Hiển thị các giá trị của các cột còn lại
        info_text += "\n".join([f"{col}: {val}" for col, val in zip(data.columns[2:], row_details)])

        # Tạo cửa sổ popup để hiển thị thông tin
        popup = Toplevel()
        popup.title("Thông tin thời tiết")
        popup.geometry("400x250")

        lbl_info = Label(popup, text=info_text, justify='left', font=('Times New Roman', 14), fg="darkblue", bg="lightyellow")
        lbl_info.pack(pady=10, padx=10)

        btn_close = Button(popup, text="Đóng", command=popup.destroy, font=('Times New Roman', 14), bg="lightcoral")
        btn_close.pack(pady=10)

def openNote():
    # Đường dẫn tới file notes.txt
    # Đường dẫn file code đang chạy
    currentDir = os.path.dirname(__file__)  

    # Đường dẫn đến file ảnh nền
    note_file = os.path.join(currentDir, '../Data/notes.txt')

    # Tạo cửa sổ note
    note_window = Toplevel()
    note_window.title("Ghi chú")
    note_window.geometry("400x300")

    # Tạo Text widget để hiển thị và chỉnh sửa nội dung
    text_area = tk.Text(note_window, wrap="word", font=("Arial", 12))
    text_area.pack(fill="both", expand=True, padx=10, pady=10)

    # Nếu file tồn tại, đọc nội dung vào Text widget
    if os.path.exists(note_file):
        with open(note_file, "r", encoding="utf-8") as file:
            content = file.read()
            text_area.insert("1.0", content)

    # Hàm lưu ghi chú
    def saveNote():
        with open(note_file, "w", encoding="utf-8") as file:
            file.write(text_area.get("1.0", "end").strip())

    # Nút lưu ghi chú
    save_button = Button(note_window, text="Lưu", command=saveNote, font=("Arial", 12), bg="lightblue")
    save_button.pack(pady=10)


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

    global tree,data
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

    create_button = ttk.Button(button_frame, text="Create", command=lambda: (updateTable(createEntry())))
    create_button.pack(side="left", padx=10)

    update_button = ttk.Button(button_frame, text="Update", command=lambda: (updateTable(updateEntry())))
    update_button.pack(side="left", padx=10)

    delete_button = ttk.Button(button_frame, text="Delete", command=lambda: (updateTable(deleteEntry())))
    delete_button.pack(side="left", padx=10)

    read_button = ttk.Button(button_frame, text="Info", command=lambda: readData())
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

    note_button = ttk.Button(button_frame, text="Note", command=openNote)
    note_button.pack(side="left", padx=10)

    window.mainloop()

if __name__ == "__main__":
    main()
