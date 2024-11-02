import pandas as pd

pd.set_option('display.max_columns', None)  # Hiển thị tất cả các cột
pd.set_option('display.width', 1000)        # Đặt chiều rộng hiển thị

data = pd.read_csv("../Data/EnglandWeather.csv")

# def display_menu():
#     print("\nChọn thao tác bạn muốn thực hiện:")
#     print("1. Tạo (Create) - Thêm một dòng dữ liệu mới")
#     print("2. Đọc (Read) - Hiển thị dữ liệu")
#     print("3. Cập nhật (Update) - Chỉnh sửa dữ liệu")
#     print("4. Xóa (Delete) - Xóa dòng dữ liệu")
#     print("5. Thoát")

def createEntry():
    try:
        formatted_date = input("Nhập ngày (Formatted Date): ")
        summary = input("Nhập mô tả thời tiết (Summary): ")
        precip_type = input("Nhập loại mưa (Precip_Type): ")
        temperature = float(input("Nhập nhiệt độ (Temperature (C)): "))
        wind_speed = float(input("Nhập tốc độ gió (Wind Speed (km/h)): "))
        pressure = float(input("Nhập áp suất (Pressure (millibars)): "))
        humidity = float(input("Nhập độ ẩm (Humidity): "))
        # Tạo dữ liệu mới và thêm vào DataFrame
        newData = {
            "Formatted Date": formatted_date,
            "Summary": summary,
            "Precip_Type": precip_type,
            "Temperature (C)": temperature,
            "Wind Speed (km/h)": wind_speed,
            "Pressure (millibars)": pressure,
            "Humidity": humidity
        }
        global data  # Thay đổi sẽ áp dụng với biến toàn cục data
        data = pd.concat([data, pd.DataFrame([newData])], ignore_index=True)
        # ignore_index=True đảm bảo các chỉ số mới khi thêm vào 
        # liên tục với các chỉ số có sẵn
        print("Đã thêm dòng mới vào dữ liệu.")
    except ValueError as ve:
        print(f"Có lỗi xảy ra khi chuyển đổi kiểu dữ liệu: {ve}")
    except Exception as e:
        print(f"Có lỗi xảy ra: {e}")

print(data.tail(5))
createEntry()
print(data.tail(5))

def readData():
    print("Dữ liệu hiện tại:")
    print(data)
    #In ra thông tin về DataFrame
    print("\nThông tin DataFrame:")
    print(data.info())
    print("\nSố lượng giá trị thiếu trong mỗi cột:")
    print(data.isna().sum())
    print("\nSố lượng bản ghi bị trùng lặp:")
    print(data.duplicated().sum())

# createEntry()
# readData()

def updateEntry():
    # Chọn chỉ số dòng và cột để cập nhật
    try:
        index = int(input("Nhập chỉ số dòng bạn muốn cập nhật: "))
        column = input("Nhập tên cột muốn cập nhật: ")
        if column in data.columns and 0 <= index < len(data):
            new_value = input(f"Nhập giá trị mới cho {column}: ")

            if new_value:  # Kiểm tra giá trị mới không rỗng
                data.at[index, column] = new_value # Cập nhật giá trị mới tại hàng thứ.. và cột thứ..
                print(f"Đã cập nhật {column} tại dòng {index} thành {new_value}.")
            else:
                print("Giá trị mới không hợp lệ. Vui lòng nhập một giá trị không rỗng.")
        else:
            print("Tên cột không hợp lệ hoặc chỉ số dòng không hợp lệ.")
    except ValueError:
        print("Vui lòng nhập một số nguyên hợp lệ cho chỉ số dòng.")
    except Exception as e:
        print(f"Có lỗi xảy ra: {e}")


# print(data.head(5))
# updateEntry()
# print(data.head(5))

def deleteEntry():
    try:
        # Xóa dòng dựa trên chỉ số dòng
        index = int(input("Nhập chỉ số dòng bạn muốn xóa: "))
        global data  # Thay đổi trực tiếp trên biến toàn cục data
        if 0 <= index < len(data):
            data = data.drop(index).reset_index(drop=True) 
            #Xóa dòng tại index bằng drop và reset_index
            #để đặt lại chỉ số của dataFrame trong trường hợp chỉ số không liên tục sau khi xóa
            print(f"Đã xóa dòng {index} khỏi dữ liệu.")
        else:
            print("Chỉ số dòng không hợp lệ.")
    except ValueError:
        print("Vui lòng nhập một số nguyên hợp lệ cho chỉ số dòng.")
    except Exception as e:
        print(f"Có lỗi xảy ra: {e}")

# print(data.head(5))
# deleteEntry()
# print(data.head(5))