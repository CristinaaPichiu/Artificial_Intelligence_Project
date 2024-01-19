from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from prophet import Prophet
from prophet.diagnostics import cross_validation, performance_metrics
import base64
from io import BytesIO

app = Flask(__name__)


def load_and_clean_data(file_path):
    # Încărcăm setul de date
    df = pd.read_csv(file_path, parse_dates=['Timestamp'], dayfirst=False)

    # Eliminăm punctele și spațiile din numerele cu virgulă mobilă
    df.replace(regex=True, inplace=True, to_replace=[r'\.', r' '], value='')
    # print(df)
    numeric_columns = ['pres', 'temp1', 'umid', 'temp2', 'V450', 'B500', 'G550', 'Y570', 'O600', 'R650', 'temps1',
                       'temps2', 'lumina']
    df[numeric_columns] = df[numeric_columns].replace(',', '', regex=True).astype(float)

    # print(df[numeric_columns])
    # Convertim coloana Timestamp în format dată
    df['Timestamp'] = pd.to_datetime(df['Timestamp'], format='%Y-%m-%d %H:%M:%S',
                                     errors='coerce')

    # Eliminăm rândurile care au valori nule în orice coloană
    df = df.dropna(how='any')

    # Conversia datelor la tip numeric
    df = df.apply(pd.to_numeric, errors='coerce')
    return df


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
    file_path = 'SensorML_small.csv'
    df = load_and_clean_data(file_path)
    return render_template('index.html')
@app.route('/generate_plot', methods=['POST'])
def generate_plot():
    file_path = 'SensorML_small.csv'
    df = load_and_clean_data(file_path)

    model_selected = request.form['model']  # This is the new part where you capture the selected model
    plot_type = request.form['plot_type']

    # Based on the selected model, you could adjust your data processing or plotting logic
    #if model_selected == 'static':
        # Apply static model logic here
    #elif model_selected == 'neural':
        # Apply neural network logic here
    #elif model_selected == 'seq2seq':
        # Apply Seq2Seq model logic here

    # Now, based on the plot type, you generate the plot
    # if plot_type == 'heatmap':
        # Assuming you have a function to handle heatmap for different models
        #img = generate_heatmap_based_on_model(df, model_selected)
       ## return render_template('image.html', image_data=img)
    #elif plot_type == 'line':
        # Assuming you have a function to handle line chart for different models
        #img = generate_line_chart_based_on_model(df, model_selected)
    # return render_template('image.html', image_data=img)

    # Handle other plot types if necessary

    return redirect(url_for('index'))

@app.route('/show_chart', methods=['GET'])
def show_chart():
    # Aici poți genera graficul sau orice altă logică specifică pentru afișarea graficului
    file_path = 'SensorML_small.csv'
    df = load_and_clean_data(file_path)
    img = plot_mean_heatmaps(df)
    return render_template('image.html', image_data=img)


@app.route('/show_line_chart', methods=['GET'])
def show_line_chart():
    # Aici poți genera graficul de tip linie sau orice altă logică specifică
    file_path = 'SensorML_small.csv'
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
