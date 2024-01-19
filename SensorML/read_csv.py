import pandas as pd


def load_and_clean_data(file_path_csv):
    # Încărcăm setul de date
    df = pd.read_csv(file_path_csv, parse_dates=['Timestamp'], dayfirst=False)

    numeric_columns = ['pres', 'temp1', 'umid', 'temp2', 'V450', 'B500', 'G550', 'Y570', 'O600', 'R650', 'temps1',
                       'temps2', 'lumina']
    df[numeric_columns] = df[numeric_columns].replace(',', '', regex=True).astype(float)

    # Convertim coloana Timestamp în format dată
    df['Timestamp'] = pd.to_datetime(df['Timestamp'], format='%m/%d/%Y %H:%M', errors='coerce')

    # Eliminăm rândurile care au valori nule
    df = df.dropna(how='any')
    df = df.apply(pd.to_numeric, errors='coerce')
    return df