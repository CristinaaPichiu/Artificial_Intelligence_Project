import joblib
from flask import Flask, render_template, request, jsonify, send_from_directory
import models  # Asigură-te că models.py este în același director sau specifică calea corectă
import numpy as np
import logging

# Configurarea logger-ului
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)

input_sequence_length = 24
output_sequence_length = 24
input_dim = 5
output_dim = 5

model = models.Seq2SeqModel(input_sequence_length, output_sequence_length, input_dim, output_dim)
model.load('model.keras')
scaler = joblib.load('scaler.pkl')

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    try:
        input_data = request.get_json()
        if isinstance(input_data, list):
            # Verifică dacă lista conține 24 de elemente
            if len(input_data) != 24:
                raise ValueError("Număr incorect de seturi de date.")

            # Transformă fiecare obiect JSON într-un array și leagă-le
            X = np.array([list(item.values()) for item in input_data])

            # Asigură-te că X are forma corectă (24, 5)
            if X.shape != (24, 5):
                raise ValueError("Forma datelor de intrare este incorectă.")

            # Aplică scaler și predicția
            X_normalized = scaler.transform(X)
            predictions = model.predict(X_normalized.reshape(1, 24, 5))
            predictions = predictions.reshape(-1, output_dim)
            predictions_denormalized = scaler.inverse_transform(predictions)

            response = {'predictions': predictions_denormalized.tolist()}
            return jsonify(response)
        else:
            raise ValueError("Formatul datelor de intrare este incorect.")
    except Exception as e:
        logging.error(f"Eroare la procesarea predicției: {e}")
        return jsonify({"error": str(e)}), 500




@app.route('/script.js')
def send_js():
    return send_from_directory('templates', 'script.js')


if __name__ == '__main__':
    app.run(debug=True)
