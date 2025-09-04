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