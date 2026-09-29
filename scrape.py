import csv
import time
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

BASE = "https://books.toscrape.com/catalogue/page-{}.html"
NUM_PAGES = 5
DELAY = 1

RATING_WORDS = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}

session = requests.Session()
session.headers.update({"User-Agent": "Mozilla/5.0 (book scraper exercise)"})


def fetch_page(page):
    url = BASE.format(page)
    resp = session.get(url, timeout=10)
    resp.raise_for_status()
    return url, resp.text


def extract_book(book, page_url):
    title = book.h3.a["title"]

    price_text = book.select_one("p.price_color").text
    price = float("".join(c for c in price_text if c.isdigit() or c == "."))

    rating_class = book.select_one("p.star-rating")["class"]
    rating_word = [c for c in rating_class if c != "star-rating"][0]
    rating = RATING_WORDS[rating_word]

    stock_text = book.select_one("p.instock.availability").text.strip()
    in_stock = "In stock" in stock_text

    book_url = urljoin(page_url, book.h3.a["href"])

    return {
        "title": title,
        "price": price,
        "rating": rating,
        "in_stock": str(in_stock).lower(),
        "url": book_url,
    }


def parse_books(html, page_url):
    soup = BeautifulSoup(html, "html.parser")
    return [extract_book(b, page_url) for b in soup.select("article.product_pod")]


def has_next_page(html):
    soup = BeautifulSoup(html, "html.parser")
    return soup.select_one("li.next a") is not None


def save_csv(rows, path="books.csv"):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["title", "price", "rating", "in_stock", "url"])
        writer.writeheader()
        writer.writerows(rows)


def main():
    rows = []
    for page in range(1, NUM_PAGES + 1):
        try:
            url, html = fetch_page(page)
        except requests.RequestException as e:
            print(f"page {page} failed: {e}")
            break

        rows.extend(parse_books(html, url))

        if not has_next_page(html):
            break

        time.sleep(DELAY)

    save_csv(rows)
    print(f"wrote {len(rows)} rows to books.csv")


if __name__ == "__main__":
    main()
