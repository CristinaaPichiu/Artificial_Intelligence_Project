import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf
import joblib

# Funcție pentru prelucrarea și normalizarea datelor
def preprocess_data(file_path):
    # Încărcarea datelor din CSV
    sensor_data = pd.read_csv(file_path, index_col='Timestamp', parse_dates=True)

    # Selectează doar primele 5 coloane, presupunând că acestea sunt caracteristicile relevante
    selected_columns = sensor_data.iloc[:, :5]  # Schimbă această linie dacă coloanele relevante sunt diferite

    # Aplicarea MinMaxScaler pe coloanele selectate
    scaler = MinMaxScaler()
    sensor_data_normalized = scaler.fit_transform(selected_columns)

    return sensor_data_normalized, scaler


# Funcție pentru crearea secvențelor
def create_sequences(data, input_sequence_length, output_sequence_length):
    X, y = [], []
    for i in range(len(data) - input_sequence_length - output_sequence_length + 1):
        X.append(data[i:(i + input_sequence_length)])
        y.append(data[(i + input_sequence_length):(i + input_sequence_length + output_sequence_length)])
    return np.array(X), np.array(y)

class Seq2SeqModel:
    def __init__(self, input_sequence_length, output_sequence_length, input_dim, output_dim):
        self.input_sequence_length = input_sequence_length
        self.output_sequence_length = output_sequence_length
        self.input_dim = input_dim
        self.output_dim = output_dim
        self.model = self._build_model()

    def _build_model(self):
        # Encoder
        encoder_inputs = tf.keras.layers.Input(shape=(self.input_sequence_length, self.input_dim))
        encoder_lstm = tf.keras.layers.LSTM(100, return_state=True)
        encoder_outputs, state_h, state_c = encoder_lstm(encoder_inputs)
        encoder_states = [state_h, state_c]

        # Decoder
        decoder_inputs = tf.keras.layers.Input(shape=(self.output_sequence_length, self.output_dim))
        decoder_lstm = tf.keras.layers.LSTM(100, return_sequences=True, return_state=True)
        decoder_outputs, _, _ = decoder_lstm(decoder_inputs, initial_state=encoder_states)
        decoder_dense = tf.keras.layers.Dense(self.output_dim, activation='linear')
        decoder_outputs = decoder_dense(decoder_outputs)

        # Modelul Seq2Seq
        model = tf.keras.models.Model([encoder_inputs, decoder_inputs], decoder_outputs)
        return model

    def train(self, X, y, epochs=5, batch_size=32, validation_split=0.2):
        self.model.compile(optimizer='adam', loss='mean_squared_error')
        history = self.model.fit([X, y], y, epochs=epochs, batch_size=batch_size, validation_split=validation_split)
        return history

    def save(self, model_path):
        self.model.save(model_path)

    def load(self, model_path):
        self.model = tf.keras.models.load_model(model_path)
        print(self.model.summary())
        return self.model

    def predict(self, X):
        # Asigură-te că X are forma corectă
        if X.ndim == 2:
            X = np.reshape(X, (1, X.shape[0], X.shape[1]))  # Transformă (24, 5) în (1, 24, 5)

        decoder_input = np.zeros((X.shape[0], self.output_sequence_length, self.output_dim))
        predictions = self.model.predict([X, decoder_input])
        return predictions


if __name__ == '__main__':
    data, scaler = preprocess_data('SensorMLDataset.csv')
    X, y = create_sequences(data, 24, 24)

    model = Seq2SeqModel(24, 24, 5, 5)
    model.train(X, y)
    model.save('model.keras')
    joblib.dump(scaler, 'scaler.pkl')