import pandas as pd
from tkinter import messagebox, simpledialog
import os
# Đảm bảo biến data được truyền vào khi cần thiết

# Đường dẫn file code đang chạy
currentDir = os.path.dirname(__file__)  

# Đường dẫn đến file CSV ban đầu và file CSV mới
dataPath = os.path.join(currentDir, '../Data/EnglandWeather.csv')
newDataPath = os.path.join(currentDir, '../Data/EnglandWeather2.csv')

# Tải dữ liệu từ file CSV
data = pd.read_csv(newDataPath)

def getData():
    return data

def createEntry():
    global data
    try:
        # Nhập dữ liệu từ người dùng thông qua hộp thoại
        formatted_date = simpledialog.askstring("Input", "Nhập ngày (Formatted Date):")
        summary = simpledialog.askstring("Input", "Nhập mô tả thời tiết (Summary):")
        precip_type = simpledialog.askstring("Input", "Nhập loại mưa (Precip_Type):")
        temperature = float(simpledialog.askfloat("Input", "Nhập nhiệt độ (Temperature (C)):"))
        wind_speed = float(simpledialog.askfloat("Input", "Nhập tốc độ gió (Wind Speed (km/h)):"))
        pressure = float(simpledialog.askfloat("Input", "Nhập áp suất (Pressure (millibars)):"))
        humidity = float(simpledialog.askfloat("Input", "Nhập độ ẩm (Humidity):"))
        date = simpledialog.askstring("Input", "Nhập ngày (Date):")

        # Tạo một dictionary để lưu dữ liệu mới
        newData = {
            "Formatted Date": formatted_date,
            "Summary": summary,
            "Precip_Type": precip_type,
            "Temperature (C)": temperature,
            "Wind Speed (km/h)": wind_speed,
            "Pressure (millibars)": pressure,
            "Humidity": humidity,
            "Date": date
        }

        # Thêm dữ liệu mới vào DataFrame
        data = pd.concat([data, pd.DataFrame([newData])], ignore_index=True)
        messagebox.showinfo("Success", "Đã thêm dòng mới vào dữ liệu.")
        return data
    except ValueError as ve:
        messagebox.showerror("Error", f"Có lỗi xảy ra khi chuyển đổi kiểu dữ liệu: {ve}")
    except Exception as e:
        messagebox.showerror("Error", f"Có lỗi xảy ra: {e}")
        return data

def updateEntry():
    global data
    try:
        # Nhập chỉ số dòng và tên cột cần cập nhật
        index = int(simpledialog.askinteger("Input", "Nhập chỉ số dòng bạn muốn cập nhật:"))
        column = simpledialog.askstring("Input", "Nhập tên cột muốn cập nhật:").lower()  # Chuyển tên cột nhập vào thành chữ thường
        # Tạo danh sách các cột ở dạng chữ thường để so sánh
        columns_lower = [col.lower() for col in data.columns]
        if column in columns_lower and 0 <= index < len(data):
            # Lấy tên cột ban đầu từ danh sách columns
            original_column = data.columns[columns_lower.index(column)]
            new_value = simpledialog.askstring("Input", f"Nhập giá trị mới cho {original_column}:")
            if new_value:
                data.at[index, original_column] = new_value  # Cập nhật giá trị mới
                messagebox.showinfo("Success", f"Đã cập nhật {original_column} tại dòng {index} thành {new_value}.")
            else:
                messagebox.showwarning("Invalid Input", "Giá trị mới không hợp lệ. Vui lòng nhập một giá trị không rỗng.")
        else:
            messagebox.showwarning("Invalid Input", "Tên cột không hợp lệ hoặc chỉ số dòng không hợp lệ.")
    except ValueError:
        messagebox.showerror("Error", "Vui lòng nhập một số nguyên hợp lệ cho chỉ số dòng.")
    except Exception as e:
        messagebox.showerror("Error", f"Có lỗi xảy ra: {e}")
    return data

def deleteEntry():
    global data
    try:
        # Nhập chỉ số dòng cần xóa
        index = int(simpledialog.askinteger("Input", "Nhập chỉ số dòng bạn muốn xóa:"))
        if 0 <= index < len(data):
            # Xóa dòng và cập nhật lại chỉ số
            data = data.drop(index).reset_index(drop=True)
            messagebox.showinfo("Success", f"Đã xóa dòng {index} khỏi dữ liệu.")
        else:
            messagebox.showwarning("Invalid Input", "Chỉ số dòng không hợp lệ.")
    except ValueError:
        messagebox.showerror("Error", "Vui lòng nhập một số nguyên hợp lệ cho chỉ số dòng.")
    except Exception as e:
        messagebox.showerror("Error", f"Có lỗi xảy ra: {e}")
    return data

def readData():
    global data
    # Hiển thị thông tin về DataFrame
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
