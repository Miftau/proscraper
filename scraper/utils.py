# scraper/save_utils.py

import os
import csv
import json

def save_to_csv(data, keyword, region, output_dir="data"):
    if not data:
        return None

    filename = f"{keyword}_{region}.csv".replace(" ", "_")
    filepath = os.path.join(output_dir, filename)

    try:
        with open(filepath, mode="w", newline='', encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["title", "location", "link"])
            writer.writeheader()
            writer.writerows(data)
        return filepath
    except Exception as e:
        print(f"Error saving CSV: {e}")
        return None


def save_to_json(data, keyword, region, output_dir="data"):
    if not data:
        return None

    filename = f"{keyword}_{region}.json".replace(" ", "_")
    filepath = os.path.join(output_dir, filename)

    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        return filepath
    except Exception as e:
        print(f"Error saving JSON: {e}")
        return None
