import csv
import sqlite3

conn = sqlite3.connect("books.db")
cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS books")
cur.execute("""
    CREATE TABLE books (
        title TEXT,
        price REAL,
        rating INTEGER,
        in_stock INTEGER,
        url TEXT
    )
""")

with open("books.csv", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        cur.execute(
            "INSERT INTO books VALUES (?, ?, ?, ?, ?)",
            (
                row["title"],
                float(row["price"]),
                int(row["rating"]),
                1 if row["in_stock"] == "true" else 0,
                row["url"],
            ),
        )

conn.commit()
print(cur.execute("SELECT COUNT(*) FROM books").fetchone())
conn.close()
