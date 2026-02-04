import pandas as pd
from pymongo import MongoClient
import json
import os

MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "lorawan_db"
COLLECTION_NAME = "uplinks"
CSV_FILE = "lorawan_uplink_devices.csv"
RESULTS_DIR = "Results"

def connect_db():
    client = MongoClient(MONGO_URI)
    return client[DB_NAME]

def ingest_data(db, log_file):
    if not os.path.exists(CSV_FILE):
        log_file.write(f"File {CSV_FILE} not found.\n")
        return

    # Load CSV
    df = pd.read_csv(CSV_FILE)
    
    # Convert timestamp to datetime
    if 'timestamp' in df.columns:
        df['timestamp'] = pd.to_datetime(df['timestamp'])

    # Convert to dictionary records
    records = df.to_dict(orient='records')
    
    # Insert
    collection = db[COLLECTION_NAME]

    # Clear existing to avoid duplicates on re-run
    collection.delete_many({})
    collection.insert_many(records)
    log_file.write(f"Inserted {len(records)} records into '{COLLECTION_NAME}'.\n")

def analyze_data(db, log_file):
    collection = db[COLLECTION_NAME]

    log_file.write("\n--- 1. Top 10 devices with highest number of uplinks ---\n")
    pipeline_top_devices = [
        {"$group": {"_id": "$device_id", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ]
    for doc in collection.aggregate(pipeline_top_devices):
        log_file.write(f"Device: {doc['_id']}, Uplinks: {doc['count']}\n")

    log_file.write("\n--- 2. Average RSSI and SNR per device (Sorted by lowest RSSI) ---\n")
    pipeline_rssi = [
        {"$group": {
            "_id": "$device_id", 
            "avg_rssi": {"$avg": "$rssi"},
            "avg_snr": {"$avg": "$snr"}
        }},
        {"$sort": {"avg_rssi": 1}}
    ]

    # Limiting output for readability
    for i, doc in enumerate(collection.aggregate(pipeline_rssi)):
        if i < 5: # Show top 5 weak connections
            log_file.write(f"Device: {doc['_id']}, Avg RSSI: {doc['avg_rssi']:.2f}, Avg SNR: {doc['avg_snr']:.2f}\n")

    log_file.write("\n--- 3. Average Temperature and Humidity per Gateway ---\n")
    pipeline_gateway = [
        {"$group": {
            "_id": "$gateway_id", 
            "avg_temp": {"$avg": "$temperature"},
            "avg_humidity": {"$avg": "$humidity"}
        }}
    ]
    for doc in collection.aggregate(pipeline_gateway):
         log_file.write(f"Gateway: {doc['_id']}, Avg Temp: {doc['avg_temp']:.2f}, Avg Humidity: {doc['avg_humidity']:.2f}\n")

    log_file.write("\n--- 4. Device IDs with more than one record ---\n")
    pipeline_duplicates = [
        {"$group": {"_id": "$device_id", "count": {"$sum": 1}}},
        {"$match": {"count": {"$gt": 1}}}
    ]

    # Count how many duplicates
    duplicates = list(collection.aggregate(pipeline_duplicates))
    log_file.write(f"Found {len(duplicates)} duplicate devices.\n")
    
    # Show first few
    for i, doc in enumerate(duplicates):
        if i < 5:
            log_file.write(f"Duplicate Device: {doc['_id']} (Count: {doc['count']})\n")

    log_file.write("\n--- 5. Export JSON for Temperature > 35C ---\n")
    query = {"temperature": {"$gt": 35}}
    projection = {"_id": 0, "device_id": 1, "latitude": 1, "longitude": 1, "temperature": 1}
    
    high_temp_records = list(collection.find(query, projection))
    
    output_json_path = os.path.join(RESULTS_DIR, "high_temp_devices.json")
    with open(output_json_path, "w") as f:
        json.dump(high_temp_records, f, indent=4)
    log_file.write(f"Exported {len(high_temp_records)} records to {output_json_path}\n")

if __name__ == "__main__":
    # Ensure results directory exists
    if not os.path.exists(RESULTS_DIR):
        os.makedirs(RESULTS_DIR)

    output_txt_path = os.path.join(RESULTS_DIR, "task1_output.txt")
    print(f"Running Task 1... Output will be saved to {output_txt_path}")
    
    with open(output_txt_path, "w") as log_file:
        db = connect_db()
        ingest_data(db, log_file)
        analyze_data(db, log_file)
    
    print("Task 1 Completed.")
