import os
import requests

# Target upstream repository API endpoint
API_URL = "https://github.com"
OUTPUT_DIR = "KQL"

# Create the folder locally in your Actions container execution space
os.makedirs(OUTPUT_DIR, exist_ok=True)

def replicate_kql_database():
    print("Initiating API mirror replication pipeline...")
    headers = {"Accept": "application/vnd.github.v3+json"}
    response = requests.get(API_URL, headers=headers, timeout=30)
    
    if response.status_code != 200:
        print(f"API Error: Received status code {response.status_code}")
        return

    file_list = response.json()
    print(f"Discovered {len(file_list)} tracking rules inside source index.")
    
    saved_count = 0
    for item in file_list:
        # Replicate only files that contain the explicit KQL extension
        if item.get("type") == "file" and item.get("name", "").endswith(".kql"):
            file_name = item["name"]
            download_url = item["download_url"]
            
            print(f"Replicating: {file_name}")
            file_response = requests.get(download_url, timeout=30)
            
            if file_response.status_code == 200:
                target_path = os.path.join(OUTPUT_DIR, file_name)
                with open(target_path, "w", encoding="utf-8") as f:
                    f.write(file_response.text)
                saved_count += 1

    print(f"Success! Replicated {saved_count} clean KQL rule structures.")

if __name__ == "__main__":
    replicate_kql_database()
