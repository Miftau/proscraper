# scraper/core_scraper.py

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from time import sleep
from scraper.parser import parse_olx_ads

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Optional: run in headless mode
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=chrome_options)
    return driver

def scrape_ads(site_url, keyword, region, max_pages=3):
    driver = setup_driver()
    all_ads = []

    try:
        for page in range(1, max_pages + 1):
            search_url = f"{site_url}/{region}/?page={page}&q={keyword}&search[description]=1&search[dist]=0"
            print(f"Scraping: {search_url}")
            driver.get(search_url)
            sleep(3)  # Allow time for the page to fully load

            # Accept cookies popup if present
            try:
                consent_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Akceptuję')]")
                consent_btn.click()
                sleep(1)
            except:
                pass  # If no popup, continue silently

            # Parse the ads using BeautifulSoup through parser.py
            page_source = driver.page_source
            ads = parse_olx_ads(page_source)

            if not ads:
                break  # No more ads found

            all_ads.extend(ads)

    except TimeoutException:
        print("Timeout while loading the page.")
    finally:
        driver.quit()

    return all_ads



