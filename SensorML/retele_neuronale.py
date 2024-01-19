import numpy as np
import matplotlib.pyplot as plt
import os
from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from read_csv import load_and_clean_data
import base64
from io import BytesIO

# Funcție pentru a crea seturi de date de intrare și ieșire
def create_dataset(dataset, time_step):
    X, Y = [], []
    for i in range(len(dataset) - time_step - 1):
        a = dataset[i:(i + time_step), 0]
        X.append(a)
        Y.append(dataset[i + time_step, 0])
    return np.array(X), np.array(Y)


def function_LSTM(df, column):
    # Extrage coloana pentru predicție
    data = df[column].values.reshape(-1, 1)

    # Normalizează datele
    scaler = MinMaxScaler(feature_range=(0, 1))
    data_normalized = scaler.fit_transform(data)

    # Crearea seturilor de date de antrenare și test
    train_data, test_data = train_test_split(data_normalized, test_size=0.2, shuffle=False)

    # Crearea seturilor de date pentru antrenare și testare
    # Parametrii modelului
    time_step = 5
    n_features = 1

    # Crearea seturilor de antrenare și test
    X_train, y_train = create_dataset(train_data, time_step)
    X_test, y_test = create_dataset(test_data, time_step)

    # Redimensionarea intrării pentru modelul LSTM
    X_train = X_train.reshape(X_train.shape[0], X_train.shape[1], n_features)
    X_test = X_test.reshape(X_test.shape[0], X_test.shape[1], n_features)

    # Construirea modelului LSTM
    model = Sequential()
    model.add(LSTM(50, return_sequences=True, input_shape=(time_step, n_features)))
    model.add(LSTM(50, return_sequences=False))
    model.add(Dense(1))

    # Compilarea modelului
    model.compile(optimizer='adam', loss='mean_squared_error')

    # Antrenarea modelului
    model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=5, batch_size=32, verbose=1)

    # Predicții
    train_predict = model.predict(X_train)
    test_predict = model.predict(X_test)

    # Transformarea înapoi la scala originală
    train_predict = scaler.inverse_transform(train_predict)
    test_predict = scaler.inverse_transform(test_predict)

    # Vizualizează rezultatele pentru coloana curentă
    plt.figure(figsize=(10, 6))
    plt.plot(scaler.inverse_transform(data_normalized), label='Datele Originale')
    plt.plot(np.arange(time_step, len(train_predict) + time_step), train_predict, label='Predicții Antrenare')
    plt.plot(np.arange(len(train_predict) + (2 * time_step) + 1, len(data_normalized) - 1), test_predict,
         label='Predicții Test')
    plt.title(f'Predicția Parametrilor pentru {column}')
    plt.xlabel('Timp')
    plt.ylabel(f'Valoarea Parametrului pentru {column}')
    plt.legend()

    image_path = f'static/images/{column}_RN.png'
    plt.savefig(image_path)
    plt.close()

    return image_path


def return_path(column):
    directory = 'static/images'  # Setează directorul în care dorești să cauți

    # Parcurge fișierele din directorul specificat
    for filename in os.listdir(directory):
        if filename.startswith(column) and filename.endswith("RN.png"):
            return filename

    return None  # Întoarce None dacă nu se găsește fișierul


if __name__ == '__main__':
    # Încărcarea și curățarea datelor
    file_path = 'SensorMLDataset.csv'
    df = load_and_clean_data(file_path)
    numeric_columns = ['pres', 'temp1', 'umid', 'temp2', 'V450', 'B500', 'G550', 'Y570', 'O600', 'R650', 'temps1',
                       'temps2', 'lumina']
    for column in numeric_columns:
        function_LSTM(df,column)