TASK 1 EXPLANATION: IoT SENSOR DATA PIPELINE

File Content = Given a file "lorawan_uplink_devices.csv" full of sensor readings (Temperature, Humidity, Signal Strength). 

Task be Done = I need to find broken devices, hot devices, and duplicate signals.

Command : python task1_pipeline.py

STEP INVOLVED IN CALCULATION

1. Connect
It connects to the local MongoDB server we set up.

2. Clean
- Reads the CSV file using Pandas.
- Converts the text timestamps into real Date objects.
- Saves all 5,000+ rows into the MongoDB database.

3. Analyze
- Top Devices: It counts how many times each device appears to see which are most active.
- Weak Signals: It looks at the Signal Strength (RSSI). We sort by the lowest numbers (like -120) to find devices that are barely connecting.
- Duplicates: It finds any device ID that appears more than once, which might indicate a configuration error.

4. Export
It filters for all sensors reporting temperatures above 35 C and saves them to a separate JSON file.

RESULTS : 
- Found about 100 devices that were sending duplicate messages.
- Found 1,305 alerts where the temperature was dangerously high (over 35 C).
- Found the device with the weakest signal was "device-2580".

SCHEDULING CRON JOB = To make this run automatically every day at 2:00 AM, you would use this Cron Job setting:

- 0 2 * * * python /path/to/task1_pipeline.py
- This means: 0th Minute, 2nd Hour, Every Day, Month, and Week
