import pandas as pd
from pymongo import MongoClient
import os

# Configuration
MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "ecommerce_db"
COLLECTION_NAME = "orders"
CSV_FILE = "orders.csv"
RESULTS_DIR = "Results"

def connect_db():
    client = MongoClient(MONGO_URI)
    return client[DB_NAME]

def ingest_data(db, log_file):
    log_file.write("Loading data...\n")
    try:
        # Load CSV, encoding might be 'cp1252' or 'utf-8'
        try:
            df = pd.read_csv(CSV_FILE, encoding='utf-8')
        except UnicodeDecodeError:
            df = pd.read_csv(CSV_FILE, encoding='cp1252')

        # Convert Order Date
        df['Order Date'] = pd.to_datetime(df['Order Date'], dayfirst=True)
        
        # Ensure Sales is numeric
        df['Sales'] = pd.to_numeric(df['Sales'], errors='coerce')

        records = df.to_dict(orient='records')
        
        collection = db[COLLECTION_NAME]
        collection.delete_many({}) # Clear existing
        collection.insert_many(records)
        log_file.write(f"Inserted {len(records)} records into '{COLLECTION_NAME}'.\n")
    except Exception as e:
        log_file.write(f"Error ingesting data: {e}\n")

def run_analytics(db, log_file):
    collection = db[COLLECTION_NAME]
    
    log_file.write("\n--- 1. Top 5 Products by Total Sales ---\n")
    pipeline_top_products = [
        {"$group": {"_id": "$Product ID", "total_sales": {"$sum": "$Sales"}}},
        {"$sort": {"total_sales": -1}},
        {"$limit": 5}
    ]
    for doc in collection.aggregate(pipeline_top_products):
        log_file.write(f"Product ID: {doc['_id']}, Total Sales: ${doc['total_sales']:,.2f}\n")

    log_file.write("\n--- 2. Total Revenue per Month (Year-Month) ---\n")
    pipeline_monthly_revenue = [
        {"$group": {
            "_id": {
                "year": {"$year": "$Order Date"},
                "month": {"$month": "$Order Date"}
            },
            "total_revenue": {"$sum": "$Sales"}
        }},
        {"$sort": {"_id.year": 1, "_id.month": 1}}
    ]
    
    # Just showing first 10 for brevity in output
    monthly_results = list(collection.aggregate(pipeline_monthly_revenue))
    for i, doc in enumerate(monthly_results):
        if i < 10: 
            log_file.write(f"{doc['_id']['year']}-{doc['_id']['month']:02d}: ${doc['total_revenue']:,.2f}\n")
    log_file.write(f"... (Total {len(monthly_results)} months)\n")


    log_file.write("\n--- 3. Average Sales per Sub-Category (Grouped by Category) ---\n")
    pipeline_category = [
        {"$group": {
            "_id": {
                "category": "$Category",
                "sub_category": "$Sub-Category"
            },
            "avg_sales": {"$avg": "$Sales"}
        }},
        {"$group": {
             "_id": "$_id.category",
             "sub_categories": {
                 "$push": {
                     "sub_category": "$_id.sub_category",
                     "avg_sales": "$avg_sales"
                 }
             }
        }}
    ]
    
    for doc in collection.aggregate(pipeline_category):
        log_file.write(f"\nCategory: {doc['_id']}\n")
        for sub in doc['sub_categories']:
            log_file.write(f"  - {sub['sub_category']}: ${sub['avg_sales']:,.2f}\n")

    log_file.write("\n--- 4. Yearly Sales Growth ---\n")
    pipeline_growth = [
        {"$group": {
            "_id": {"$year": "$Order Date"},
            "total_sales": {"$sum": "$Sales"}
        }},
        {"$sort": {"_id": 1}}
    ]
    
    yearly_data = list(collection.aggregate(pipeline_growth))
    
    log_file.write(f"{'Year':<6} | {'Total Sales':<15} | {'Growth %':<10}\n")
    log_file.write("-" * 35 + "\n")
    
    prev_sales = 0
    for doc in yearly_data:
        year = doc['_id']
        sales = doc['total_sales']
        growth = 0
        if prev_sales > 0:
            growth = ((sales - prev_sales) / prev_sales) * 100
            growth_str = f"{growth:+.2f}%"
        else:
            growth_str = "N/A"
        
        log_file.write(f"{year:<6} | ${sales:,.2f}    | {growth_str:<10}\n")
        prev_sales = sales

if __name__ == "__main__":
    # Ensure results directory exists
    if not os.path.exists(RESULTS_DIR):
        os.makedirs(RESULTS_DIR)

    output_txt_path = os.path.join(RESULTS_DIR, "task2_output.txt")
    print(f"Running Task 2... Output will be saved to {output_txt_path}")
    
    with open(output_txt_path, "w") as log_file:
        db = connect_db()
        ingest_data(db, log_file)
        run_analytics(db, log_file)
    
    print("Task 2 Completed.")
