import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Assuming the file path is valid
currentDir = os.path.dirname(__file__)
dataPath = os.path.join(currentDir, '../Data/EnglandWeather2.csv')
df = pd.read_csv(dataPath)

# Helper function for seasons
def get_season(month):
    if month in [12, 1, 2]:
        return 'Winter'
    elif month in [3, 4, 5]:
        return 'Spring'
    elif month in [6, 7, 8]:
        return 'Summer'
    else:
        return 'Autumn'

df.fillna('rain', inplace=True)
df[['date', 'time']] = df['Formatted Date'].str.split(' ', n=1, expand=True)
df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month
df['day'] = df['date'].dt.day
df['hour'] = pd.to_numeric(df['time'].str[:2], errors='coerce').fillna(0).astype(int)  # Extract hour correctly
df['Humidity'] = df['Humidity'] * 100
df['season'] = df['month'].apply(get_season)

# Create a simpler DataFrame for plotting
df_plot = df.copy()
df_plot = df_plot.drop(columns=['Formatted Date', 'time']).sort_values(by=['year', 'month', 'day', 'hour']).reset_index(drop=True)

month_names = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

# Plotting functions
def show_summary_count():
    global canvas, figure, ax
    # Xóa toàn bộ figure
    figure.clf()
    # Tạo lại trục mới
    ax = figure.add_subplot(111)
    sns.countplot(y='Summary', data=df_plot, palette="YlOrBr", ax=ax)
    ax.set_title('Summary Count', fontsize=16)
    plt.xticks(rotation=90)
    canvas.draw()

def show_month_count():
    global canvas, figure, ax
    # Xóa toàn bộ figure
    figure.clf()
    # Tạo lại trục mới
    ax = figure.add_subplot(111)
    sns.countplot(x='month', data=df_plot, palette="YlOrBr", ax=ax)
    ax.set_xticks(np.arange(12))
    ax.set_xticklabels(month_names, rotation=90)
    ax.set_title('Month Count', fontsize=16)
    canvas.draw()

def show_precip_type():
    global canvas, figure, ax
    # Xóa toàn bộ figure
    figure.clf()
    # Tạo lại trục mới
    ax = figure.add_subplot(111)
    sns.countplot(y='Precip_Type', data=df_plot, palette="YlOrBr", ax=ax)
    ax.set_title('Precip Type Count', fontsize=16)
    plt.xticks(rotation = 90)
    canvas.draw()

def show_max_humidity():
    global canvas, figure, ax
    # Xóa toàn bộ figure
    figure.clf()
    # Tạo lại trục mới
    ax = figure.add_subplot(111)
    max_humidity_by_summary = df_plot.groupby('Summary')['Humidity'].mean().sort_values(ascending=False)
    order = max_humidity_by_summary.index.tolist()
    sns.barplot(x='Humidity', y='Summary', data=df_plot, order=order, palette='YlOrBr', ax=ax)
    for index, value in enumerate(max_humidity_by_summary):
        ax.text(value, index, f' {round(value, 2)}', va='center')
    ax.set_xlabel('Humidity')
    ax.set_ylabel('Summary')
    ax.set_title('Average Humidity by Summary')
    canvas.draw()

def show_heatmap():
    global canvas, figure, ax
    # Xóa toàn bộ figure
    figure.clf()
    # Tạo lại trục mới
    ax = figure.add_subplot(111)
    correlation_matrix = df_plot[['Temperature (C)', 'Wind Speed (km/h)', 'Pressure (millibars)', 'Humidity']].corr()
    # Vẽ heatmap lên trục mới
    sns.heatmap(correlation_matrix, annot=True, cmap="YlOrBr", ax=ax)
    # Đặt tiêu đề cho heatmap
    ax.set_title('Correlation Heatmap', fontsize=16)
    canvas.draw()

# Hover effect functions
def on_enter(event, button):
    button['bg'] = '#ff8a80'  # Change button color on hover
    button['fg'] = 'white'

def on_leave(event, button):
    button['bg'] = '#90caf9'  # Revert button color when mouse leaves
    button['fg'] = 'black'

# Main GUI function
def create_gui():
    global canvas, ax, figure
    root = tk.Tk()
    root.title("Weather Data Visualization")

    def exit_app():
        root.quit()
        root.destroy()

    # Fullscreen toggle
    root.attributes("-fullscreen", True)
    root.bind("<Escape>", lambda e: root.attributes("-fullscreen", False))

    # Cấu hình lưới cho bố cục giao diện
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1, minsize=200)
    root.grid_columnconfigure(1, weight=4)

    # Frame cho các nút với màu nền nhẹ nhàng
    button_frame = tk.Frame(root, bg="#e3f2fd")  # Màu xanh nhạt
    button_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
    
    # Tạo các nút với hiệu ứng
    button1 = tk.Button(button_frame, text="Summary Count", command=show_summary_count, width=25, height=2, bg="#90caf9", fg="black")
    button1.grid(row=0, column=0, pady=5)
    button1.bind("<Enter>", lambda event, button=button1: on_enter(event, button))
    button1.bind("<Leave>", lambda event, button=button1: on_leave(event, button))

    button2 = tk.Button(button_frame, text="Month Count", command=show_month_count, width=25, height=2, bg="#90caf9", fg="black")
    button2.grid(row=1, column=0, pady=5)
    button2.bind("<Enter>", lambda event, button=button2: on_enter(event, button))
    button2.bind("<Leave>", lambda event, button=button2: on_leave(event, button))

    button3 = tk.Button(button_frame, text="Precip Type", command=show_precip_type, width=25, height=2, bg="#90caf9", fg="black")
    button3.grid(row=2, column=0, pady=5)
    button3.bind("<Enter>", lambda event, button=button3: on_enter(event, button))
    button3.bind("<Leave>", lambda event, button=button3: on_leave(event, button))

    button4 = tk.Button(button_frame, text="Max Humidity", command=show_max_humidity, width=25, height=2, bg="#90caf9", fg="black")
    button4.grid(row=3, column=0, pady=5)
    button4.bind("<Enter>", lambda event, button=button4: on_enter(event, button))
    button4.bind("<Leave>", lambda event, button=button4: on_leave(event, button))

    button5 = tk.Button(button_frame, text="Heatmap", command=show_heatmap, width=25, height=2, bg="#90caf9", fg="black")
    button5.grid(row=4, column=0, pady=5)
    button5.bind("<Enter>", lambda event, button=button5: on_enter(event, button))
    button5.bind("<Leave>", lambda event, button=button5: on_leave(event, button))

    button6 = tk.Button(button_frame, text="Exit", command=exit_app, width=25, height=2, bg="#ff8a80", fg="white")
    button6.grid(row=5, column=0, pady=5)
    button6.bind("<Enter>", lambda event, button=button6: on_enter(event, button))
    button6.bind("<Leave>", lambda event, button=button6: on_leave(event, button))

    # Frame cho Canvas với nền trong suốt
