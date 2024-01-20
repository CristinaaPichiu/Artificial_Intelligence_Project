import pickle

import joblib
import pandas as pd
from flask import Flask, render_template, request, redirect, url_for
from prophet_file import return_path_prophet
from seq2seq import return_pathSeq2Seq
from retele_neuronale import return_path_RN

model = joblib.load('model_rosii_bolnave.pkl')
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/models')
def models():
    return render_template('models.html')


@app.route('/prediction')
def prediction():
    return render_template('prediction.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Collect form data
    input_data = {
        'Affected Part': request.form.get('AffectedPart'),
        'Intensity': request.form.get('Intensity'),
        'Texture': request.form.get('Texture'),
        'Color': request.form.get('Color'),
        'Pattern': request.form.get('Pattern'),
        'Anatomical Region': request.form.get('AnatomicalRegion'),
        'Shape': request.form.get('Shape'),
        'Border Color': request.form.get('BorderColor')
    }

    print("Received a POST request")

    # Convert form data to DataFrame
    df = pd.DataFrame([input_data])

    # Predict using the model
    prediction = model.predict(df)

    # Set variables for template rendering
    selected_attributes = input_data
    disease = 'Există un risc ridicat de boală la roșii.' if prediction == 1 else 'Riscul de boală la roșii este scăzut.'

    # Render the template with the variables
    return render_template('prediction.html', selected_attributes=selected_attributes, disease=disease)


@app.route('/disease')
def diseases():
    return render_template('disease.html')


# Functie pentru afisarea graficelelor pt diseases:
@app.route('/generate_plot_disease', methods=['POST'])
def generate_plot_disease():
    plot_type = request.form['plot_type']
    image_path = "images/" + f'{plot_type}_chart.png'
    return render_template('image.html', image_path=image_path)


# Aici sunt functiile pentru models:
@app.route('/generate_plot', methods=['POST'])
def generate_plot():
    plot_type = request.form['plot_type']

    if plot_type == 'Prophet':
        parameter_type = request.form['parameter_type']
        return redirect(url_for('show_chart_prophet', parameter_type=parameter_type))
    elif plot_type == 'RN':
        parameter_type = request.form['parameter_type']
        return redirect(url_for('show_chart_RN', parameter_type=parameter_type))
    elif plot_type == 'Seq2Seq':
        parameter_type = request.form['parameter_type']
        return redirect(url_for('show_chart_Seq2Seq', parameter_type=parameter_type))

    return redirect(url_for('models'))


@app.route('/show_chart_RN/<parameter_type>', methods=['GET'])
def show_chart_RN(parameter_type):
    image_path = "images/" + return_path_RN(parameter_type)
    print(image_path)
    return render_template('image.html', image_path=image_path)


@app.route('/show_chart_Seq2Seq/<parameter_type>', methods=['GET'])
def show_chart_Seq2Seq(parameter_type):
    image_path = "images/"+return_pathSeq2Seq(parameter_type)
    print(image_path)
    return render_template('image.html', image_path=image_path)


@app.route('/show_chart_prophet/<parameter_type>', methods=['GET'])
def show_chart_prophet(parameter_type):
    image_path = "images/"+return_path_prophet(parameter_type)
    print(image_path)
    return render_template('image.html', image_path=image_path)


if __name__ == '__main__':
    app.run(debug=True)

