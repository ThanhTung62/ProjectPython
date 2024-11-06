import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import ttk
import pandas as pd

# Tải dữ liệu từ file CSV
data = pd.read_csv("../Data/EnglandWeather.csv")

# Thiết lập các tùy chọn hiển thị của Pandas
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

# Các hàm cho các thao tác CRUD
def createEntry():
    try:
        # Nhập dữ liệu từ người dùng thông qua hộp thoại
        formatted_date = simpledialog.askstring("Input", "Nhập ngày (Formatted Date):")
        summary = simpledialog.askstring("Input", "Nhập mô tả thời tiết (Summary):")
        precip_type = simpledialog.askstring("Input", "Nhập loại mưa (Precip_Type):")
        temperature = float(simpledialog.askfloat("Input", "Nhập nhiệt độ (Temperature (C)):"))
        wind_speed = float(simpledialog.askfloat("Input", "Nhập tốc độ gió (Wind Speed (km/h)):"))
        pressure = float(simpledialog.askfloat("Input", "Nhập áp suất (Pressure (millibars)):"))
        humidity = float(simpledialog.askfloat("Input", "Nhập độ ẩm (Humidity):"))

        # Tạo một dictionary để lưu dữ liệu mới
        newData = {
            "Formatted Date": formatted_date,
            "Summary": summary,
            "Precip_Type": precip_type,
            "Temperature (C)": temperature,
            "Wind Speed (km/h)": wind_speed,
            "Pressure (millibars)": pressure,
            "Humidity": humidity
        }

        global data  # Sử dụng biến toàn cục data
        # Thêm dữ liệu mới vào DataFrame
        data = pd.concat([data, pd.DataFrame([newData])], ignore_index=True)
        messagebox.showinfo("Success", "Đã thêm dòng mới vào dữ liệu.")
        updateTable()  # Cập nhật bảng hiển thị
    except ValueError as ve:
        messagebox.showerror("Error", f"Có lỗi xảy ra khi chuyển đổi kiểu dữ liệu: {ve}")
    except Exception as e:
        messagebox.showerror("Error", f"Có lỗi xảy ra: {e}")

def updateTable(filtered_data=None):
    # Xóa dữ liệu hiện tại từ Treeview
    for row in tree.get_children():
        tree.delete(row)

    # Sử dụng dữ liệu đã lọc nếu có, nếu không sử dụng dữ liệu gốc
    display_data = filtered_data if filtered_data is not None else data

    # Chèn dữ liệu đã cập nhật từ DataFrame vào Treeview
    for index, row in display_data.iterrows():
        tree.insert("", "end", values=[index] + list(row))

def readData():
    # Hiển thị dữ liệu hiện tại trong cửa sổ console
    print("Dữ liệu hiện tại:")
    print(data)
    # Lấy thông tin về DataFrame
    info_str = f"\nThông tin DataFrame:\n{data.info(buf=None)}"
    missing_values = f"\nSố lượng giá trị thiếu trong mỗi cột:\n{data.isna().sum()}"
    duplicated = f"\nSố lượng bản ghi bị trùng lặp: {data.duplicated().sum()}"
    # Tạo thông tin hiển thị
    data_info = (
        f"Dữ liệu hiện tại:\n{data.head().to_string()}\n"  # Hiển thị 5 hàng đầu tiên
        + info_str
        + missing_values
        + duplicated
    )
    # Hiển thị thông tin trong hộp thoại messagebox
    messagebox.showinfo("Thông Tin Dữ Liệu", data_info)

def updateEntry():
    try:
        # Nhập chỉ số dòng và tên cột cần cập nhật
        index = int(simpledialog.askinteger("Input", "Nhập chỉ số dòng bạn muốn cập nhật:"))
        column = simpledialog.askstring("Input", "Nhập tên cột muốn cập nhật:")
        if column in data.columns and 0 <= index < len(data):
            new_value = simpledialog.askstring("Input", f"Nhập giá trị mới cho {column}:")
            if new_value:
                data.at[index, column] = new_value  # Cập nhật giá trị mới
                messagebox.showinfo("Success", f"Đã cập nhật {column} tại dòng {index} thành {new_value}.")
                updateTable()
            else:
                messagebox.showwarning("Invalid Input", "Giá trị mới không hợp lệ. Vui lòng nhập một giá trị không rỗng.")
        else:
            messagebox.showwarning("Invalid Input", "Tên cột không hợp lệ hoặc chỉ số dòng không hợp lệ.")
    except ValueError:
        messagebox.showerror("Error", "Vui lòng nhập một số nguyên hợp lệ cho chỉ số dòng.")
    except Exception as e:
        messagebox.showerror("Error", f"Có lỗi xảy ra: {e}")

