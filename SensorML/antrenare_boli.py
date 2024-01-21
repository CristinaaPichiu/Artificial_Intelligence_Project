import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib
import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler, OneHotEncoder

# Citirea fișierului CSV
df = pd.read_csv('boli_simptome.csv')

# Afișarea primelor rânduri pentru a înțelege structura datelor
df.head()

# Prelucrarea datelor
# Înlocuirea valorilor lipsă cu 'Unknown' pentru coloanele textuale și cu mediana pentru coloanele numerice
df.fillna('Unknown', inplace=True)
# Inițializarea LabelEncoder pentru coloana țintă
label_encoder = LabelEncoder()
# Codificarea coloanei țintă
y = label_encoder.fit_transform(df['Disease'])
print(y)

# Separarea caracteristicilor de intrare și a etichetelor
X = df.drop('Disease', axis=1)
text_columns = X.select_dtypes(include=['object']).columns
numeric_columns = X.select_dtypes(exclude=['object']).columns

# Construirea preprocesorului cu OneHotEncoder pentru coloanele textuale și StandardScaler pentru cele numerice
preprocessor = ColumnTransformer(transformers=[
    ('num', StandardScaler(), numeric_columns),
    ('cat', OneHotEncoder(handle_unknown='ignore'), text_columns)
])

# Crearea pipeline-ului care include preprocesorul și modelul RandomForestClassifier
model_pipeline = Pipeline([
    ('preprocessor', preprocessor),
    ('classifier', RandomForestClassifier(random_state=42))
])

# Împărțirea datelor în seturi de antrenare și test
# Împărțirea datelor în seturi de antrenare și test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Antrenarea modelului
model_pipeline.fit(X_train, y_train)

# Evaluarea modelului
y_pred = model_pipeline.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy}")

# Salvarea modelului în format pkl
joblib.dump(model_pipeline, 'model_rosii_bolnave.pkl')