import os
import urllib.request
import zipfile
import shutil

BASE_DIR = os.getcwd()
MONGO_DIR = os.path.join(BASE_DIR, "mongodb")
DATA_DIR = os.path.join(BASE_DIR, "mongodb_data")

URLS = [
    "https://fastdl.mongodb.org/windows/mongodb-windows-x86_64-7.0.5.zip",
    "https://fastdl.mongodb.org/windows/mongodb-windows-x86_64-6.0.8.zip"
]

def download_file(url, dest):
    print(f"Attempting to download from {url}...")
    try:
        with urllib.request.urlopen(url) as response, open(dest, 'wb') as out_file:
            shutil.copyfileobj(response, out_file)
        print("Download successful.")
        return True
    except Exception as e:
        print(f"Failed to download: {e}")
        return False

def setup():
    # 1. Create Data Directory
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
        print(f"Created data directory: {DATA_DIR}")

    # 2. Download MongoDB
    zip_path = "mongodb.zip"
    if not os.path.exists(MONGO_DIR):
        downloaded = False
        for url in URLS:
            if download_file(url, zip_path):
                downloaded = True
                break
        
        if not downloaded:
            print("Could not download MongoDB. Please check internet connection or URLs.")
            return

        # 3. Extract
        print("Extracting MongoDB...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall("mongodb_temp")
        
        # Move inner folder to proper location
        for item in os.listdir("mongodb_temp"):
            if "mongodb-win" in item:
                shutil.move(os.path.join("mongodb_temp", item), MONGO_DIR)
                break
        
        # Cleanup
        os.remove(zip_path)
        shutil.rmtree("mongodb_temp")
        print("MongoDB extracted successfully.")
    else:
        print("MongoDB is already setup.")

if __name__ == "__main__":
    setup()
