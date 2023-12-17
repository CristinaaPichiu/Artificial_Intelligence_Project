import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from prophet import Prophet

# Încărcați datele
df = pd.read_csv("SensorML_small.csv")

# Convertiți coloana de timestamp în format dată
df['Timestamp'] = pd.to_datetime(df['Timestamp'])

# 1. Analiza univariată a datelor
for col in df.columns[1:]:  # Excludem prima coloana care este 'Timestamp'
    # Histograma
    plt.figure(figsize=(10, 6))
    sns.histplot(df[col], bins=30, kde=True)
    plt.title(col + ' Histogram')
    plt.xlabel(col)
    plt.ylabel('Frequency')
    plt.show()

    # Boxplot
    plt.figure(figsize=(10, 6))
    sns.boxplot(x=df[col])
    plt.title(col + ' Boxplot')
    plt.xlabel(col)
    plt.show()

    # Heatmap
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(df.groupby(df['Timestamp'].dt.date)[col].agg(['mean', 'median']).transpose(), cmap="viridis", annot=True)
    plt.title(col + ' Daily Mean and Median Heatmap')
    plt.show()

# 2. Determinați matricea de corelație
corr = df.corr()

# Afișați matricea de corelație
print("Matricea de corelație:")
print(corr)

# 3. Antrenați modelul Prophet pentru fiecare parametru
for col in df.columns[2:]:  # Excludem primele doua coloane care sunt 'Timestamp' și 'pres'
    # Pregătiți datele pentru Prophet
    data = df[['Timestamp', col]]
    data.columns = ['ds', 'y']

    # Creați și antrenați modelul
    m = Prophet()
    m.fit(data)

    # Creează dataframe pentru predicții
    future = m.make_future_dataframe(periods=48, freq="H")

    # Generați predicții
    forecast = m.predict(future)

    # 4. Realizați grafice pentru predicții
    fig = m.plot(forecast)
    plt.title(f'{col} - Predicții vs. Realitate')
    plt.xlabel('Timestamp')
    plt.ylabel(col)
    plt.show()

    # 5. Afișați eroarea la antrenare utilizând cross-validare
    mse = np.mean((forecast["yhat"] - data["y"])**2)
    print(f'Eroarea medie la antrenare pentru {col}: {mse}')

    # Afișați componentele sezoniere și tendința
    fig = m.plot_components(forecast)
    plt.show()
