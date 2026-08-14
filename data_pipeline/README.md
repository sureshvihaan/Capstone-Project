# data_pipeline — Zepto Catalog Benchmarking Pipeline

A single end-to-end script that scrapes book listings from
`books.toscrape.com` (a public scraping-practice site — no login, no API
key, no paid tier), cleans and types the fields, converts GBP → INR at a
fixed project rate, loads everything into a normalized SQLite database, and
runs SQL + pandas queries against it.

## Setup

```bash
pip install requests beautifulsoup4 pandas
```

## Run (end to end)

```bash
python data_pipeline.py
```

This single script does everything in order: scrape → clean → load into
SQLite → run queries. Re-running it rebuilds `zepto_books.db` from scratch
each time (the old file is deleted at the start of the run).

Output produced:
- `zepto_books.db` — the SQLite database (categories + books tables)
- Printed output in the terminal for every SQL query and the pandas
  verification step (also save this output to a text file or notebook cell
  if you want it committed alongside the code)

## Design decisions

**Category selection:** 3 fixed categories — Travel, Poetry, Fiction — are
scraped by paging through each category's listing pages (`index.html`,
`page-2.html`, `page-3.html`, ...) until a `404`/empty page is hit. Together
these comfortably clear the required 60-book minimum.

**Currency conversion (required baseline):** `price_inr = price_gbp * 105.50`.
**1 GBP = 105.50 INR** is a fixed, project-defined constant for this
assignment only — not a live or historical market rate, and it requires no
external API call.

**Row-cleaning policy for unparseable rows:** rows are **dropped** if
`price_gbp`, `rating`, or `title` fail to parse (via `df.dropna(subset=...)`
after the type-conversion step). Justification: the HTML structure on
books.toscrape.com is consistent across every category/listing page, so
parse failures are expected to be rare-to-nonexistent; dropping a handful of
malformed rows is safer than median-imputing fields that are
categorical/boolean in nature (a "median rating" or "median in-stock flag"
isn't a meaningful concept). The script prints how many rows were dropped
on each run.

**Schema:**
```
categories(category_id PK, category_name UNIQUE)
books(book_id PK, title, price_gbp, price_inr, rating, in_stock, category_id FK -> categories)
```
Two tables, one PK/FK relationship, as required. Categories are inserted
first, then their auto-generated `category_id`s are mapped back onto the
books DataFrame before loading `books` via `to_sql`.

**SQL queries** cover, across 6 queries: `WHERE`, `ORDER BY` + `LIMIT`,
`DISTINCT`, `BETWEEN`, `IN`, and a `JOIN` (5-star books joined with their
category names). The JOIN result is independently reproduced using
`pd.merge()` on in-memory DataFrames (no SQL) pulled in via `pd.read_sql()`,
and the script prints `True`/`False` confirming the two outputs match.

## Files

| File | Purpose |
|---|---|
| `data_pipeline.py` | scrape + clean + convert + load + query, all in one script |

