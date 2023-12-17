import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns

# Importați datele
df = pd.read_csv("SensorML_small.csv")

# Histograme
for col in df.columns:
    plt.figure(figsize=(10, 6))
    plt.hist(df[col], label=col)
    plt.title(f"Distribuția {col}")
    plt.legend()
    plt.show()

# Boxploturi
for col in df.columns:
    plt.figure(figsize=(10, 6))
    plt.boxplot(df[col])
    plt.xlabel(col)
    plt.ylabel("Valoare")
    plt.show()

# Heatmap-uri
for col in df.columns:
    fig = px.imshow(
        df.groupby("Timestamp")[col].mean().to_numpy(),
        color_continuous_scale="viridis",
    )
    fig.update_layout(title=f"{col} pe parcursul zilei")
    fig.show()

# Calculați matricea de corelație
corr = df.corr()

# Afișați matricea de corelație
fig = sns.heatmap(
    corr,
    vmin=-1,
    vmax=1,
    annot=True,
    cmap="Reds",
    linewidths=0.5,
    linecolor="white",
)
fig.set_title("Matricea de corelație")
fig.show()

# Creați modelul Prophet
from prophet import Prophet

# Creați modelul Prophet
m = Prophet()

# Antrenați modelul
m.fit(df)

# Creați un dataframe pentru predicții
future = m.make_future_dataframe(periods=48, freq="H")

# Generați predicții
forecast = m.predict(future)

# Plotați predicțiile
fig = m.plot(forecast)
plt.xlabel("Oră")
plt.ylabel("Temperatură")
plt.show()

# Calculați eroarea la antrenare
mse = np.mean((forecast["yhat"] - df["y"])**2)
print("MSE:", mse)
