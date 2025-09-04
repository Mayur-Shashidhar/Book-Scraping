import pandas as pd

# Load the cleaned dataset
df_analysis = pd.read_csv('cleaned_books.csv')

# Generate descriptive statistics for numerical columns
descriptive_stats = df_analysis[['Price', 'Rating', 'Stock']].describe()

print("Descriptive Statistical Analysis:")
print(descriptive_stats)
