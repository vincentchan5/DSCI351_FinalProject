import pandas as pd
from pymongo import MongoClient
from pathlib import Path

df = pd.read_csv("../db/NBA Stats 202324 All Stats  NBA Player Props Tool (4).csv")


percent_fields = ["USG%", "TO%", "FT%", "2P%", "3P%", "eFG%", "TS%"]
stat_fields = [
    "AGE", "GP", "MPG", "PPG", "RPG", "APG", "SPG", "BPG", "TPG",
    "P+R", "P+A", "P+R+A", "VI", "ORtg", "DRtg"
]

for col in percent_fields:
    if col in df.columns:
        df[col] = df[col].astype(str).str.replace('%', '', regex=False)
        df[col] = pd.to_numeric(df[col], errors='coerce')

for col in stat_fields:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')

client = MongoClient("mongodb://localhost:27017/")
db = client["chatdb"]
collection = db["players"]

collection.delete_many({})

records = df.to_dict(orient="records")
collection.insert_many(records)

print(f"✅ NBA player stats loaded into MongoDB! {len(records)} records inserted.")
print("📄 Sample player:", records[0])