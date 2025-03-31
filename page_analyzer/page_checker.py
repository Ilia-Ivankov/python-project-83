import requests
from bs4 import BeautifulSoup


def check_and_parse_url(url: str) -> dict | bool:
    """Check URL and parse SEO elements, return False on error"""
    try:
        response = requests.get(url, timeout=180)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        h1 = soup.find("h1")
        title = soup.find("title")
        description_tag = soup.find("meta", attrs={"name": "description"})

        return {
            "status_code": response.status_code,
            "h1": h1.text.strip() if h1 else None,
            "title": title.text.strip() if title else None,
            "description": description_tag["content"].strip()
            if description_tag
            else None,
        }
    except requests.exceptions.RequestException:
        return False
