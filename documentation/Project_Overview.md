PROJECT OVERVIEW AND SETUP GUIDE

1. PROJECT SUMMARY
This project involves setting up a data engineering and analytics environment using Python and MongoDB. The goal is to ingest raw CSV data (IoT sensor logs and E-commerce orders), store it in a NoSQL database (MongoDB), and perform complex analytical queries to derive business insights.

2. TECHNOLOGY STACK
- Python: Used for data manipulation and scripting the logic.
- MongoDB: A NoSQL database used to store flexible data.
- Pandas: A Python library for efficient data loading.
- PyMongo: The library that allows Python to speak to MongoDB.

3. INSTALLATION METHOD (WINDOWS)
As we are running on a Windows environment and wanted to keep everything contained within one folder (without modifying system-wide settings), we used a "Portable" setup.
- We downloaded the ZIP version of MongoDB.
- We extracted it directly into this project folder ("mongodb").
- We configured it to save all data to a local folder ("mongodb_data").

4. COMPLETE COMMAND HISTORY (STEP-BY-STEP)
These are the exact commands used to set up the environment, install dependencies, and run the analysis.

PRE-REQUISITES
- Ensure Python is installed on your system.
- Open a Terminal (Command Prompt or PowerShell) in the "Assignment" folder.

STEP 1: INSTALL DEPENDENCIES
Command : pip install pandas pymongo

STEP 2 : SETUP MONGODB (AUTOMATED)
Command : python setup_mongo.py

STEP 3 : START THE DATABASE SERVER
Command : .\mongodb\bin\mongod.exe --dbpath .\mongodb_data --bind_ip 127.0.0.1

STEP 4 : EXECUTE TASK 1 (IoT PIPELINE)
Command : python task1_pipeline.py

STEP 5: EXECUTE TASK 2 (SALES ANALYTICS)
Command : python task2_analysis.py

---------------------------------------------------

5. PROJECT SKELETON (FOLDER STRUCTURE)

Assignment/
│   
├── mongodb/                    [Database Server Binaries]
├── mongodb_data/               [Database Storage Folder]
├── Results/                    [Generated Outputs]
│   ├── task1_output.txt
│   ├── task2_output.txt
│   └── high_temp_devices.json
│
├── documentation/              [Project Documentation]
│   ├── Project_Overview.md
│   ├── Task1_LoRaWAN_Solution.md
│   └── Task2_Ecommerce_Solution.md
│
├── setup_mongo.py              [Setup Script]
├── setup_project.bat           [One-Click Run Script]
├── task1_pipeline.py           [Python Code for Task 1]
├── task2_analysis.py           [Python Code for Task 2]
│
├── lorawan_uplink_devices.csv  [Input Data Task 1]
├── orders.csv                  [Input Data Task 2]
└── Task 1.pdf                  [Requirements]

---------------------------------------------------

6. DETAILED FOLDER EXPLANATION

Here is why each folder exists and when it was created.

[mongodb]
- Created: During Step 2 (setup_mongo.py).
- Explanation : This contains the actual "mongod.exe" program (the Database Server). We needed it because we could not use the standard Windows Installer active on this machine.

[mongodb_data]
- Created: During Step 2 (setup_mongo.py).
- Explanation : This is the storage folder for the database. When you run MongoDB, it needs a place to save the actual data on your hard drive. If you delete this, your database becomes empty.

[documentation]
- Created: Manually during development.
- Explanation : To keep all "ReadMe" files and guides in one clean place, separating them from the code.

[Results]
- Created: Automatically when you run Task 1 or Task 2 scripts.
- Explanation : To keep the output files separate from the code. This ensures we know exactly which files are "generated" and which are "source code".

[setup_mongo.py]
- Created: At the start of the project.
- Explanation : To automate the downloading of MongoDB so you don't have to manually go to a website, download a zip, and unzip it.

[task1_pipeline.py]
- Created: To solve Task 1.
- Explanation : Ideally, we separate logic into files. This file handles all IoT data cleaning and analysis.

[task2_analysis.py]
- Created: To solve Task 2.
- Explanation : This file handles all E-commerce sales analysis.

7. WHERE TO FIND RESULTS
After running the scripts, open the "Results" folder.
- task1_output.txt: Shows the top devices and signal analysis.
- high_temp_devices.json: The exported list of overheating sensors.
- task2_output.txt: Shows the sales revenue and growth reports.

8. DATA EXTRACTION & INGESTION DETAILS
To bridge the gap between raw CSV files and the MongoDB NoSQL database, we implemented a custom ETL (Extract, Transform, Load) process within our python scripts (`task1_pipeline.py` and `task2_analysis.py`).

Explanation : 

a. Extraction :
   - We utilize the `pandas` library to read the `.csv` files.
   - For `orders.csv`, we specifically handle encoding (checking 'utf-8' and falling back to 'cp1252') to avoid errors with special characters.

b. Transformation :
   - Dates are parsed using `pd.to_datetime` to ensure MongoDB recognizes them as actual Date objects, enabling powerful time-based queries (like grouping by month/year).
   - Numeric fields (like "Sales") are cleaned and converted using `pd.to_numeric` to prevent string math errors.
   - The Pandas DataFrame is then converted to a native Python dictionary format using `df.to_dict(orient='records')`.

c. Loading :
   - We use the `pymongo` library to establish a connection.
   - The data is inserted in bulk using `collection.insert_many(records)` for efficiency.
   - Before insertion, we run `collection.delete_many({})` to ensure the collection is clean and prevent duplicate entries if the script is run multiple times.

9. MONGODB CONNECTION DETAILS
Since the database is hosted locally within this project folder (Portable Mode), no complex authentication is required for this development environment.

- Host : `localhost` (or `127.0.0.1`)
- Port : `27017`
- Protocol : `mongodb://`
- Connection URI : `mongodb://localhost:27017/`
- Authentication : None (No username or password required by default for this local setup)
- username:password : for server side.

