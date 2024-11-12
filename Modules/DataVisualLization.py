import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import tkinter as tk
from tkinter import Button
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Assuming the file path is valid
currentDir = os.path.dirname(__file__)
dataPath = os.path.join(currentDir, '../Data/EnglandWeather.csv')
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
    ax.clear()
    sns.countplot(y='Summary', data=df_plot, palette="YlOrBr", ax=ax)
    ax.set_title('Summary Count', fontsize=16)
    plt.xticks(rotation=90)
    canvas.draw()

def show_month_count():
    ax.clear()
    sns.countplot(x='month', data=df_plot, palette="YlOrBr", ax=ax)
    ax.set_xticks(np.arange(12))
    ax.set_xticklabels(month_names, rotation=90)
    ax.set_title('Month Count', fontsize=16)
    canvas.draw()

def show_precip_type():
    ax.clear()
    sns.countplot(y='Precip_Type', data=df_plot, palette="YlOrBr", ax=ax)
    ax.set_title('Precip Type Count', fontsize=16)
    plt.xticks(rotation = 90)
    canvas.draw()

def show_max_humidity():
    global canvas, ax
    ax.clear()
    max_humidity_by_summary = df_plot.groupby('Summary')['Humidity'].mean().sort_values(ascending=False)
    order = max_humidity_by_summary.index.tolist()
    sns.barplot(x='Humidity', y='Summary', data=df_plot, order=order, palette='YlOrBr', ax=ax)
    for index, value in enumerate(max_humidity_by_summary):
        ax.text(value, index, f' {round(value, 2)}', va='center')
    ax.set_xlabel('Humidity')
    ax.set_ylabel('Summary')
    ax.set_title('Average Humidity by Summary')
    canvas.draw()

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
    
    Button(button_frame, text="Summary Count", command=show_summary_count, width=25, height=2, bg="#90caf9", fg="black").grid(row=0, column=0, pady=5)
    Button(button_frame, text="Month Count", command=show_month_count, width=25, height=2, bg="#90caf9", fg="black").grid(row=1, column=0, pady=5)
    Button(button_frame, text="Precip Type", command=show_precip_type, width=25, height=2, bg="#90caf9", fg="black").grid(row=2, column=0, pady=5)
    Button(button_frame, text="Max Humidity", command=show_max_humidity, width=25, height=2, bg="#90caf9", fg="black").grid(row=3, column=0, pady=5)
    Button(button_frame, text="Exit", command=exit_app, width=25, height=2, bg="#ff8a80", fg="white").grid(row=4, column=0, pady=5)

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
