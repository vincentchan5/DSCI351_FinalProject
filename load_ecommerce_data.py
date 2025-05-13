import json
from pymongo import MongoClient
from pathlib import Path

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["chatdb"]
collection = db["ecommerce"]

# Load JSON from data folder
json_path = Path(__file__).resolve().parents[1] / "data" / "E-Commerce.json"

with open(json_path) as f:
    data = json.load(f)

# Optional: unwrap if nested
if isinstance(data, dict) and "data" in data:
    data = data["data"]

# Print preview
if isinstance(data, list):
    print("JSON is a list. Sample doc:", data[0])
else:
    print("JSON not a list. Inserting raw object.")
    data = [data]  # Wrap as single doc

# Insert into MongoDB
collection.delete_many({})  # Optional: clear old records
collection.insert_many(data)

print(f"Loaded {len(data)} records into 'ecommerce' collection!")
