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
