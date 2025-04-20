from bs4 import BeautifulSoup

def dispatch_parser(site_key):
    parsers = {
        "olx": parse_olx_ads,
        "ebay": parse_ebay_ads,
        "jumia": parse_jumia_ads,
        "konga": parse_konga_ads,
        "aliexpress": parse_aliexpress_ads,
        "amazon": parse_amazon_ads,
        "craigslist": parse_craigslist_ads,
        "mercadolibre": parse_mercadolibre_ads,
        "gumtree": parse_gumtree_ads,
        "etsy": parse_etsy_ads,
        "walmart": parse_walmart_ads,
        "target": parse_target_ads,
        "bestbuy": parse_bestbuy_ads,
        "shopee": parse_shopee_ads,
        "flipkart": parse_flipkart_ads
    }
    return parsers.get(site_key, default_parser)


# =================== Site-Specific Parsers ===================

def parse_olx_ads(html):
    soup = BeautifulSoup(html, "html.parser")
    ads = []
    listings = soup.select("div[data-cy='l-card']")
    for listing in listings:
        title = listing.select_one("h6")
        location = listing.select_one("p[data-testid='location-date']")
        link = listing.select_one("a")
        if title and link:
            ads.append({
                "title": title.get_text(strip=True),
                "location": location.get_text(strip=True) if location else "Unknown",
                "link": link["href"]
            })
    return ads


def parse_ebay_ads(html):
    soup = BeautifulSoup(html, "html.parser")
    ads = []
    for item in soup.select("li.s-item"):
        title = item.select_one("h3.s-item__title")
        location = item.select_one("span.s-item__location")
        link = item.select_one("a.s-item__link")
        if title and link:
            ads.append({
                "title": title.get_text(strip=True),
                "location": location.get_text(strip=True) if location else "Unknown",
                "link": link["href"]
            })
    return ads


def parse_jumia_ads(html):
    soup = BeautifulSoup(html, "html.parser")
    ads = []
    for item in soup.select("article.prd"):
        title = item.select_one("h3.name")
        link = item.select_one("a.core")
        if title and link:
            ads.append({
                "title": title.get_text(strip=True),
                "location": "Jumia",
                "link": "https://www.jumia.com.ng" + link["href"]
            })
    return ads


def parse_konga_ads(html):
    soup = BeautifulSoup(html, "html.parser")
    ads = []
    for item in soup.select(".product-block"):
        title = item.select_one(".product-block-title")
        link = item.select_one("a")
        if title and link:
            ads.append({
                "title": title.get_text(strip=True),
                "location": "Konga",
                "link": link["href"]
            })
    return ads


def parse_aliexpress_ads(html):
    soup = BeautifulSoup(html, "html.parser")
    ads = []
    for item in soup.select("a._3t7zg"):
        title = item.get("title") or item.get_text(strip=True)
        link = "https:" + item["href"] if item["href"].startswith("//") else item["href"]
        ads.append({
            "title": title,
            "location": "AliExpress",
            "link": link
        })
    return ads


def parse_amazon_ads(html):
    soup = BeautifulSoup(html, "html.parser")
    ads = []
    for item in soup.select("div.s-result-item"):
        title = item.select_one("h2 span")
        link = item.select_one("a.a-link-normal")
        if title and link:
            ads.append({
                "title": title.get_text(strip=True),
                "location": "Amazon",
                "link": "https://www.amazon.com" + link["href"]
            })
    return ads


def parse_craigslist_ads(html):
    soup = BeautifulSoup(html, "html.parser")
    ads = []
    for item in soup.select(".result-row"):
        title = item.select_one(".result-title")
        location = item.select_one(".result-hood")
        if title:
            ads.append({
                "title": title.get_text(strip=True),
                "location": location.get_text(strip=True) if location else "Unknown",
                "link": title["href"]
            })
    return ads


def parse_mercadolibre_ads(html):
    soup = BeautifulSoup(html, "html.parser")
    ads = []
    for item in soup.select("li.ui-search-layout__item"):
        title = item.select_one("h2")
        link = item.select_one("a")
        if title and link:
            ads.append({
                "title": title.get_text(strip=True),
                "location": "MercadoLibre",
                "link": link["href"]
            })
    return ads


def parse_gumtree_ads(html):
    soup = BeautifulSoup(html, "html.parser")
    ads = []
    for item in soup.select("article"):
        title = item.select_one("a[href*='/s-ad/']")
        if title:
            ads.append({
                "title": title.get_text(strip=True),
                "location": "Gumtree",
                "link": "https://www.gumtree.com" + title["href"]
            })
    return ads


def parse_etsy_ads(html):
    soup = BeautifulSoup(html, "html.parser")
    ads = []
    for item in soup.select("li.wt-list-unstyled"):
        link = item.select_one("a.listing-link")
        title = item.select_one("h3")
        if link and title:
            ads.append({
                "title": title.get_text(strip=True),
                "location": "Etsy",
                "link": link["href"]
            })
    return ads


def parse_walmart_ads(html):
    soup = BeautifulSoup(html, "html.parser")
    ads = []
    for item in soup.select("div.search-result-gridview-item"):
        title = item.select_one("a.product-title-link span")
        link = item.select_one("a.product-title-link")
        if title and link:
            ads.append({
                "title": title.get_text(strip=True),
                "location": "Walmart",
                "link": "https://www.walmart.com" + link["href"]
            })
    return ads


def parse_target_ads(html):
    soup = BeautifulSoup(html, "html.parser")
    ads = []
    for item in soup.select("li.h-padding-a-none"):
        title = item.select_one("a[data-test='product-title']")
        if title:
            ads.append({
                "title": title.get_text(strip=True),
                "location": "Target",
                "link": "https://www.target.com" + title["href"]
            })
    return ads


def parse_bestbuy_ads(html):
    soup = BeautifulSoup(html, "html.parser")
    ads = []
    for item in soup.select("li.sku-item"):
        title = item.select_one("h4.sku-header a")
        if title:
            ads.append({
                "title": title.get_text(strip=True),
                "location": "BestBuy",
                "link": "https://www.bestbuy.com" + title["href"]
            })
    return ads


def parse_shopee_ads(html):
    soup = BeautifulSoup(html, "html.parser")
    ads = []
    for item in soup.select("a[data-sqe='link']"):
        title = item.get("title") or item.get_text(strip=True)
        link = "https://shopee.com" + item["href"]
        ads.append({
            "title": title,
            "location": "Shopee",
            "link": link
        })
    return ads


def parse_flipkart_ads(html):
    soup = BeautifulSoup(html, "html.parser")
    ads = []
    for item in soup.select("div._1AtVbE"):
        title = item.select_one("div._4rR01T")
        link = item.select_one("a._1fQZEK")
        if title and link:
            ads.append({
                "title": title.get_text(strip=True),
                "location": "Flipkart",
                "link": "https://www.flipkart.com" + link["href"]
            })
    return ads

# =================== Default Parser ===================

def default_parser(html):
    soup = BeautifulSoup(html, "html.parser")
    ads = []
    for link in soup.find_all("a", href=True):
        text = link.get_text(strip=True)
        if text and len(text) > 10:
            ads.append({
                "title": text,
                "location": "Unknown",
                "link": link["href"]
            })
    return ads
