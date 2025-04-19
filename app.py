from flask import Flask, render_template, request, redirect, url_for, send_file, flash
import os
from scraper.config import SUPPORTED_WEBSITES
from scraper.scraper_core import scrape_ads
from scraper.utils import save_to_csv, save_to_json

app = Flask(__name__)
app.secret_key = "Baba##thunday"  # Needed for flashing messages

DATA_DIR = os.path.join(os.getcwd(), "data")
os.makedirs(DATA_DIR, exist_ok=True)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        keyword = request.form.get("keyword")
        region = request.form.get("region")
        website_key = request.form.get("website")

        if not keyword or not region or not website_key:
            flash("All fields are required!")
            return redirect(url_for("index"))

        site_info = SUPPORTED_WEBSITES.get(website_key)
        if not site_info:
            flash("Unsupported website selected.")
            return redirect(url_for("index"))

        site_url = site_info["url"]
        ads = scrape_ads(site_url, keyword, region)

        # Save results
        csv_path = save_to_csv(ads, keyword, region, DATA_DIR)
        json_path = save_to_json(ads, keyword, region, DATA_DIR)
        if not csv_path or not json_path:
            flash("Failed to save scraped results.")
            return redirect(url_for("index"))

        return render_template(
            "results.html",
            ads=ads,
            site=site_url,
            keyword=keyword,
            region=region,
            csv_filename=os.path.basename(csv_path),
            json_filename=os.path.basename(json_path)
        )

    return render_template("index.html", websites=SUPPORTED_WEBSITES)


@app.route("/download/<filename>")
def download_file(filename):
    filepath = os.path.join(DATA_DIR, filename)
    if not os.path.exists(filepath):
        flash("File not found.")
        return redirect(url_for("index"))
    return send_file(filepath, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)


