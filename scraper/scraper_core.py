from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from time import sleep
from bs4 import BeautifulSoup
from scraper.parser import dispatch_parser

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(options=chrome_options)

def scrape_ads(site_url, keyword, region, parser_name=None, selector=None, max_pages=3):
    driver = setup_driver()
    all_ads = []

    try:
        for page in range(1, max_pages + 1):
            if "{region}" in site_url and "{keyword}" in site_url:
                search_url = site_url.format(region=region, keyword=keyword, page=page)
            else:
                search_url = f"{site_url}?page={page}&q={keyword}"

            print(f"Scraping: {search_url}")
            driver.get(search_url)
            sleep(3)

            # Accept cookies popup if present
            try:
                consent_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Akceptuję')]")
                consent_btn.click()
                sleep(1)
            except:
                pass

            page_source = driver.page_source

            # Use predefined parser if available
            if parser_name:
                parser_func = dispatch_parser(parser_name)
                ads = parser_func(page_source)
            elif selector:
                ads = extract_generic_ads(page_source, selector)
            else:
                ads = []

            if not ads:
                break

            all_ads.extend(ads)

    except TimeoutException:
        print("Timeout while loading the page.")
    finally:
        driver.quit()

    return all_ads

def extract_generic_ads(html, selector):
    soup = BeautifulSoup(html, "html.parser")
    elements = soup.select(selector)
    ads = []

    for el in elements:
        text = el.get_text(strip=True)
        link = el.find("a")["href"] if el.find("a") else "#"
        ads.append({
            "title": text,
            "location": "N/A",
            "link": link
        })

    return ads



