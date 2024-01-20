from flask import Flask, render_template, request, redirect, url_for
from prophet_file import return_path_prophet
from seq2seq import return_pathSeq2Seq
from retele_neuronale import return_path_RN


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


@app.route('/disease')
def diseases():
    return re   nder_template('disease.html')


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

