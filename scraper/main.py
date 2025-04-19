from scraper.scraper_core import scrape_ads
from scraper.utils import save_to_csv, save_to_json

def main():
    print("🔍 Welcome to the OLX Classified Ads Scraper!")

    keyword = input("Enter a search keyword (e.g., 'bike'): ").strip()
    region = input("Enter the region (e.g., 'mazowieckie'): ").strip()
    pages = input("Max number of pages to search [default=3]: ").strip()

    try:
        max_pages = int(pages) if pages else 3
    except ValueError:
        print("Invalid page count. Using default value of 3.")
        max_pages = 3

    ads = scrape_ads(
        site_url="https://www.olx.pl",
        keyword=keyword,
        region=region,
        max_pages=max_pages
    )

    if not ads:
        print("⚠️ No ads found.")
        return

    save_to_csv(ads, keyword, region)
    save_to_json(ads, keyword, region)

if __name__ == "__main__":
    main()