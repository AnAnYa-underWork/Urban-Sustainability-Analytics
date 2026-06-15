import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.preprocessing import MinMaxScaler

df = pd.read_excel("maths dataset.xlsx")
df_2023 = df[df['YEAR'] == 2023].drop(columns='YEAR')

metrics = df_2023.columns.drop('CITY')
scaler = MinMaxScaler()
df_2023[metrics] = scaler.fit_transform(df_2023[metrics])

def plot_radar(city_data, title):
    labels = metrics.tolist()
    values = city_data[metrics].values.flatten().tolist()
    values += values[:1]  # close the loop

    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax.plot(angles, values, marker='o')
    ax.fill(angles, values, alpha=0.25)
    ax.set_title(title, size=12)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)
    ax.set_yticklabels([])
    plt.show()

for city in ['Delhi', 'Mumbai', 'Chennai']:
    city_row = df_2023[df_2023['CITY'] == city]
    if not city_row.empty:
        plot_radar(city_row, title=f"Urban Metric Profile - {city}")
