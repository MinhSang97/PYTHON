import shutil
import os
import time

def copy_and_replace(source_path, destination_path):
    try:
        shutil.copy2(source_path, destination_path)
        print(f"File copied from {source_path} to {destination_path}")
    except FileNotFoundError:
        print(f"File not found: {source_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    source_file = r"C:\Windows\System32\data_cache.json"
    destination_folder = r"C:\Users\Administrator\Desktop\API\API_TESTTODAY"
    destination_file = os.path.join(destination_folder, "data_cache.json")

    while True:
        copy_and_replace(source_file, destination_file)
        time.sleep(300)  # Sleep for 5 minutes (300 seconds)

if __name__ == "__main__":
    main()
