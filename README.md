# 📚 Book Scraper & Analytics Project

A comprehensive web scraping and data analysis project that extracts book information from an online bookstore, cleans the data and provides detailed analytics with visualizations.

## 🎯 Project Overview

This project demonstrates a complete data pipeline from web scraping to data visualization:

1. **Web Scraping**: Extract book data from multiple pages
2. **Data Cleaning**: Process and standardize the raw data
3. **Data Analysis**: Generate descriptive statistics
4. **Data Visualization**: Create comprehensive charts and plots

## 📁 Project Structure

```
BookScraping/
├── book_scaper.py          # Main web scraping script
├── clean_scraper.py        # Data cleaning and preprocessing
├── analyze_scraper.py      # Statistical analysis
├── visualize_scarper.py    # Data visualization and plotting
├── raw_books.csv          # Raw scraped data
├── cleaned_books.csv      # Processed and cleaned data
└── README.md             # Project documentation
```

## 🚀 Features

### Web Scraping (`book_scaper.py`)
- Scrapes book data from multiple pages
- Extracts: Title, Price, Rating, and Availability
- Handles pagination automatically
- Saves raw data to CSV format

### Data Cleaning (`clean_scraper.py`)
- Processes raw scraped data
- Converts availability text to stock numbers
- Handles missing values and duplicates
- Standardizes data formats
- Outputs clean dataset for analysis

### Statistical Analysis (`analyze_scraper.py`)
- Generates descriptive statistics
- Analyzes price, rating, and stock distributions
- Provides summary insights

### Data Visualization (`visualize_scarper.py`)
- **Distribution Analysis**: Histograms for Price, Rating, and Stock
- **Outlier Detection**: Boxplots for identifying anomalies
- **Top Rankings**: Bar charts for highest-priced and highest-stock books
- **Correlation Analysis**: Scatter plots for relationship exploration

## 📊 Generated Visualizations

1. **Histograms**: Distribution patterns and skewness analysis
2. **Boxplots**: Outlier detection and data spread
3. **Bar Charts**: Top 15 books by price and stock
4. **Scatter Plots**: Price vs Rating and Price vs Stock relationships

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.7+
- pip package manager

### Required Libraries
```bash
pip install pandas numpy matplotlib requests beautifulsoup4
```

### Alternative Installation
```bash
pip install -r requirements.txt
```

## 🎮 Usage

### 1. Run the Complete Pipeline
```bash
# Step 1: Scrape the data
python book_scaper.py

# Step 2: Clean the data
python clean_scraper.py

# Step 3: Analyze the data
python analyze_scraper.py

# Step 4: Visualize the data
python visualize_scarper.py
```

### 2. Individual Script Usage

#### Web Scraping
```bash
python book_scaper.py
```
- Scrapes book data from the target website
- Generates `raw_books.csv`

#### Data Cleaning
```bash
python clean_scraper.py
```
- Processes `raw_books.csv`
- Generates `cleaned_books.csv`

#### Statistical Analysis
```bash
python analyze_scraper.py
```
- Analyzes `cleaned_books.csv`
- Prints descriptive statistics

#### Data Visualization
```bash
python visualize_scarper.py
```
- Creates multiple visualization plots
- Displays interactive charts

## 📈 Data Schema

### Raw Data (`raw_books.csv`)
| Column       | Type   |         Description        |
|--------------|--------|----------------------------|
| Title        | String | Book title                 |
| Price        | String | Price with currency symbol |
| Rating       | String | Star rating (text/numeric) |
| Availability | String | Stock availability text    |

### Cleaned Data (`cleaned_books.csv`)
| Column | Type    |        Descriptiom       |
|--------|---------|--------------------------|
| Title  | String  | Book title               |
| Price  | Float   | Numeric price value      |
| Rating | Integer | Rating (1-5 scale)       |
| Stock  | Integer | Number of books in stock |

## 🔍 Key Insights

The analysis reveals:
- **Price Distribution**: Range and average book prices
- **Rating Patterns**: Customer satisfaction trends
- **Stock Levels**: Inventory distribution
- **Correlations**: Relationships between price, rating, and availability

## 🚧 Technical Notes

### Data Cleaning Process
- Extracts numeric values from text fields
- Handles currency symbols and formatting
- Converts word-based ratings to numeric values
- Processes availability text to extract stock numbers

### Visualization Features
- Automatic plot sizing and formatting
- Clear labeling and titles
- Professional styling
- Multiple chart types for comprehensive analysis

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


---

