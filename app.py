from flask import Flask, render_template, request, redirect, url_for, send_file, flash
from flask_mail import Mail, Message
import os
from scraper.config import SUPPORTED_WEBSITES
from scraper.scraper_core import scrape_ads
from scraper.utils import save_to_csv, save_to_json

app = Flask(__name__)
app.secret_key = "Baba##thunday"  # Needed for flashing messages

# Mail configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")
app.config['MAIL_DEFAULT_SENDER'] = os.getenv("MAIL_USERNAME")
mail = Mail(app)

DATA_DIR = os.path.join(os.getcwd(), "data")
os.makedirs(DATA_DIR, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method != "POST":
        return render_template("index.html", sites=SUPPORTED_WEBSITES.keys())
    keyword = request.form.get("keyword")
    region = request.form.get("region")
    website_key = request.form.get("site")
    email = request.form.get("email")
    custom_url = request.form.get("custom_url")
    custom_selector = request.form.get("custom_selector")

    if not keyword or not region or not website_key:
        flash("Keyword, region, and site are required!")
        return redirect(url_for("index"))

    if custom_url:
        site_url = custom_url.strip()
    else:
        site_info = SUPPORTED_WEBSITES.get(website_key)
        if not site_info:
            flash("Unsupported website selected.")
            return redirect(url_for("index"))
        site_url = site_info["url"]

    ads = scrape_ads(site_url, keyword, region, custom_selector)

    # Save results
    csv_path = save_to_csv(ads, keyword, region, DATA_DIR)
    json_path = save_to_json(ads, keyword, region, DATA_DIR)
    if not csv_path or not json_path:
        flash("Failed to save scraped results.")
        return redirect(url_for("index"))

    # Optional email sending
    if email:
        try:
            msg = Message("Your ProScraper Results", recipients=[email])
            msg.body = f"Attached are your scraped results for '{keyword}' in '{region}'."
            with open(csv_path, 'rb') as f:
                msg.attach(os.path.basename(csv_path), "text/csv", f.read())
            with open(json_path, 'rb') as f:
                msg.attach(os.path.basename(json_path), "application/json", f.read())
            mail.send(msg)
            flash("Results sent to your email successfully!")
        except Exception as e:
            flash(f"Failed to send email: {str(e)}")

    return render_template(
        "results.html",
        ads=ads,
        site=site_url,
        keyword=keyword,
        region=region,
        csv_filename=os.path.basename(csv_path),
        json_filename=os.path.basename(json_path)
    )

@app.route("/download/<filename>")
def download_file(filename):
    filepath = os.path.join(DATA_DIR, filename)
    if not os.path.exists(filepath):
        flash("File not found.")
        return redirect(url_for("index"))
    return send_file(filepath, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=False)
