# scraper/exporter.py

import csv
import json
from datetime import datetime

def save_results(ads, export_csv=True, export_json=True):
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    if export_csv:
        csv_path = f"data/results_{timestamp}.csv"
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=["title", "location", "link"])
            writer.writeheader()
            writer.writerows(ads)

    if export_json:
        json_path = f"data/results_{timestamp}.json"
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(ads, f, ensure_ascii=False, indent=4)
