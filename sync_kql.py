import os
import requests

# Clean community production stream
UPSTREAM_URL = "https://githubusercontent.com"
OUTPUT_DIR = "KQL"

# Create target directories
os.makedirs(OUTPUT_DIR, exist_ok=True)

def pull_active_kql_library():
    print("Connecting directly to the upstream community rule database...")
    response = requests.get(UPSTREAM_URL, timeout=30)
    
    if response.status_code != 200:
        print(f"Connection failed: {response.status_code}")
        return

    # Split cleanly by the precise rule dividers used by the system
    rules = response.text.split("// --- NEW RULE --- //")
    print(f"Successfully connected. Processing {len(rules)} items.")
    
    for index, rule_body in enumerate(rules):
        rule_body = rule_body.strip()
        if not rule_body:
            continue
            
        # Parse titles line-by-line safely without crashing
        lines = [line.strip() for line in rule_body.split('\n') if line.strip()]
        if not lines:
            continue
            
        # FIX: Extract the text index item from the array safely
        first_line = lines[0]
        clean_title = first_line.replace("//", "").replace(":", "").replace(" ", "-").strip().lower()
        
        # Strip windows/linux forbidden filename symbols
        for char in ['\\', '/', '*', '?', '"', '<', '>', '|', ':']:
            clean_title = clean_title.replace(char, "")
            
        if not clean_title or len(clean_title) < 3:
            clean_title = f"detection-rule-{index}"

        # Write clean .kql query payloads out
        if any(keyword in rule_body for keyword in ["where", "project", "extend", "take", "summarize"]):
            file_name = f"{clean_title}.kql"
            file_path = os.path.join(OUTPUT_DIR, file_name)
            
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(rule_body)
                
    print("Process complete! All available queries isolated.")

if __name__ == "__main__":
    pull_active_kql_library()
