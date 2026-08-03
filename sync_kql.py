import os
import requests

# Direct structured data source mirroring the community rules
UPSTREAM_URL = "https://githubusercontent.com"
OUTPUT_DIR = "KQL"

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

def pull_active_kql_library():
    print("Connecting directly to the upstream community rule database...")
    response = requests.get(UPSTREAM_URL)
    
    if response.status_code != 200:
        print(f"Connection failed with status code: {response.status_code}")
        return

    # Parse individual KQL rules split by standard documentation dividers
    raw_content = response.text
    rules = raw_content.split("// --- NEW RULE --- //")
    
    print(f"Successfully processed database. Found {len(rules)} active rule packages.")
    
    for index, rule_body in enumerate(rules):
        rule_body = rule_body.strip()
        if not rule_body:
            continue
            
        # Extract a clean title from the comment block of the query
        try:
            first_line = rule_body.split('\n')[0]
            title = first_line.replace("//", "").strip().lower().replace(" ", "-")
        except Exception:
            title = f"detection-rule-{index}"
            
        # Verify it contains valid KQL structure
        if "where" in rule_body or "project" in rule_body:
            file_name = f"{title}.kql"
            file_path = os.path.join(OUTPUT_DIR, file_name)
            
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(rule_body)
            print(f"Synchronized file: {file_path}")

if __name__ == "__main__":
    pull_active_kql_library()
