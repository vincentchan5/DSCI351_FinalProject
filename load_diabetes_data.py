import pandas as pd
import pymysql
from pathlib import Path

base_dir = Path(__file__).resolve().parents[1]
csv_path = base_dir / "data" / "Healthcare-Diabetes.csv"

df = pd.read_csv(csv_path)

df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

expected_columns = [
    "Pregnancies", "Glucose", "BloodPressure", "SkinThickness",
    "Insulin", "BMI", "DiabetesPedigreeFunction", "Age", "Outcome"
]

missing_cols = set(expected_columns) - set(df.columns)
if missing_cols:
    raise ValueError(f"Missing columns in CSV: {missing_cols}")

df = df[expected_columns]

print("CSV loaded successfully!")
print("Shape:", df.shape)
print("Columns:", df.columns.tolist())

conn = pymysql.connect(
    host="localhost",
    user="root",
    password="dsci-351",
    database="chatdb"
)

cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS diabetes (
        id INT AUTO_INCREMENT PRIMARY KEY,
        Pregnancies INT,
        Glucose INT,
        BloodPressure INT,
        SkinThickness INT,
        Insulin INT,
        BMI FLOAT,
        DiabetesPedigreeFunction FLOAT,
        Age INT,
        Outcome INT
    );
""")

for _, row in df.iterrows():
    values = row.tolist()
    cursor.execute("""
        INSERT INTO diabetes (
            Pregnancies, Glucose, BloodPressure, SkinThickness,
            Insulin, BMI, DiabetesPedigreeFunction, Age, Outcome
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, values)

conn.commit()
conn.close()

print("Diabetes data loaded into MySQL successfully!")