def deleteEntry():
    try:
        # Nhập chỉ số dòng cần xóa
        index = int(simpledialog.askinteger("Input", "Nhập chỉ số dòng bạn muốn xóa:"))
        global data
        if 0 <= index < len(data):
            data = data.drop(index).reset_index(drop=True)  # Xóa dòng và đặt lại chỉ số
            messagebox.showinfo("Success", f"Đã xóa dòng {index} khỏi dữ liệu.")
            updateTable()
        else:
            messagebox.showwarning("Invalid Input", "Chỉ số dòng không hợp lệ.")
    except ValueError:
        messagebox.showerror("Error", "Vui lòng nhập một số nguyên hợp lệ cho chỉ số dòng.")
    except Exception as e:
        messagebox.showerror("Error", f"Có lỗi xảy ra: {e}")

def searchIndex():
    search_value = search_entry.get()

    # Kiểm tra nếu ô tìm kiếm có giá trị và tìm kiếm trong Index
    if search_value:
        try:
            search_value = int(search_value)  # Chuyển đổi sang số nguyên
            # Kiểm tra xem chỉ số có trong dữ liệu không
            filtered_data = data[data.index == search_value]
            if not filtered_data.empty:
                updateTable(filtered_data)  # Cập nhật bảng với kết quả tìm kiếm
            else:
                messagebox.showinfo("Thông báo", "Không tìm thấy chỉ số.")
                updateTable()  # Nếu không tìm thấy, hiển thị lại toàn bộ dữ liệu
        except ValueError:
            messagebox.showerror("Lỗi", "Giá trị tìm kiếm không hợp lệ. Hãy nhập một chỉ số hợp lệ.")
            updateTable()  # Nếu không thể chuyển đổi giá trị tìm kiếm, hiển thị lại toàn bộ dữ liệu
    else:
        updateTable()  # Nếu không có tìm kiếm, hiển thị lại toàn bộ dữ liệu

def main():
    window = tk.Tk()
    window.title("Weather Data Management")
    window.state('zoomed')  # Mở cửa sổ toàn màn hình
    window.configure(bg="#f8f9fa")  # Màu nền tổng thể sáng nhẹ

    # Tạo style cho Treeview
    style = ttk.Style(window)
    style.theme_use("clam")
    
    style.configure("Treeview", 
                    background="#f0f0f0",  # Nền bảng xám nhẹ
                    foreground="#212529",  # Màu chữ đen xám
                    rowheight=25,
                    fieldbackground="#f0f0f0",  # Nền xám nhẹ cho các ô
                    borderwidth=2,  # Thêm viền cho bảng
                    relief="solid")  # Viền rắn cho bảng
    
    style.configure("Treeview.Heading", 
                    background="#6c757d",  # Màu nền xám cho tiêu đề cột
                    foreground="white",  # Màu chữ trắng cho tiêu đề cột
                    font=("Arial", 10, "bold"))  # Font chữ cho tiêu đề cột

    style.map('Treeview', 
              background=[('selected', '#74c0fc')],  # Màu xanh nhạt cho dòng được chọn
              foreground=[('selected', '#ffffff')])  # Màu chữ trắng khi dòng được chọn

    # Tạo một widget Treeview để hiển thị dữ liệu
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
    tree.column("Index", width=50, anchor='center')  # Điều chỉnh chiều rộng cột
    for col in data.columns:
        tree.heading(col, text=col)
        tree.column(col, width=100, anchor='center')

    # Tải dữ liệu ban đầu vào bảng
    updateTable()

    # Tạo ô tìm kiếm và nút tìm kiếm
    search_frame = ttk.Frame(window)
    search_frame.pack(pady=10)
    
    search_label = ttk.Label(search_frame, text="Find index:")
    search_label.pack(side="left", padx=10)

    global search_entry
    search_entry = ttk.Entry(search_frame)
    search_entry.pack(side="left", padx=10)

    search_button = ttk.Button(search_frame, text="Find", command=searchIndex)
    search_button.pack(side="left", padx=10)

    # Tạo các nút cho từng thao tác
    button_frame = ttk.Frame(window)
    button_frame.pack(pady=10)

    create_button = ttk.Button(button_frame, text="Create", command=createEntry)
    create_button.pack(side="left", padx=10)

    update_button = ttk.Button(button_frame, text="Update", command=updateEntry)
    update_button.pack(side="left", padx=10)

    delete_button = ttk.Button(button_frame, text="Delete", command=deleteEntry)
    delete_button.pack(side="left", padx=10)

    read_button = ttk.Button(button_frame, text="Info", command=readData)
    read_button.pack(side="left", padx=10)

    exit_button = ttk.Button(button_frame, text="Exit", command=window.quit)
    exit_button.pack(side="left", padx=10)

    show_all_button = ttk.Button(search_frame, text="Show all", command=lambda: updateTable())
    show_all_button.pack(side="left", padx=10)

    window.mainloop()  # Bắt đầu vòng lặp chính của GUI

if __name__ == "__main__":
    main()  # Gọi hàm main để chạy ứng dụng