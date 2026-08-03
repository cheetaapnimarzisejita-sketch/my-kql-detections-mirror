import os
import requests

API_URL = "https://github.com"
OUTPUT_DIR = "KQL"

os.makedirs(OUTPUT_DIR, exist_ok=True)

def replicate_kql_database():
    print("Initiating authorized API mirror replication pipeline...")
    headers = {"Accept": "application/vnd.github.v3+json"}
    
    token = os.getenv("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"token {token}"

    response = requests.get(API_URL, headers=headers, timeout=30)
    if response.status_code != 200:
        print(f"API Error: {response.status_code}")
        return

    file_list = response.json()
    saved_count = 0
    
    for item in file_list:
        if item.get("type") == "file" and item.get("name", "").endswith(".kql"):
            file_name = item["name"]
            download_url = item["download_url"]
            
            file_response = requests.get(download_url, headers=headers, timeout=30)
            if file_response.status_code == 200:
                target_path = os.path.join(OUTPUT_DIR, file_name)
                with open(target_path, "w", encoding="utf-8") as f:
                    f.write(file_response.text)
                saved_count += 1

    print(f"Success! Stored {saved_count} clean files.")

if __name__ == "__main__":
    replicate_kql_database()

