import pandas as pd
import matplotlib.pyplot as plt
import os

def generate_bar_charts(file_path, output_directory='static/images'):
    # Verifică dacă directorul de ieșire există și, dacă nu, îl creează
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Încarcă datele din fișierul CSV
    data = pd.read_csv(file_path)

    diseases = data['Disease']
    temp1 = data['Air Temperature [°C]']
    temp2 = data['Unnamed: 2']  # Ajustează denumirea coloanei corespunzător
    hum1 = data['AirHumidity [%rh]']
    hum2 = data['Unnamed: 4']

    # Crează graficul pentru temperatura
    fig, ax1 = plt.subplots(figsize=(10, 6))
    bar_width = 0.35
    opacity = 0.8

    # Bara pentru temperatura 1
    rects1 = ax1.bar([x - bar_width/2 for x in range(len(diseases))], temp1, bar_width, alpha=opacity, color='b', label='Temperature 1 [°C]')

    # Bara pentru temperatura 2
    rects2 = ax1.bar([x + bar_width/2 for x in range(len(diseases))], temp2, bar_width, alpha=opacity, color='g', label='Temperature 2 [°C]')

    ax1.set_xlabel('Disease')
    ax1.set_ylabel('Temperature [°C]')
    ax1.set_title('Temperature for Different Diseases')
    ax1.set_xticks(range(len(diseases)))
    ax1.set_xticklabels(diseases)
    ax1.legend()

    # Salvează primul grafic
    temp_chart_path = os.path.join(output_directory, 'temp_chart.png')
    plt.tight_layout()
    plt.savefig(temp_chart_path)
    plt.close()

    # Crează graficul pentru umiditate
    fig, ax2 = plt.subplots(figsize=(10, 6))

    # Bara pentru umiditate 1
    rects3 = ax2.bar([x - bar_width/2 for x in range(len(diseases))], hum1, bar_width, alpha=opacity, color='b', label='Humidity 1 [%rh]')

    # Bara pentru umiditate 2
    rects4 = ax2.bar([x + bar_width/2 for x in range(len(diseases))], hum2, bar_width, alpha=opacity, color='g', label='Humidity 2 [%rh]')

    ax2.set_xlabel('Disease')
    ax2.set_ylabel('Humidity [%rh]')
    ax2.set_title('Humidity for Different Diseases')
    ax2.set_xticks(range(len(diseases)))
    ax2.set_xticklabels(diseases)
    ax2.legend()

    # Salvează al doilea grafic
    hum_chart_path = os.path.join(output_directory, 'hum_chart.png')
    plt.tight_layout()
    plt.savefig(hum_chart_path)
    plt.close()

    return temp_chart_path, hum_chart_path


if __name__ == '__main__':
    generate_bar_charts("Disease.csv")