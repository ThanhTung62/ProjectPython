import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

currentDir = os.path.dirname(__file__)
dataPath = os.path.join(currentDir, '../Data/EnglandWeather.csv')
    
df = pd.read_csv(dataPath)

def get_season(month):
    if month in [12, 1, 2]:
        return 'Winter'
    elif month in [3, 4, 5]:
        return 'Spring'
    elif month in [6, 7, 8]:
        return 'Summer'
    else:
        return 'Autumn'

def split_time(hour):
    if 0 <= hour <= 11:
        return "Morning"
    elif 12 <= hour <= 24:
        return "Evening"
    else:
        return "nan"

df2 = df.copy()
df2.fillna('rain', inplace=True)
df2.isna().sum()
df2[['date', 'time']] = df2['Formatted Date'].str.split(' ', n=1, expand=True)

df3 = df2.drop('Formatted Date', axis=1)
df3["date"] = pd.to_datetime(df3["date"], format='%Y-%m-%d')
df3['year'] = df3['date'].dt.year
df3["month"] = df3["date"].dt.month
df3['day'] = df3['date'].dt.day
df3['hour'] = df3['date'].dt.hour
df3['Humidity'] = df3['Humidity']*100

df3 = df3.sort_values('date')
df3 = df3.reset_index(drop=True)
df3.sort_values(by=['year', 'month', 'day', 'hour'], inplace=True)

cols = df3.columns.to_list()
cols = cols[-2:] + cols[:-2]
df3 = df3[cols]

df3['season'] = df3['month'].apply(get_season)
df4=pd.DataFrame(df3,columns=["Summary","Precip Type","season"])
month_names = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

def show1():
    plt.figure(figsize=(18, 6))
    ax = sns.countplot(y='Summary', data=df4, palette="YlOrBr")
    plt.xticks(rotation=90)
    plt.title('Summary Count', fontsize=16)
    plt.show()

def show2():
    fig , ax = plt.subplots(figsize=(18,6))
    ax = sns.countplot(x=df3['month'], data=df3, palette="YlOrBr")
    plt.xticks(ticks=np.arange(12), labels=month_names, rotation = 90)
    plt.title('Month Count', fontsize=16)
    plt.show()

def show3():
    fig, axes = plt.subplots(figsize=(15,4) , nrows=2, ncols=2)
    fig.suptitle('Histogram of Numerical features', fontsize=16)
    i=0
    j=0
    columns = ['Temperature (C)', 'Wind Speed (km/h)', 'Humidity', 'Pressure (millibars)']
    for col in columns:
        sns.histplot(ax=axes[i,j], data=df3, x=col, kde=True,color='#f4a261')
        if j == 1:
            i += 1
            j = 0
        else:
            j += 1
    plt.tight_layout()
    plt.show()

def show4():
    max_humidity_by_summary = df3.groupby('Summary')['Humidity'].mean().sort_values(ascending=False)
    order = max_humidity_by_summary.index.tolist()
    plt.figure(figsize=(25, 10))
    sns.barplot(x='Humidity', y='Summary', data=df3, order=order, palette='YlOrBr')
    for index, value in enumerate(max_humidity_by_summary):
        plt.text(value, index, f' {round(value , 2)}', va='center')
    plt.xlabel('Humidity')
    plt.ylabel('Summary')
    plt.title('Maximum Humidity by Summary')
    plt.show()

def main():
    show1()
    show2()
    show3()
    show4()

if __name__ == "__main__":
    main()