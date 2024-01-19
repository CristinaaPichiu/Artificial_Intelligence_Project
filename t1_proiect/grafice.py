import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from prophet import Prophet
from prophet.diagnostics import cross_validation, performance_metrics

def load_and_clean_data(file_path):
    # Încărcăm setul de date
    df = pd.read_csv(file_path, parse_dates=['Timestamp'], dayfirst=False)

    # Eliminăm punctele și spațiile din numerele cu virgulă mobilă
    df.replace(regex=True, inplace=True, to_replace=[r'\.', r' '], value='')
    #print(df)
    numeric_columns = ['pres', 'temp1', 'umid', 'temp2', 'V450', 'B500', 'G550', 'Y570', 'O600', 'R650', 'temps1',
                       'temps2', 'lumina']
    df[numeric_columns] = df[numeric_columns].replace(',', '', regex=True).astype(float)

    #print(df[numeric_columns])
    # Convertim coloana Timestamp în format dată
    df['Timestamp'] = pd.to_datetime(df['Timestamp'], format='%Y-%m-%d %H:%M:%S', errors='coerce')#########################

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
    # Crearea unui heatmap                                                                                          simplu pentru valorile din dataframe
    plt.figure(figsize=(12, 8))
    sns.heatmap(df.corr(), annot=True, cmap='coolwarm')
    plt.title('Heatmap pentru corelația dintre variabile')
    plt.show()


def plot_median_heatmaps(df):
    # Verificare dacă dataframe-ul conține date valide
    if df.empty:
        print("Nu există date valide pentru afișarea heatmap-ului.")
        return

    # Eliminarea coloana 'Timestamp' pentru a asigura doar date numerice
    df_numeric = df.drop(['Timestamp'], axis=1)

    # Verificare și conversie la tip datetime
    if not pd.api.types.is_datetime64_any_dtype(df['Timestamp']):
        df['Timestamp'] = pd.to_datetime(df['Timestamp'], errors='coerce')


    # Eliminarea rândurilor care conțin NaN
    df_numeric = df_numeric.dropna()


    # Crearea unui heatmap pentru valorile mediane pe zi
    median_heatmap = df_numeric.groupby(df['Timestamp'].dt.date).median()

    print(median_heatmap.corr())
    # Ajustarea dimensiunii figurii pentru a evita suprapunerea valorilor
    plt.figure(figsize=(14, 10))

    # Crearea heatmap-ului cu anotări și formatarea valorilor
    sns.heatmap(median_heatmap.corr(), annot=True, cmap='coolwarm', annot_kws={"size": 8})

    # Ajustarea etichetelor axelor
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)

    plt.title('Heatmap pentru valorile mediane pe zi')
    plt.show()


def plot_boxplots(df):
    # Crearea boxplot-urilor pentru identificarea outlierelor și distribuției valorilor
    plt.figure(figsize=(16, 10))
    sns.boxplot(data=df.drop(['Timestamp'], axis=1), palette='pastel', showfliers=False)
    plt.title('Boxplot-uri pentru identificarea outlierelor și a distribuției valorilor')
    plt.xticks(rotation=45)
    plt.show()

def train_prophet_models(df):
    prophet_models = {}
    for parameter in df.columns[1:]:  # Excludem prima coloana 'Timestamp'
        print(parameter)
        # Creearea unui dataframe pentru antrenare
        train_data = df[['Timestamp', parameter]].rename(columns={'Timestamp': 'ds', parameter: 'y'})

        # Converteste timestamp-urile in nanosecunde
        train_data['ds'] = pd.to_datetime(train_data['ds'], unit='ns')

        # Inițializare și antrenare model
        model = Prophet(yearly_seasonality=True, weekly_seasonality=True, daily_seasonality=False)
        model.fit(train_data)
        prophet_models[parameter] = model

        # Crearea unui dataframe pentru predictie
        future = model.make_future_dataframe(periods=48, freq='H')  # 48 de ore înainte
        forecast = model.predict(future)

        # Afișare grafic cu predicțiile
        fig = model.plot(forecast)
        plt.title(f'Prophet Predictions for {parameter}')
        plt.show()

        # Afișare eroare la antrenare utilizând cross-validare
        fig = model.plot_components(forecast)
        plt.show()

    return prophet_models


def plot_actual_vs_predicted(df, forecast, parameter):
    # Realizați grafice care indică valorile predicțiilor realizate de model în paralel cu valorile actuale
    plt.figure(figsize=(16, 6))
    plt.plot(df['Timestamp'], df[parameter], label='Actual', color='blue')
    plt.plot(forecast['ds'], forecast['yhat'], label='Predicted', color='red')
    plt.title(f'Actual vs Predicted for {parameter}')
    plt.xlabel('Timestamp')
    plt.ylabel(parameter)
    plt.legend()
    plt.show()

def perform_cross_validation(model, initial, period, horizon):
    # Specificăm perioada de predictie și frecvența
    initial = str(initial) + ' hours'
    period = str(period) + ' hours'
    horizon = str(horizon) + ' hours'

    # Realizarea cross-validation
    df_cv = cross_validation(model, initial=initial, period=period, horizon=horizon)

    # Afișare erori
    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(111)
    ax.plot(df_cv['ds'], df_cv['y'], label='Actual')
    ax.plot(df_cv['ds'], df_cv['yhat'], label='Predicted', color='red')
    ax.fill_between(df_cv['ds'], df_cv['yhat_lower'], df_cv['yhat_upper'], color='r', alpha=0.3)
    ax.set_title('Cross-Validation Results')
    ax.set_xlabel('Timestamp')
    ax.set_ylabel('Value')
    plt.legend()
    plt.show()


if __name__ =="__main__":
     file_path = 'SensorML_small.csv'
     df=load_and_clean_data(file_path)
# 1. Heatmaps + Boxplot

     plot_mean_heatmaps(df)

     plot_median_heatmaps(df)
     plot_boxplots(df)

    #
    # # 3. Antrenarea modelelor Prophet
     prophet_models = train_prophet_models(df)
    #
    # # 4. Realizarea predicțiilor și afișarea graficelor
     for parameter, model in prophet_models.items():
         future = model.make_future_dataframe(periods=48, freq='H')
         forecast = model.predict(future)
         plot_actual_vs_predicted(df, forecast, parameter)

     # for parameter, model in prophet_models.items():
     #     perform_cross_validation(model, initial=7*24, period=2*24, horizon=2*24)
     #
