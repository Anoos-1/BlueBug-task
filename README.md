# Books to Scrape

`scrape.py` pulls the first 100 books (pages 1-5) from books.toscrape.com into `books.csv`.
`load_db.py` loads that CSV into a local SQLite database.
`queries.sql` has the three queries: average price per rating, top 5 most expensive 4/5-star books, and out-of-stock count per rating.

## Five lines

**What broke / took longer than expected:**
- The £ symbol kept getting mangled going through my editor/terminal, so matching on it in the price string failed - ended up just stripping everything that wasn't a digit or a dot instead.
- `in_stock` had to be written out as the string `"true"`/`"false"`, not Python's `True`/`False` - `csv.writer` just dumps whatever you give it.
- All 100 books came back in stock, so the "out of stock per rating" query returns nothing. Not a bug, just what the site has.

**If it started blocking me after 50 requests:**
- Add a real delay between pages (already have a 1s sleep, would bump it up).
- Set a real `User-Agent` header - `requests`' default one is an easy way to get flagged.
- Cache pages already pulled to disk so a retry doesn't re-hit ones that worked.
- If it's IP-based, rotate through a couple of proxies.
