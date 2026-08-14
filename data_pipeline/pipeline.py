import requests
from bs4 import BeautifulSoup
import pandas as pd
import sqlite3
import re, os

print("Starting scrape...")

#Targeting 3 categories 
CATEGORIES={
    "Philosophy": "https://books.toscrape.com/catalogue/category/books/philosophy_7/",
    "Mystery": "https://books.toscrape.com/catalogue/category/books/mystery_3/",
    "Historical Fiction": "https://books.toscrape.com/catalogue/category/books/historical-fiction_4/"
}

RATING_WORDS = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}

scraped_data = []

for cat_name, base_url in CATEGORIES.items():
    page_num = 1
    while True:
        page_url = f"{base_url}index.html" if page_num == 1 else f"{base_url}page-{page_num}.html"
        response = requests.get(page_url)

        if response.status_code != 200:
            break  # no more pages in this category

        soup = BeautifulSoup(response.text, 'html.parser')
        books = soup.select('article.product_pod')

        if not books:
            break

        for book in books:
            title = book.h3.a['title']
            price_text = book.select_one('p.price_color').get_text(strip=True)
            rating_word = book.select_one('p.star-rating')['class'][1]
            availability_text = book.select_one('p.instock.availability').get_text(strip=True)

            scraped_data.append({
                'title': title,
                'price': price_text,
                'star_rating': rating_word,
                'availability': availability_text,
                'category': cat_name
            })

        page_num += 1

print(f"Scraped {len(scraped_data)} books total across {len(CATEGORIES)} categories.")

print("\nCleaning the scraped data...")
df = pd.DataFrame(scraped_data)

# Strip the currency symbol and cast to float (no regex this time, plain string ops)
df['price_gbp'] = df['price'].str.replace(r'[^\d.]', '', regex=True).astype(float)

# Map text ratings into integers
df['rating'] = df['star_rating'].map(RATING_WORDS)

# Parse availability into a boolean
df['in_stock'] = df['availability'].apply(lambda x: 'In stock' in x)

# Row-cleaning policy: drop any row that failed to parse a required field
before = len(df)
df.dropna(subset=['price_gbp', 'rating', 'title'], inplace=True)   #Drop missing/messy rows
dropped = before - len(df)
print(f"Dropped {dropped} unparseable row(s) (policy: drop on failure, see README).")

# Fixed-rate GBP -> INR conversion (project-defined constant, no API call)
GBP_TO_INR_RATE = 105.50
df['price_inr'] = (df['price_gbp'] * GBP_TO_INR_RATE).round(2)

df_clean = df[['title', 'price_gbp', 'price_inr', 'rating', 'in_stock', 'category']].copy()
df_clean['rating'] = df_clean['rating'].astype(int)
df_clean['in_stock'] = df_clean['in_stock'].astype(int)

print('-' * 30)
print("Loading data into SQLite...\n")

db_name = 'zepto_books.db'
if os.path.exists(db_name):
    os.remove(db_name)  # start fresh each run

conn = sqlite3.connect(db_name)
cursor = conn.cursor()

cursor.executescript("""
CREATE TABLE categories (
    category_id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_name TEXT UNIQUE
);

CREATE TABLE books (
    book_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    price_gbp REAL,
    price_inr REAL,
    rating INTEGER,
    in_stock INTEGER,
    category_id INTEGER REFERENCES categories(category_id)
);
""")

# Insert unique categories first
categories_df = pd.DataFrame(df_clean['category'].unique(), columns=['category_name'])
categories_df.to_sql('categories', conn, if_exists='append', index=False)

# Pull back generated category_ids and map them onto the books
cat_map_df = pd.read_sql("SELECT * FROM categories", conn)
category_to_id = dict(zip(cat_map_df.category_name, cat_map_df.category_id))
df_clean['category_id'] = df_clean['category'].map(category_to_id)

books_df_db = df_clean.drop(columns=['category'])
books_df_db.to_sql('books', conn, if_exists='append', index=False)

print("Data loaded into normalized SQLite database (categories + books).\n")

print('-' * 30)
print("SQL QUERIES & PANDAS EQUIVALENCE\n")

queries = {
    "1. SELECT/WHERE (in-stock books under 20 GBP)":
        "SELECT title, price_gbp FROM books WHERE in_stock = 1 AND price_gbp < 20;",

    "2. ORDER BY + LIMIT (5 cheapest books)":
        "SELECT title, price_gbp FROM books ORDER BY price_gbp ASC LIMIT 5;",

    "3. DISTINCT (category names in the catalog)":
        "SELECT DISTINCT category_name FROM categories;",

    "4. BETWEEN (books priced 1500-2500 INR)":
        "SELECT title, price_inr FROM books WHERE price_inr BETWEEN 1500 AND 2500 LIMIT 5;",

    "5. IN (books rated 3, 4 or 5 stars)":
        "SELECT title, rating FROM books WHERE rating IN (3, 4, 5) LIMIT 5;",

    "6. JOIN (5-star books with their category names)": """
        SELECT c.category_name, b.title, b.rating
        FROM books b
        JOIN categories c ON b.category_id = c.category_id
        WHERE b.rating = 5
        ORDER BY c.category_name
        LIMIT 5;
    """
}
#Execute and print all sql queries
print("--- EXECUTING SQL QUERIES ---")
for desc, query in queries.items():
    print(f"\n{desc}")
    print(pd.read_sql(query, conn))

print("\n--- VALIDATING JOIN (PANDAS VS SQL) ---")

# Read the SQL JOIN result back into pandas
sql_join_result = pd.read_sql(queries["6. JOIN (5-star books with their category names)"], conn)

# Reproduce the same result purely in pandas, with no SQL JOIN involved
books_raw = pd.read_sql("SELECT * FROM books", conn)
categories_raw = pd.read_sql("SELECT * FROM categories", conn)

merged = pd.merge(books_raw, categories_raw, on='category_id')
pandas_join_result = merged[merged['rating'] == 5][['category_name', 'title', 'rating']]
pandas_join_result = pandas_join_result.sort_values(by='category_name').head(5).reset_index(drop=True)

print("\nSQL Output:")
print(sql_join_result)
print("\nPandas pd.merge() Output:")
print(pandas_join_result)

print("\nOutputs match:", sql_join_result.reset_index(drop=True).equals(pandas_join_result))

conn.close()
print("\nPipeline execution complete.")