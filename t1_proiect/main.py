import pandas as pd

# Încărcați setul de date
df = pd.read_csv('SensorML_small.csv', parse_dates=['Timestamp'], dayfirst=True)

# Eliminați punctele din numerele cu virgulă mobilă
df.replace(regex=True, inplace=True, to_replace=r'\.', value='')

# Convertiți coloana Timestamp în format dată
df['Timestamp'] = pd.to_datetime(df['Timestamp'])

# Afișați primele rânduri ale setului de date
print(df.head())

import matplotlib.pyplot as plt
import seaborn as sns

# Setați stilul pentru grafice
sns.set(style="whitegrid")

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
    sns.boxplot(x=df[parameter], color='lightcoral')
    plt.title(f'Boxplot pentru {parameter}')

    # Cumulativ
    plt.subplot(2, 2, 4)
    sns.histplot(df[parameter], kde=True, cumulative=True, stat="density", common_norm=False, color='lightgreen')
    plt.title(f'Histogramă cumulativă pentru {parameter}')

    plt.tight_layout()
    plt.show()

# Apelați funcția pentru fiecare parametru
parameters = ['pres', 'temp1', 'umid', 'temp2', 'V450', 'B500', 'G550', 'Y570', 'O600', 'R650', 'temps1', 'temps2', 'lumina']
for parameter in parameters:
    univariate_analysis(parameter)

# Crearea unui heatmap pentru valorile medii
plt.figure(figsize=(12, 8))
sns.heatmap(df.groupby(df['Timestamp'].dt.date).mean(), annot=True, cmap='coolwarm')
plt.title('Heatmap pentru valorile medii pe zi')
plt.show()

# Crearea unui heatmap pentru valorile mediane
plt.figure(figsize=(12, 8))
sns.heatmap(df.groupby(df['Timestamp'].dt.date).median(), annot=True, cmap='coolwarm')
plt.title('Heatmap pentru valorile mediane pe zi')
plt.show()

# Crearea boxplot-urilor pentru identificarea outlierelor și distribuției valorilor
plt.figure(figsize=(16, 10))
sns.boxplot(data=df.drop(['Timestamp'], axis=1), palette='pastel')
plt.title('Boxplot-uri pentru identificarea outlierelor și a distribuției valorilor')
plt.xticks(rotation=45)
plt.show()
