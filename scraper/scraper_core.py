from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from urllib.parse import urljoin
from scraper.parser import parse_generic_ads


def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Headless mode for servers
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.page_load_strategy = 'eager'
    chrome_options.add_argument("--log-level=3")

    driver = webdriver.Chrome(options=chrome_options)
    driver.set_page_load_timeout(600)
    return driver


def scrape_ads(start_url, keyword, custom_selector=None, max_pages=3):
    driver = setup_driver()
    all_ads = []
    seen_urls = set()
    page_url = start_url

    try:
        for page in range(max_pages):
            if not page_url or page_url in seen_urls:
                break
            seen_urls.add(page_url)

            print(f"[Scraping] {page_url}")
            try:
                driver.get(page_url)
            except TimeoutException:
                print(f"[Timeout] {page_url}")
                continue

            sleep(4)

            # Handle cookie/consent popups
            try:
                consent = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Accept') or contains(text(), 'Akceptuję')]"))
                )
                consent.click()
                sleep(1)
            except:
                pass

            page_source = driver.page_source

            parsed = parse_generic_ads(page_source, base_url=page_url, custom_selector=custom_selector, keyword=keyword)
            ads = parsed.get("ads", [])

            if not ads:
                print(f"[Info] No ads found on page {page + 1}")
                break

            all_ads.extend(ads)

            # Handle pagination (from parser)
            next_url = parsed.get("next_page_url")
            if not next_url:
                print("[Pagination] No next page link found.")
                break

            page_url = urljoin(page_url, next_url)

    except WebDriverException as e:
        print(f"[WebDriver Error] {e}")
    finally:
        driver.quit()

    return all_ads

