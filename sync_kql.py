import os
import requests
from bs4 import BeautifulSoup

# Global targets
BASE_URL = "https://detections.ai"
OUTPUT_DIR = "KQL"

# Create the repository folder structure dynamically
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

def fetch_trending_detections():
    print("Initiating connection to Detections.ai...")
    response = requests.get(BASE_URL)
    if response.status_code != 200:
        print(f"Network error: Unable to hit endpoint (Status {response.status_code})")
        return
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Locate all recent cards/elements inside the live tracking layout 
    rules = soup.find_all('div', class_='rule-card') 
    print(f"Discovered {len(rules)} prospective logic components to map.")
    
    for rule in rules:
        try:
            # Reformat string headers into safe file path definitions
            raw_title = rule.find('h3').text.strip()
            title = raw_title.replace(" ", "-").replace("/", "-").lower()
            
            # Extract raw text from the query block elements
            kql_content = rule.find('code').text.strip() 
            
            if kql_content:
                file_path = os.path.join(OUTPUT_DIR, f"{title}.kql")
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(kql_content)
                print(f"Synchronized: {file_path}")
        except Exception as e:
            continue

if __name__ == "__main__":
    fetch_trending_detections()
