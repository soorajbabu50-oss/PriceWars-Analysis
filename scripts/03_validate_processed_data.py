import pandas as pd

z = pd.read_csv("data/processed/zomato_clean.csv")
s = pd.read_csv("data/processed/swiggy_clean.csv")

print("ZOMATO:", z.shape)
print(z.head())

print("\nSWIGGY:", s.shape)
print(s.head())

# Basic sanity checks
print("\nMissing values:\n")
print("Zomato:", z.isna().sum())
print("Swiggy:", s.isna().sum())
