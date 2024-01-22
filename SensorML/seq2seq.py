import os

import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf
import matplotlib.pyplot as plt

from read_csv import load_and_clean_data


# Funcție pentru crearea secvențelor
def create_sequences(data, input_sequence_length, output_sequence_length):
    X, y = [], []
    for i in range(len(data) - input_sequence_length - output_sequence_length + 1):
        X.append(data[i:(i + input_sequence_length), 0].reshape(input_sequence_length, 1))
        y.append(data[(i + input_sequence_length):(i + input_sequence_length + output_sequence_length), 0].reshape(output_sequence_length, 1))
    return np.array(X), np.array(y)

def function_Seq2Seq(df, column):
    # Extrage coloana pentru predicție
    data = df[column].values.reshape(-1, 1)

    # Normalizează datele
    scaler = MinMaxScaler(feature_range=(0, 1))
    data_normalized = scaler.fit_transform(data)

    # Crearea seturilor de date pentru antrenare și testare
    input_sequence_length = 24
    output_sequence_length = 24

    # Crearea secvențelor
    X, y = create_sequences(data_normalized, input_sequence_length, output_sequence_length)

    # Dimensiunile input și output
    input_dim = 1  # Există o singură caracteristică per pas de timp
    output_dim = 1  # Există o singură caracteristică de ieșire pentru fiecare pas de timp în secvența de ieșire

    # Encoder
    encoder_inputs = tf.keras.layers.Input(shape=(input_sequence_length, input_dim))
    encoder_lstm = tf.keras.layers.LSTM(50, return_state=True)
    encoder_outputs, state_h, state_c = encoder_lstm(encoder_inputs)
    encoder_states = [state_h, state_c]

    # Decoder
    decoder_inputs = tf.keras.layers.Input(shape=(output_sequence_length, input_dim))  # Ajustează această linie
    decoder_lstm = tf.keras.layers.LSTM(50, return_sequences=True, return_state=True)
    decoder_outputs, _, _ = decoder_lstm(decoder_inputs, initial_state=encoder_states)
    decoder_dense = tf.keras.layers.Dense(output_dim, activation='linear')
    decoder_outputs = decoder_dense(decoder_outputs)
    # Modelul Seq2Seq
    model = tf.keras.models.Model([encoder_inputs, decoder_inputs], decoder_outputs)

    # Afișarea sumarului modelului
    model.summary()

    # Compilarea modelului
    model.compile(optimizer='adam', loss='mean_squared_error')

    # Antrenarea modelului
    history = model.fit([X, np.zeros((X.shape[0], output_sequence_length, input_dim))], y, epochs=5, batch_size=32, validation_split=0.2)

    # Generarea predicțiilor
    decoder_input = np.zeros((X.shape[0], output_sequence_length, output_dim))
    predictions = model.predict([X, decoder_input])

    # De-normalizarea predicțiilor și a valorilor reale (dacă este necesar)
    predictions_original = scaler.inverse_transform(predictions.reshape(-1, predictions.shape[2])).reshape(predictions.shape)
    y_original = scaler.inverse_transform(y.reshape(-1, y.shape[2])).reshape(y.shape)

    # Vizualizarea evoluției pentru fiecare coloană
    for i in range(output_dim):
        # Alegerea unei serii temporale pentru afișare
        index = 0  # Exemplu: prima serie temporală
        predicted_sequence = predictions_original[index][:, i]
        true_sequence = y_original[index][:, i]

        # Setarea intervalului de timp pentru axa X
        time_steps = range(len(predicted_sequence))

        # Crearea graficului
        plt.figure(figsize=(12, 6))
        plt.plot(time_steps, true_sequence, label='Actual', linewidth=2)  # Linii mai groase
        plt.plot(time_steps, predicted_sequence, label='Predicted', linewidth=2)
        plt.title(f'Evoluția coloanei {column} în timp', fontsize=14)  # Titlu lizibil
        plt.xlabel('Time Step', fontsize=12)
        plt.ylabel('Value', fontsize=12)
        plt.legend(fontsize=12)
        plt.grid(True)  # Adăugarea unei grile
        plt.tight_layout()  # Asigură-te că totul se încadrează bine

        # Salvarea imaginii
        image_path = f'static/images/{column}_Seq2Seq.png'
        plt.savefig(image_path)
        plt.close()

        print(f'Imaginea salvată la: {image_path}')

    return image_path


def return_pathSeq2Seq(column):
    directory = 'static/images'  # Setează directorul în care dorești să cauți
    # Parcurge fișierele din directorul specificat
    for filename in os.listdir(directory):
        if filename.startswith(column) and filename.endswith("seq2seq.png"):
            return filename

    return None  # Întoarce None dacă nu se găsește fișierul


if __name__ == '__main__':
    # Încărcarea și curățarea datelor
    file_path = 'SensorMLDataset.csv'
    df = load_and_clean_data(file_path)
    numeric_columns = ['pres', 'temp1', 'umid', 'temp2', 'V450', 'B500', 'G550', 'Y570', 'O600', 'R650', 'temps1',
                       'temps2', 'lumina']
    for column in numeric_columns:
        function_Seq2Seq(df,column)