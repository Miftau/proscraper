import csv
import json
import os
from datetime import datetime


def export_to_csv(ads, output_dir="results"):
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = os.path.join(output_dir, f"ads_{timestamp}.csv")

    if not ads:
        return file_path

    fieldnames = [
        "title", "price", "location", "date", "url", "description", "image",
        "rating", "category", "seller", "views", "contact"
    ]

    with open(file_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for ad in ads:
            writer.writerow({key: ad.get(key, "") for key in fieldnames})

    return file_path


def export_to_json(ads, output_dir="results"):
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = os.path.join(output_dir, f"ads_{timestamp}.json")

    with open(file_path, mode="w", encoding="utf-8") as file:
        json.dump(ads, file, indent=2, ensure_ascii=False)

    return file_path

