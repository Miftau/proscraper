# 🕵️ Classified Ads Scraper (Flask + Selenium + BeautifulSoup)

A browser-based Python web app that scrapes classified ads (like OLX.pl), counts ads from a specific region, and lets users download results in CSV and JSON formats.

---

## 🚀 Features

- 🔍 Search any keyword + region from the selected site
- 🌍 Site config driven (easily extendable)
- 📄 Results table with clickable links
- 📦 Download results as CSV & JSON
- 🧠 Combines Selenium and BeautifulSoup for accurate scraping
- ✅ Supports pagination and dynamic content
- 💻 Simple browser UI (Bootstrap-powered)

---

## 🛠 Tech Stack

- Python (Flask)
- Selenium + WebDriver
- BeautifulSoup (bs4)
- Bootstrap 5 (Frontend)
- Railway (Deployment)

---

## 📦 Project Structure

├── app.py # Flask entry point ├── config/
│ └── sites.json # Site options ├── scraper/ │ ├── core_scraper.py # Scraper logic (Selenium + bs4) │ ├── driver_setup.py # Chrome WebDriver setup │ └── parser.py # HTML parsing logic ├── templates/ │ ├── index.html │ └── results.html ├── data/ # Output files ├── requirements.txt ├── README.md


---

## 🚧 Installation & Development

1. Clone this repo:

```bash
git clone https://github.com/Miftau/proscraper.git
cd "root_folder"

## Create a virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
pip install -r requirements.txt
