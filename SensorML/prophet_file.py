import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt
import os

def plot_actual_vs_predicted(df, forecast, parameter):
    plt.figure(figsize=(16, 6))
    plt.plot(df['Timestamp'], df[parameter], label='Actual', color='blue')
    plt.plot(forecast['ds'], forecast['yhat'], label='Predicted', color='red')
    plt.title(f'Actual vs Predicted for {parameter}')
    plt.xlabel('Timestamp')
    plt.ylabel(parameter)
    plt.legend()

    file_path = f'static/images/{parameter}_prophet.png'
    plt.savefig(file_path)
    plt.close()

    return file_path

def train_prophet_model_for_parameter(df, parameter):
    # Make sure 'Timestamp' is a datetime column
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])

    # Create a dataframe for training
    train_data = df[['Timestamp', parameter]].rename(columns={'Timestamp': 'ds', parameter: 'y'})

    # Initialize and train the model
    model = Prophet(yearly_seasonality=True, weekly_seasonality=True, daily_seasonality=False)
    model.fit(train_data)

    return model

def return_path_prophet(column):
    directory = 'static/images'
    for filename in os.listdir(directory):
        if filename.startswith(column) and filename.endswith("Prophet.png"):
            return filename

    return None

if __name__ == "__main__":
    file_path = 'SensorMLDataset.csv'
    df = pd.read_csv(file_path)
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])

    parameters = ['pres', 'temp1', 'umid', 'temp2', 'V450', 'B500', 'G550', 'Y570', 'O600', 'R650', 'temps1', 'temps2', 'lumina']
    prophet_models = {}
    for parameter in parameters:
        prophet_models[parameter] = train_prophet_model_for_parameter(df, parameter)

    for parameter, model in prophet_models.items():
        future = model.make_future_dataframe(periods=48, freq='H')
        forecast = model.predict(future)
        plot_actual_vs_predicted(df, forecast, parameter)
