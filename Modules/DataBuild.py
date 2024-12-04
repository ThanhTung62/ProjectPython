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

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

data = getData()
sortOrder = {col: True for col in data.columns}

def sortData(column):
    global sortOrder, data

    data = data.sort_values(by=column, ascending=sortOrder[column]).reset_index(drop=True)
    sortOrder[column] = not sortOrder[column]
    
    updateTable()

def updateTable():
    for row in tree.get_children():
        tree.delete(row)

    display_data = data.iloc[(current_page-1)*items_per_page:current_page*items_per_page]

    for index, row in display_data.iterrows():
        tree.insert("", "end", values=[index] + list(row))

def nextPage():
    global current_page, max_page
    if current_page < max_page:
        current_page += 1
        updateTable()
        page_label.config(text=f"Page {current_page} of {max_page}")

def prevPage():
    global current_page
    if current_page > 1:
        current_page -= 1
        updateTable()
        page_label.config(text=f"Page {current_page} of {max_page}")

def firstPage():
    global current_page
    current_page = 1
    updateTable()
    page_label.config(text=f"Page {current_page} of {max_page}")

def lastPage():
    global current_page, max_page
    current_page = max_page
    updateTable()
    page_label.config(text=f"Page {current_page} of {max_page}")

def searchDate():
    search_value = search_entry.get().strip()
    global data
    data = getData()  # Làm mới dữ liệu từ nguồn

    if search_value:
        # Chuyển đổi dữ liệu 'Date' thành chuỗi nếu nó chưa phải là chuỗi
        filtered_data = data[data['Date'].astype(str).str.contains(search_value, case=False, na=False)]
        if not filtered_data.empty:
            data = filtered_data  # Cập nhật lại dữ liệu với kết quả lọc
            updateTable()  # Cập nhật bảng với dữ liệu lọc
        else:
            messagebox.showinfo("Thông báo", "Không tìm thấy dữ liệu với giá trị Date đó.")
            updateTable()  # Cập nhật lại bảng dù không có kết quả tìm thấy
    else:
        updateTable()  # Nếu ô tìm kiếm rỗng, cập nhật lại bảng với dữ liệu ban đầu

def showRowInfo(event):
    selected_item = tree.selection()
    if selected_item:
        row_data = tree.item(selected_item)["values"]
        
        stt_value = row_data[0]
        date_value = row_data[1]
        pre_value = row_data[2]
        row_details = row_data[3:]

        info_text = f"Thông tin thời tiết:\n\n"
        info_text += f"STT: {stt_value}\n"
        info_text += f"Ngày: {date_value}\n"
        info_text += f"Loai thoi tiet: {pre_value}\n"
        info_text += "\n".join([f"{col}: {val}" for col, val in zip(data.columns[2:], row_details)])

        popup = Toplevel()
        popup.title("Thông tin thời tiết")
        popup.geometry("300x300")

        lbl_info = Label(popup, text=info_text, justify='left', font=('Times New Roman', 14), fg="darkblue", bg="lightyellow")
        lbl_info.pack(pady=10, padx=10)

        btn_close = Button(popup, text="Đóng", command=popup.destroy, font=('Times New Roman', 14), bg="lightcoral")
        btn_close.pack(pady=10)

def openNote():
    currentDir = os.path.dirname(__file__)
    note_file = os.path.join(currentDir, '../Data/notes.txt')

    note_window = Toplevel()
    note_window.title("Ghi chú")
    note_window.geometry("400x300")

    text_area = tk.Text(note_window, wrap="word", font=("Arial", 12))
    text_area.pack(fill="both", expand=True, padx=10, pady=10)

    if os.path.exists(note_file):
        with open(note_file, "r", encoding="utf-8") as file:
            content = file.read()
            text_area.insert("1.0", content)

    def saveNote():
        with open(note_file, "w", encoding="utf-8") as file:
            file.write(text_area.get("1.0", "end").strip())

    save_button = Button(note_window, text="Lưu", command=saveNote, font=("Arial", 12), bg="lightblue")
    save_button.pack(pady=10)

def createEntryAndUpdate():
    createEntry(window)  # Gọi hàm tạo dữ liệu mới
    global data
    data = getData()  # Làm mới dữ liệu từ nguồn
    updateTable()  # Cập nhật bảng hiển thị

def deleteEntryAndUpdate():
    deleteEntry(window)  # Gọi hàm xóa dữ liệu
    global data
    data = getData()  # Làm mới dữ liệu từ nguồn
    updateTable()  # Cập nhật bảng hiển thị

def updateEntryAndUpdate():
    updateEntry(window)  # Gọi hàm tạo dữ liệu mới
    global data
    data = getData()  # Làm mới dữ liệu từ nguồn
    updateTable()  # Cập nhật bảng hiển thị

def showAllAndUpdate():
    global data
    data = getData()  # Lấy toàn bộ dữ liệu
    updateTable()  # Cập nhật bảng hiển thị

def main():
    global window 
    window = tk.Tk()
    window.title("Weather Data Management")
    window.state('zoomed')
    window.configure(bg="#e3f2fd")

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

    global tree, current_page, items_per_page, max_page, page_label, data

    items_per_page = 20
    current_page = 1
    max_page = (len(data) // items_per_page) + 1

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

    create_button = ttk.Button(button_frame, text="Create", command=createEntryAndUpdate)
    create_button.pack(side="left", padx=10)

    update_button = ttk.Button(button_frame, text="Update", command=updateEntryAndUpdate)
    update_button.pack(side="left", padx=10)

    delete_button = ttk.Button(button_frame, text="Delete", command=deleteEntryAndUpdate)
    delete_button.pack(side="left", padx=10)

    read_button = ttk.Button(button_frame, text="Info", command=lambda: readData(window))
    read_button.pack(side="left", padx=10)
    read_button.pack(side="left", padx=10)

    exit_button = ttk.Button(button_frame, text="Exit", command=exitApp)
    exit_button.pack(side="left", padx=10)

    show_all_button = ttk.Button(search_frame, text="Show all", command=showAllAndUpdate)
    show_all_button.pack(side="left", padx=10)

    page_frame = ttk.Frame(window)
    page_frame.pack(pady=10)

    first_button = ttk.Button(page_frame, text="First", command=firstPage)
    first_button.pack(side="left", padx=10)

    prev_button = ttk.Button(page_frame, text="Previous", command=prevPage)
    prev_button.pack(side="left", padx=10)

    page_label = ttk.Label(page_frame, text=f"Page {current_page} of {max_page}", background="#e3f2fd")
    page_label.pack(side="left", padx=10)

    next_button = ttk.Button(page_frame, text="Next", command=nextPage)
    next_button.pack(side="left", padx=10)

    last_button = ttk.Button(page_frame, text="Last", command=lastPage)
    last_button.pack(side="left", padx=10)

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
