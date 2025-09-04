# Scraping of the books from the website http://books.toscrape.com/catalogue/
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

# Function to scrape data from a single page
def scrape_page(url):
    books_data = []
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find all book articles on the page
    books = soup.find_all('article', class_='product_pod')
    
    for book in books:
        # Extract title
        title = book.h3.a['title']
        
        # Extract price
        price_str = book.find('p', class_='price_color').text
        price = float(re.search(r'[\d.]+', price_str).group())
        
        # Extract star rating (e.g., 'star-rating Three')
        rating_class = book.find('p', class_='star-rating')['class'][1]
        rating_map = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}
        rating = rating_map.get(rating_class, 0) # Default to 0 if not found
        
        # Extract availability
        availability = book.find('p', class_='instock availability').text.strip()
        
        books_data.append([title, price, rating, availability])
        
    return books_data

# Main scraping logic
all_books = []
base_url = 'http://books.toscrape.com/catalogue/'
# Scrape the first 50 pages (the entire site)
for i in range(1, 51):
    url = f'{base_url}page-{i}.html'
    print(f'Scraping page {i}...')
    all_books.extend(scrape_page(url))

# Create a DataFrame and save to CSV
df = pd.DataFrame(all_books, columns=['Title', 'Price', 'Rating', 'Availability'])
df.to_csv('raw_books.csv', index=False)

print("\nScraping complete. Raw data saved to raw_books.csv")
print(df.head())
# The code above scrapes book data from the specified website and saves it to 'raw_books.csv'.

#Cleaning of the scaped data
import pandas as pd

# Load the raw dataset
df_clean = pd.read_csv('raw_books.csv')

# 1. Check data types
print("Data Types:")
print(df_clean.dtypes)

# 2. Check for missing values
print("\nMissing Values:")
print(df_clean.isnull().sum())

# 3. Check for duplicates
print(f"\nNumber of duplicate rows: {df_clean.duplicated().sum()}")

# 4. Process the 'Availability' column to get the stock number
# Example: "In stock (22 available)" -> 22
# CORRECTED CODE
# This safely handles cases where no number is found by treating them as 0
df_clean['Stock'] = df_clean['Availability'].str.extract(r'(\d+)').fillna(0).astype(int)
df_clean = df_clean.drop('Availability', axis=1) # Drop the original column

# Save the cleaned data to a new CSV file
df_clean.to_csv('cleaned_books.csv', index=False)

print("\nPreprocessing complete. Cleaned data saved to cleaned_books.csv")
print(df_clean.head())
# The code above cleans the raw data and saves it to 'cleaned_books.csv'.

# Analysis of the cleaned data
import pandas as pd

# Load the cleaned dataset
df_analysis = pd.read_csv('cleaned_books.csv')

# Generate descriptive statistics for numerical columns
descriptive_stats = df_analysis[['Price', 'Rating', 'Stock']].describe()

print("Descriptive Statistical Analysis:")
print(descriptive_stats)
# The code above provides a statistical summary of the cleaned book data.

#Visualization of the cleaned data
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ---------- Load & validate ----------
df = pd.read_csv("cleaned_books.csv")

# Normalize column names (e.g., accidental spaces/casing)
df.columns = [c.strip().title() for c in df.columns]
required = ["Title", "Price", "Rating", "Stock"]
missing = [c for c in required if c not in df.columns]
if missing:
    raise ValueError(f"Missing required columns: {missing}. Found: {list(df.columns)}")

# ---------- Clean numeric fields ----------
def to_number(x):
    if pd.isna(x):
        return np.nan
    if isinstance(x, (int, float, np.number)):
        return float(x)
    s = str(x)
    # remove common currency symbols & thousands separators
    s = s.replace(",", "").replace("£", "").replace("$", "").replace("€", "")
    # keep digits, dot, and minus only
    s = "".join(ch for ch in s if ch.isdigit() or ch in ".-")
    try:
        return float(s)
    except:
        return np.nan

# Price
df["Price"] = df["Price"].apply(to_number)

# Rating: handle numeric or word-based (e.g., "Three", "four")
rating_map = {
    "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
    "One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5
}
# Try numeric first; if NaN, map from words
tmp_num = pd.to_numeric(df["Rating"], errors="coerce")
tmp_map = df["Rating"].map(rating_map)
df["Rating"] = tmp_num.fillna(tmp_map)
df["Rating"] = pd.to_numeric(df["Rating"], errors="coerce")

# Stock
df["Stock"] = pd.to_numeric(df["Stock"], errors="coerce")

# Drop rows without numeric values where needed
df = df.dropna(subset=["Price", "Rating", "Stock"])

# ---------- Helper: shorten long titles for plotting ----------
def shorten_title(t, n=40):
    t = "" if pd.isna(t) else str(t)
    return (t[: n - 1] + "…") if len(t) > n else t

df["TitleShort"] = df["Title"].apply(lambda x: shorten_title(x, 40))

# ---------- Histograms: distribution & skewness ----------
for col in ["Price", "Rating", "Stock"]:
    plt.figure(figsize=(8, 5))
    plt.hist(df[col].dropna(), bins="auto", edgecolor="black")
    plt.title(f"{col} Distribution")
    plt.xlabel(col)
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.show()

# For discrete ratings, an optional fixed-bin version (uncomment if you prefer):
# plt.figure(figsize=(8,5))
# plt.hist(df["Rating"].dropna(), bins=[0.5,1.5,2.5,3.5,4.5,5.5], edgecolor="black")
# plt.xticks([1,2,3,4,5])
# plt.title("Rating Distribution (Discrete)")
# plt.xlabel("Rating")
# plt.ylabel("Frequency")
# plt.tight_layout()
# plt.show()

# ---------- Boxplots: outlier detection ----------
for col in ["Price", "Rating", "Stock"]:
    plt.figure(figsize=(6, 5))
    plt.boxplot(df[col].dropna(), vert=True, labels=[col], showfliers=True)
    plt.title(f"{col} Boxplot")
    plt.tight_layout()
    plt.show()

# ---------- Bar charts: top-N comparisons ----------
N = 15

# Top by Price
top_price = df.nlargest(N, "Price")[["TitleShort", "Price"]]
plt.figure(figsize=(10, 6))
# barh with reversed order so the largest is at the top visually
plt.barh(top_price["TitleShort"][::-1], top_price["Price"][::-1])
plt.title(f"Top {N} Books by Price")
plt.xlabel("Price")
plt.ylabel("Title")
plt.tight_layout()
plt.show()

# Top by Stock
top_stock = df.nlargest(N, "Stock")[["TitleShort", "Stock"]]
plt.figure(figsize=(10, 6))
plt.barh(top_stock["TitleShort"][::-1], top_stock["Stock"][::-1])
plt.title(f"Top {N} Books by Stock")
plt.xlabel("Stock")
plt.ylabel("Title")
plt.tight_layout()
plt.show()

# ---------- Relationship checks: scatter plots ----------
# Price vs Rating
plt.figure(figsize=(7, 5))
plt.scatter(df["Rating"], df["Price"])
plt.title("Price vs Rating")
plt.xlabel("Rating")
plt.ylabel("Price")
plt.tight_layout()
plt.show()

# Price vs Stock
plt.figure(figsize=(7, 5))
plt.scatter(df["Stock"], df["Price"])
plt.title("Price vs Stock")
plt.xlabel("Stock")
plt.ylabel("Price")
plt.tight_layout()
plt.show()
# The code above visualizes the cleaned book data with various plots.
