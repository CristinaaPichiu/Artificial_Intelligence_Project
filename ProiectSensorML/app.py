from flask import Flask, render_template, request, jsonify
import models  # Asigură-te că models.py este în același director
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


@app.route('/predict', methods=['POST'])
def predict():
    input_data = request.get_json()

    processed_data = np.array([[input_data['temperature'], input_data['humidity'], input_data['light'],
                                input_data['pressure'], input_data['soil_moisture']]])

    predictions = model.predict(processed_data)

    # Aici adaugi logica de manipulare a datelor pentru a crea răspunsul JSON
    # Cum ar fi adăugarea de timestamp-uri sau alte detalii necesare

    return jsonify(predictions.tolist())


if __name__ == '__main__':
    app.run(debug=True)
