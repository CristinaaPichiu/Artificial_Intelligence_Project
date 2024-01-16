import joblib
from flask import Flask, render_template, request, jsonify, send_from_directory
import models  # Asigură-te că models.py este în același director sau specifică calea corectă
import numpy as np

app = Flask(__name__)

input_sequence_length = 24
output_sequence_length = 24
input_dim = 5
output_dim = 5

model = models.Seq2SeqModel(input_sequence_length, output_sequence_length, input_dim, output_dim)
model.load('model.h5')


@app.route('/')
def index():
    return render_template('index.html')

scaler = joblib.load('scaler.pkl')

@app.route('/predict', methods=['POST'])
def predict():
    input_data = request.get_json()

    # Verifică și asigură-te că input_data este o listă de 24 de elemente, fiecare cu 5 caracteristici
    if not isinstance(input_data, list) or len(input_data) != 24 or any(len(entry) != 5 for entry in input_data):
        return jsonify({'error': 'Invalid input format'}), 400

    # Convertirea listei într-un array NumPy cu forma corectă
    X = np.array([input_data])  # Acest lucru va crea un array cu forma (1, 24, 5)

    # Asigură-te că datele sunt scalate corespunzător, dacă modelul a fost antrenat cu date scalate
    X_normalized = scaler.transform(X.reshape(-1, 5)).reshape(X.shape)

    # Realizarea predicțiilor
    predictions = model.predict(X_normalized)

    # De-normalizarea predicțiilor
    predictions_denormalized = scaler.inverse_transform(predictions.reshape(-1, predictions.shape[2])).reshape(predictions.shape)

    # Construirea răspunsului JSON
    response = {'predictions': predictions_denormalized.tolist()}

    # Aici poți adăuga și altele, cum ar fi timestamp-urile sau alte detalii

    return jsonify(response)

@app.route('/script.js')
def send_js():
    return send_from_directory('templates', 'script.js')


if __name__ == '__main__':
    app.run(debug=True)
