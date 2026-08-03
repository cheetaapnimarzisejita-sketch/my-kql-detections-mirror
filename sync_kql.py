import os
import requests

API_URL = "https://github.com"
OUTPUT_DIR = "KQL"

os.makedirs(OUTPUT_DIR, exist_ok=True)

def replicate_kql_database():
    print("Initiating authorized API mirror replication pipeline...")
    headers = {"Accept": "application/vnd.github.v3+json"}
    
    # Authenticate using the GitHub Actions built-in environment token
    token = os.getenv("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"token {token}"
        print("GitHub Token detected and injected into header rules.")
    else:
        print("Warning: Running without token authentication (subject to strict rate limiting).")

    response = requests.get(API_URL, headers=headers, timeout=30)
    
    if response.status_code != 200:
        print(f"API Error: Received status code {response.status_code}")
        print("Payload response text:", response.text)
        return

    file_list = response.json()
    print(f"Discovered {len(file_list)} entries in the remote repository tracker.")
    
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

    print(f"Success! Replicated {saved_count} clean KQL rule files inside the folder local context.")

if __name__ == "__main__":
    replicate_kql_database()
