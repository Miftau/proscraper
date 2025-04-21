from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re



def parse_generic_ads(html, selector=None):
    soup = BeautifulSoup(html, "html.parser")
    ads = []

    if not selector:
        print("No selector provided.")
        return ads

    ad_elements = soup.select(selector)
    for ad in ad_elements:
        try:
            title = (
                ad.select_one("h2, .title, .ad-title") or {}
            ).get_text(strip=True)

            price = (
                ad.select_one(".price, .amount, .ad-price") or {}
            ).get_text(strip=True)

            location = (
                ad.select_one(".location, .place, .city") or {}
            ).get_text(strip=True)

            date = (
                ad.select_one(".date, .posted-date, .timestamp") or {}
            ).get_text(strip=True)

            url = (
                ad.select_one("a[href]")["href"]
                if ad.select_one("a[href]")
                else ""
            )

            image = (
                ad.select_one("img")["src"]
                if ad.select_one("img")
                else ""
            )

            description = (
                ad.select_one(".description, p, .text") or {}
            ).get_text(strip=True)

            rating = (
                ad.select_one(".rating, .stars") or {}
            ).get_text(strip=True)

            category = (
                ad.select_one(".category, .tag, .label") or {}
            ).get_text(strip=True)

            seller = (
                ad.select_one(".seller, .vendor, .user") or {}
            ).get_text(strip=True)

            views = (
                ad.select_one(".views, .hits, .count") or {}
            ).get_text(strip=True)

            contact = (
                ad.select_one(".contact, .phone, .email") or {}
            ).get_text(strip=True)

            ads.append({
                "title": title,
                "price": price,
                "location": location,
                "date": date,
                "url": url,
                "image": image,
                "description": description,
                "rating": rating,
                "category": category,
                "seller": seller,
                "views": views,
                "contact": contact,
            })
        except Exception as e:
            print(f"Error parsing ad: {e}")
            continue



    # Optional: detect next page URL
    next_page_tag = soup.find("a", text=re.compile("next", re.IGNORECASE))
    next_page_url = urljoin(url, next_page_tag["href"]) if next_page_tag and url else None

    return {
        "ads": ads,
        "next_page_url": next_page_url
    }

