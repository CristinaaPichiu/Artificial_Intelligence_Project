import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from prophet import Prophet

# Încărcați setul de date
df = pd.read_csv('SensorML_small.csv', parse_dates=['Timestamp'], dayfirst=True)

# Eliminați punctele și spațiile din numerele cu virgulă mobilă
df.replace(regex=True, inplace=True, to_replace=[r'\.', r' '], value='')

# Convertiți coloana Timestamp în format dată
df['Timestamp'] = pd.to_datetime(df['Timestamp'], format="%m/%d/%Y %H:%M")

# Conversia datelor la tip numeric
df = df.apply(pd.to_numeric, errors='coerce')

# Funcție pentru a crea analiza univariată
def univariate_analysis(parameter):
    plt.figure(figsize=(12, 6))

    # Histograma
    plt.subplot(2, 2, 1)
    sns.histplot(df[parameter], kde=True, color='skyblue')
    plt.title(f'Histograma pentru {parameter}')

    # Seria temporală
    plt.subplot(2, 2, 2)
    sns.lineplot(x='Timestamp', y=parameter, data=df, color='orange')
    plt.title(f'Seria temporală pentru {parameter}')
    plt.xticks(rotation=45)

    # Boxplot
    plt.subplot(2, 2, 3)
    sns.boxplot(data=df[parameter], palette='pastel', showfliers=False)
    plt.title(f'Boxplot pentru {parameter}')

    # Cumulativ
    plt.subplot(2, 2, 4)
    sns.histplot(df[parameter], kde=True, cumulative=True, stat="density", common_norm=False, color='lightgreen')
    plt.title(f'Histogramă cumulativă pentru {parameter}')

    plt.tight_layout()

    # Salvați diagrama curentă într-o variabilă
    global current_plot
    current_plot = plt.gcf()

    return current_plot

# Apelați funcția pentru fiecare parametru
parameters = ['pres', 'temp1', 'umid', 'temp2', 'V450', 'B500', 'G550', 'Y570', 'O600', 'R650', 'temps1', 'temps2', 'lumina']
for parameter in parameters:
    # Apelați funcția de mai jos pentru a crea o copie a diagramei
    univariate_analysis(parameter)
    plt.show()

# Crearea unui heatmap pentru valorile medii
plt.figure(figsize=(12, 8))
mean_heatmap = df.groupby(df['Timestamp'].dt.date).mean()
sns.heatmap(mean_heatmap, annot=True, cmap='coolwarm', fmt=".2f")
plt.title('Heatmap pentru valorile medii pe zi')
plt.show()

# Crearea unui heatmap pentru valorile mediane
plt.figure(figsize=(12, 8))
median_heatmap = df.groupby(df['Timestamp'].dt.date).median()
sns.heatmap(median_heatmap, annot=True, cmap='coolwarm', fmt=".2f")
plt.title('Heatmap pentru valorile mediane pe zi')
plt.show()

# Crearea boxplot-urilor pentru identificarea outlierelor și distribuției valorilor
plt.figure(figsize=(16, 10))
sns.boxplot(data=df.drop(['Timestamp'], axis=1), palette='pastel')
plt.title('Boxplot-uri pentru identificarea outlierelor și a distribuției valorilor')
plt.xticks(rotation=45)
plt.show()

# Determinați matricea de corelație
correlation_matrix = df.corr()

# Afișați matricea de corelație
plt.figure(figsize=(12, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')
plt.title('Matrice de corelație')
plt.show()

# Antrenare model Prophet pentru fiecare parametru
for parameter in parameters:
    # Creează un dataframe pentru antrenare
    train_data = df[['Timestamp', parameter]].rename(columns={'Timestamp': 'ds', parameter: 'y'})

    # Inițializare și antrenare model
    model = Prophet(yearly_seasonality=True, weekly_seasonality=True, daily_seasonality=False)
    model.fit(train_data)

    # Crearea unui dataframe pentru predictie
    future = model.make_future_dataframe(periods=48, freq='H')  # 48 de ore înainte
    forecast = model.predict(future)

    # Afișare grafic cu predicțiile
    fig = model.plot(forecast)
    plt.title(f'Prophet Predictions for {parameter}')
    plt.show()

    # Afișare eroare la antrenare utilizând cross-validare
    fig = model.plot_components(forecast)
    plt.show()