def on_enter(event, button):
    button.config(bg="#81d4fa", relief="sunken", borderwidth=2)  # Đổi nền và tạo chiều sâu nút khi hover
    button.config(cursor="hand2")  # Hiệu ứng trỏ chuột tay

def on_leave(event, button):
    button.config(bg="#90caf9", relief="raised", borderwidth=0)  # Quay lại kiểu mặc định

def create_gui():
    global canvas, ax, figure
    root = tk.Tk()
    root.title("Weather Data Visualization")

    def exit_app():
        root.quit()
        root.destroy()

    # Fullscreen toggle
    root.attributes("-fullscreen", True)
    root.bind("<Escape>", lambda e: root.attributes("-fullscreen", False))

    # Cấu hình lưới cho bố cục giao diện
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1, minsize=200)
    root.grid_columnconfigure(1, weight=4)

    # Frame cho các nút với màu nền nhẹ nhàng
    button_frame = tk.Frame(root, bg="#e3f2fd")  # Màu xanh nhạt
    button_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
    
   # Tạo các nút với hiệu ứng

    def on_enter(event, button):
        # Khi chuột vào, thay đổi màu nền nút
        button.config(bg="#81c784")  # Ví dụ, nền sáng hơn khi hover

    def on_leave(event, button):
        # Khi chuột rời, kiểm tra nếu đây là nút Exit, giữ màu nền đỏ
        if button['text'] == "Exit":
            button.config(bg="red")
        else:
            button.config(bg="#90caf9")  # Màu nền mặc định


    button1 = tk.Button(button_frame, text="Summary Count", command=show_summary_count, width=25, height=2, bg="#90caf9", fg="black", font=("Helvetica", 12, "bold"))
    button1.grid(row=0, column=0, pady=5)
    button1.bind("<Enter>", lambda event, button=button1: on_enter(event, button))
    button1.bind("<Leave>", lambda event, button=button1: on_leave(event, button))

    button2 = tk.Button(button_frame, text="Month Count", command=show_month_count, width=25, height=2, bg="#90caf9", fg="black", font=("Helvetica", 12, "bold"))
    button2.grid(row=1, column=0, pady=5)
    button2.bind("<Enter>", lambda event, button=button2: on_enter(event, button))
    button2.bind("<Leave>", lambda event, button=button2: on_leave(event, button))

    button3 = tk.Button(button_frame, text="Precip Type", command=show_precip_type, width=25, height=2, bg="#90caf9", fg="black", font=("Helvetica", 12, "bold"))
    button3.grid(row=2, column=0, pady=5)
    button3.bind("<Enter>", lambda event, button=button3: on_enter(event, button))
    button3.bind("<Leave>", lambda event, button=button3: on_leave(event, button))

    button4 = tk.Button(button_frame, text="Max Humidity", command=show_max_humidity, width=25, height=2, bg="#90caf9", fg="black", font=("Helvetica", 12, "bold"))
    button4.grid(row=3, column=0, pady=5)
    button4.bind("<Enter>", lambda event, button=button4: on_enter(event, button))
    button4.bind("<Leave>", lambda event, button=button4: on_leave(event, button))

    button5 = tk.Button(button_frame, text="Heatmap", command=show_heatmap, width=25, height=2, bg="#90caf9", fg="black", font=("Helvetica", 12, "bold"))
    button5.grid(row=4, column=0, pady=5)
    button5.bind("<Enter>", lambda event, button=button5: on_enter(event, button))
    button5.bind("<Leave>", lambda event, button=button5: on_leave(event, button))

    button6 = tk.Button(button_frame, text="Exit", command=exit_app, width=25, height=2, bg="red", fg="white", font=("Helvetica", 12, "bold"))
    button6.grid(row=5, column=0, pady=5)
    button6.bind("<Enter>", lambda event, button=button6: on_enter(event, button))
    button6.bind("<Leave>", lambda event, button=button6: on_leave(event, button))


    # Frame cho Canvas với nền trong suốt, tạo sự kết nối với nền tổng thể
    canvas_frame = tk.Frame(root, bg="#bbdefb")
    canvas_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
    
    figure = plt.Figure(figsize=(6, 6), tight_layout=True)
    ax = figure.add_subplot(111)
    canvas = FigureCanvasTkAgg(figure, canvas_frame)
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    root.mainloop()

if __name__ == "__main__":
    create_gui()
