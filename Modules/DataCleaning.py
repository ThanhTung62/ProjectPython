import pandas as pd
import os

def clean_and_save_weather_data():
    # Đường dẫn file code đang chạy
    currentDir = os.path.dirname(__file__)  
    
    # Đường dẫn đến file CSV ban đầu và file CSV mới
    dataPath = os.path.join(currentDir, '../Data/EnglandWeather.csv')
    newDataPath = os.path.join(currentDir, '../Data/EnglandWeather2.csv')

    # Đọc dữ liệu từ file CSV
    df = pd.read_csv(dataPath)

    # Kiểm tra và xử lý cột 'Formatted Date' nếu tồn tại
    if 'Formatted Date' in df.columns:
        df['Formatted Date'] = pd.to_datetime(df['Formatted Date'], errors='coerce', utc=True)
        df['Date'] = pd.to_datetime(df['Formatted Date'].dt.date)  # Chuyển cột Date sang datetime
        df['Time'] = pd.to_datetime(df['Formatted Date'].dt.strftime('%H:%M:%S'), format='%H:%M:%S').dt.time
        df.drop(['Time'], axis=1, inplace=True)  # Xóa cột 'Time' sau khi xử lý

    # Xóa các dòng có giá trị bị thiếu
    df = df.dropna()

    # Lưu dữ liệu đã clean vào file EnglandWeather2.csv
    df.to_csv(newDataPath, index=False)

    # Trả về đường dẫn của file mới
    return newDataPath


# import pandas as pd
# import os
# from datetime import datetime


# currentDir = os.path.dirname(__file__)  # Đường dẫn file code đang chạy
# dataPath = os.path.join(currentDir, '../Data/EnglandWeather.csv')  # Đường dẫn đến file CSV


# df = pd.read_csv(dataPath)


# print("\n======================================")
# print("Xem so luot file csv: ")
# print(df.info())
# print("======================================\n")


# print("\n======================================")
# print("5 dong dau tien: ")
# print(df.head())
# print("======================================\n")


# if 'Formatted Date' in df.columns:
#     try:
#         # Chuyen cot 'Formatted Date' thanh kieu datetime voi utc=True
#         df['Formatted Date'] = pd.to_datetime(df['Formatted Date'], errors='coerce', utc=True)

#         # Kiem tra xem co gia tri NaT (Not a Time) nao khong
#         if df['Formatted Date'].isnull().any():
#             print("Co gia tri khong hop le trong cot 'Formatted Date'. Cac gia tri nay se duoc chuyen thanh NaT.")

#         # Tach ngay va gio
#         df['Date'] = df['Formatted Date'].dt.date
#         df['Time'] = df['Formatted Date'].dt.time

#         # Chuyen doi cot Date ve kieu du lieu datetime
#         df['Date'] = pd.to_datetime(df['Date'])  # Chuyen cot Date sang datetime

#         # Chuyen doi cot Time sang kieu thoi gian
#         df['Time'] = df['Formatted Date'].dt.strftime('%H:%M:%S')  # Chuyen doi thanh chuoi thoi gian

#         # In ra gia tri trong cot Time de kiem tra
#         print("Cac gia tri trong cot Time truoc khi chuyen doi:")
#         print(df['Time'].head())

#         # Chuyen doi cac gia tri trong cot Time sang datetime.time
#         df['Time'] = pd.to_datetime(df['Time'], format='%H:%M:%S').dt.time  # Chuyen sang datetime.time

#         # Kiem tra kieu du lieu cua cot Time
#         print("\nKieu du lieu cua cot Time sau khi chuyen doi:")
#         print(df['Time'].dtype)

#         # In thong tin ve DataFrame sau khi tach
#         print("\n======================================")
#         print("Thong tin DataFrame sau khi tach cot:")
#         print(df.info())
#         print("======================================\n")

#         # Hien thi vai dong dau tien cua DataFrame
#         print("Vai dong dau tien cua DataFrame sau khi tach:")
#         print(df.head())

#     except Exception as e:
#         print(f"Co loi xay ra khi xu ly du lieu: {e}")
# else:
#     print("Cot 'Formatted Date' khong ton tai trong file CSV.")


# print("\n======================================")
# print("Kiem tra du lieu co bi trung lap hay khong: ")
# print("Co {} du lieu trung lap!!!".format(df.duplicated().sum()))
# print("======================================\n")


# print("\n======================================")
# print("Kiem tra du lieu co cac o bi thieu hay khong: ")
# print(df.isna().sum())
# print("======================================\n")


# print("\n======================================")
# print("Xoa cac dong co value bi thieu: ")
# df = df.dropna()
# print(df.info())
# print("======================================\n")


# print("\n======================================")
# print("Kiem tra lai du lieu co cac o bi thieu hay khong: ")
# print(df.isna().sum())
# print("======================================\n")


# print("\n======================================")
# df.drop(['Time'], axis = 1, inplace = True)
# print("Sau khi xoa cot Time: ")
# print(df.info())
# print("======================================\n")


# print("\n======================================")
# print("Cac loai du lieu trong cot SPrecip_Type: ")
# print(df.Precip_Type.unique())
# print(df.Precip_Type.value_counts())
# print("======================================\n")