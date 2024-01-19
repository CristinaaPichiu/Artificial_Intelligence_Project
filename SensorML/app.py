from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from SensorML.prophet_file import return_path_prophet
from SensorML.seq2seq import function_Seq2Seq, return_pathSeq2Seq
from read_csv import load_and_clean_data
from retele_neuronale import function_LSTM, return_path
import base64
from io import BytesIO

app = Flask(__name__)


def plot_mean_heatmaps(df):
    # Verificare dacă dataframe-ul conține date valide
    if df.empty:
        print("Nu există date valide pentru afișarea heatmap-ului.")
        return
    print(df.corr())
    # Crearea unui heatmap simplu pentru valorile din dataframe
    plt.figure(figsize=(12, 8))
    sns.heatmap(df.corr(), annot=True, cmap='coolwarm')
    plt.title('Heatmap pentru corelația dintre variabile')

    buf = BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return f"data:image/png;base64,{data}"


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_plot', methods=['POST'])
def generate_plot():
    file_path = 'SensorMLDataset.csv'
    df = load_and_clean_data(file_path)

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

    # Adaugă aici condiții pentru alte tipuri de grafice

    return redirect(url_for('index'))

@app.route('/show_chart_RN/<parameter_type>', methods=['GET'])
def show_chart_RN(parameter_type):
    file_path = 'SensorMLDataset.csv'
    df = load_and_clean_data(file_path)

    # Apelarea funcției pentru valoarea primită a parameter_type
    image_path = "images/"+return_path(parameter_type)
    print(image_path)
    return render_template('image.html', image_path=image_path)
@app.route('/show_chart_Seq2Seq/<parameter_type>', methods=['GET'])
def show_chart_Seq2Seq(parameter_type):
    file_path = 'SensorMLDataset.csv'
    df = load_and_clean_data(file_path)
    # Apelarea funcției pentru valoarea primită a parameter_type în contextul Seq2Seq
    image_path = "images/"+return_pathSeq2Seq(parameter_type)
    print(image_path)
    return render_template('image.html', image_path=image_path)

@app.route('/show_chart_prophet/<parameter_type>', methods=['GET'])
def show_chart_prophet(parameter_type):
    file_path = 'SensorMLDataset.csv'
    df = load_and_clean_data(file_path)
    # Apelarea funcției pentru valoarea primită a parameter_type în contextul Seq2Seq
    image_path = "images/"+return_path_prophet(parameter_type)
    print(image_path)
    return render_template('image.html', image_path=image_path)



@app.route('/show_chart', methods=['GET'])
def show_chart():
    # Aici poți genera graficul sau orice altă logică specifică pentru afișarea graficului
    file_path = 'SensorMLDataset.csv'
    df = load_and_clean_data(file_path)
    img = plot_mean_heatmaps(df)
    return render_template('image.html', image_data=img)


@app.route('/show_line_chart', methods=['GET'])
def show_line_chart():
    # Aici poți genera graficul de tip linie sau orice altă logică specifică
    file_path = 'SensorMLDataset.csv'
    df = load_and_clean_data(file_path)
    img = generate_line_chart(df)
    return render_template('image.html', image_data=img)


def generate_line_chart(df):
    # Implementează logica pentru generarea graficului de tip linie
    # Poți utiliza biblioteca matplotlib/seaborn sau oricare altă bibliotecă
    # Returnează imaginea generată sub formă de data URL
    plt.figure(figsize=(12, 8))
    plt.plot(df['Timestamp'], df['temp1'], label='Temperature 1', marker='o')
    plt.plot(df['Timestamp'], df['temp2'], label='Temperature 2', marker='o')
    plt.title('Line Chart for Temperatures over Time')
    plt.xlabel('Timestamp')
    plt.ylabel('Temperature')
    plt.legend()

    buf = BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    data = base64.b64encode(buf.getbuffer()).decode("ascii")

    return f"data:image/png;base64,{data}"

if __name__ == '__main__':
    app.run(debug=True)

