import pandas as pd

# Încarc setul de date

data = pd.read_csv('SensorML_small.csv')
data['Timestamp'] = pd.to_datetime(data['Timestamp'])
data.replace(regex=True, inplace=True, to_replace=[r'\.', r' '], value='')

# Renumim coloanele pentru a le face compatibile cu analiza de corelație
data = data.rename(columns={'Timestamp': 'ds', 'pres': 'y_pres', 'temp1': 'y_temp1', 'umid': 'y_umid', 'temp2': 'y_temp2',
                            'V450': 'y_V450', 'B500': 'y_B500', 'G550': 'y_G550', 'Y570': 'y_Y570', 'O600': 'y_O600',
                            'R650': 'y_R650', 'temps1': 'y_temps1', 'temps2': 'y_temps2', 'lumina': 'y_lumina'})

# Curățăm datele și le convertim numeric
data_numeric = data.apply(lambda x: pd.to_numeric(x))
print(data)

#data_numeric e full matricea si cu prima coloana (etichete)

# Calculăm matricea de corelație
correlation_matrix = data_numeric.corr()
print("Matrice de Corelație:")
print(correlation_matrix)


# Analizăm corelațiile pentru fiecare variabilă
for variable in data_numeric.columns:
    variable_correlations = correlation_matrix[variable]

    direct_correlations = variable_correlations[variable_correlations > 0].sort_values(ascending=False)
    inverse_correlations = variable_correlations[variable_correlations < 0].sort_values()

    print(f"\nVariabile cu corelație directă puternică pentru '{variable}':")
    print(direct_correlations)

    print(f"\nVariabile cu corelație inversă puternică pentru '{variable}':")
    print(inverse_correlations)

    print('-' * 50)

