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
