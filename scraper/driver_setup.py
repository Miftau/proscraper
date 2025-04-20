from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import shutil

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Get path to chromedriver
    chromedriver_path = shutil.which("chromedriver")

    if not chromedriver_path:
        raise RuntimeError("Chromedriver not found in PATH!")

    service = Service(executable_path=chromedriver_path)
    return webdriver.Chrome(service=service, options=chrome_options)
