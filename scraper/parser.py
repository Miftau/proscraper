
from bs4 import BeautifulSoup

def parse_olx_ads(page_source):
    soup = BeautifulSoup(page_source, 'html.parser')
    ads = []

    items = soup.select("div[data-cy='l-card']")
    for item in items:
        title_el = item.select_one("h6")
        loc_el = item.select_one("p.css-p6wsjo-Text")
        link_el = item.find('a', href=True)

        title = title_el.text.strip() if title_el else "No Title"
        location = loc_el.text.strip() if loc_el else "Unknown"
        link = f"https://www.olx.pl{link_el['href']}" if link_el else "#"

        ads.append({
            "title": title,
            "location": location,
            "link": link
        })

    return ads
