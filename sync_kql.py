import os
import requests
import re

# Direct structured data source mirroring the community rules
UPSTREAM_URL = "https://githubusercontent.com"
OUTPUT_DIR = "KQL"

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

def sanitize_filename(filename):
    # Remove characters that are invalid in filenames
    return re.sub(r'[\\/*?:"<>|]', "", filename)

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
            
        # Extract a clean title from the comment block of the query safely
        try:
            lines = rule_body.split('\n')
            first_line = lines[0] # Grab the actual text string from the list
            title = first_line.replace("//", "").strip().lower().replace(" ", "-")
            title = sanitize_filename(title)
            if not title:
                title = f"detection-rule-{index}"
        except Exception:
            title = f"detection-rule-{index}"
            
        # Verify it contains valid KQL structure
        if "where" in rule_body or "project" in rule_body or "extend" in rule_body:
            file_name = f"{title}.kql"
            file_path = os.path.join(OUTPUT_DIR, file_name)
            
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(rule_body)
            print(f"Synchronized file: {file_path}")

if __name__ == "__main__":
    pull_active_kql_library()
