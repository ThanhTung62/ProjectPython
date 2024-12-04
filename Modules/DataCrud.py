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

def createEntry(window):
    global data
    try:
        # Nhập dữ liệu từ người dùng thông qua hộp thoại
        formatted_date = simpledialog.askstring("Input", "Nhập ngày (Formatted Date):", parent=window)
        summary = simpledialog.askstring("Input", "Nhập mô tả thời tiết (Summary):", parent=window)
        precip_type = simpledialog.askstring("Input", "Nhập Precip_Type:", parent=window)
        temperature = simpledialog.askfloat("Input", "Nhập nhiệt độ (Temperature (C)):", parent=window)
        wind_speed = simpledialog.askfloat("Input", "Nhập tốc độ gió (Wind Speed (km/h)):", parent=window)
        pressure = simpledialog.askfloat("Input", "Nhập áp suất (Pressure (millibars)):", parent=window)
        humidity = simpledialog.askfloat("Input", "Nhập độ ẩm (Humidity):", parent=window)
        date = simpledialog.askstring("Input", "Nhập ngày (Date):", parent=window)

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

def updateEntry(window):
    global data
    try:
        # Nhập chỉ số dòng và tên cột cần cập nhật
        index = int(simpledialog.askinteger("Input", "Nhập chỉ số dòng bạn muốn cập nhật:", parent=window))
        column = simpledialog.askstring("Input", "Nhập tên cột muốn cập nhật:", parent=window).lower()  # Chuyển tên cột nhập vào thành chữ thường
        # Tạo danh sách các cột ở dạng chữ thường để so sánh
        columns_lower = [col.lower() for col in data.columns]
        
        if column in columns_lower and 0 <= index < len(data):
            # Lấy tên cột ban đầu từ danh sách columns
            original_column = data.columns[columns_lower.index(column)]
            
            # Lấy kiểu dữ liệu của cột
            column_type = data[original_column].dtype
            
            # Yêu cầu người dùng nhập giá trị mới
            new_value = simpledialog.askstring("Input", f"Nhập giá trị mới cho {original_column}:", parent=window)
            
            if new_value:
                # Kiểm tra và chuyển đổi kiểu dữ liệu của giá trị mới nếu cần
                if column_type == 'int64':  # Kiểu dữ liệu int
                    try:
                        new_value = int(new_value)  # Chuyển giá trị mới thành kiểu int
                    except ValueError:
                        messagebox.showwarning("Invalid Input", f"Giá trị mới phải là kiểu số nguyên cho cột {original_column}.", parent=window)
                        return
                elif column_type == 'float64':  # Kiểu dữ liệu float
                    try:
                        new_value = float(new_value)  # Chuyển giá trị mới thành kiểu float
                    except ValueError:
                        messagebox.showwarning("Invalid Input", f"Giá trị mới phải là kiểu số thực cho cột {original_column}.", parent=window)
                        return
                # Nếu kiểu dữ liệu là string hoặc các kiểu khác, không cần chuyển đổi
                
                # Cập nhật giá trị mới vào DataFrame
                data.at[index, original_column] = new_value
                messagebox.showinfo("Success", f"Đã cập nhật {original_column} tại dòng {index} thành {new_value}.", parent=window)
            else:
                messagebox.showwarning("Invalid Input", "Giá trị mới không hợp lệ. Vui lòng nhập một giá trị không rỗng.", parent=window)
        else:
            messagebox.showwarning("Invalid Input", "Tên cột không hợp lệ hoặc chỉ số dòng không hợp lệ.", parent=window)
    except ValueError:
        messagebox.showerror("Error", "Vui lòng nhập một số nguyên hợp lệ cho chỉ số dòng.", parent=window)
    except Exception as e:
        messagebox.showerror("Error", f"Có lỗi xảy ra: {e}", parent=window)

    return data


def deleteEntry(window):
    global data
    try:
        # Nhập chỉ số dòng cần xóa
        index = int(simpledialog.askinteger("Input", "Nhập chỉ số dòng bạn muốn xóa:", parent=window))
        if 0 <= index < len(data):
            # Xóa dòng và cập nhật lại chỉ số
            data = data.drop(index).reset_index(drop=True)
            messagebox.showinfo("Success", f"Đã xóa dòng {index} khỏi dữ liệu.", parent=window)
        else:
            messagebox.showwarning("Invalid Input", "Chỉ số dòng không hợp lệ.", parent=window)
    except ValueError:
        messagebox.showerror("Error", "Vui lòng nhập một số nguyên hợp lệ cho chỉ số dòng.", parent=window)
    except Exception as e:
        messagebox.showerror("Error", f"Có lỗi xảy ra: {e}", parent=window)
    
    return data


def readData(window):
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
    messagebox.showinfo("Thông Tin Dữ Liệu", data_info, parent=window)

