import pandas as pd
from pathlib import Path

# paths (adjust if needed)
zomato_path = Path("data/raw/zomato_bangalore.csv")
swiggy_path = Path("data/raw/swiggy_restaurants.csv")

# load
zomato = pd.read_csv(zomato_path, low_memory=False)
swiggy = pd.read_csv(swiggy_path, low_memory=False)

# function to summarize
def profile(df, name):
    print(f"\n🔍 PROFILE: {name}")
    print("Shape:", df.shape)
    print("Columns:", df.columns.tolist())
    print("\n-- Data Types --")
    print(df.dtypes)
    print("\n-- Missing% (non-zero only) --")
    miss = df.isna().mean() * 100
    print(miss[miss > 0].round(2).sort_values(ascending=False))
    print("\n-- Sample unique values --")
    key_cols = ['rate','rating','avgRating','deliveryTime','minDeliveryTime','maxDeliveryTime',
                'costForTwoStrings','approx_cost(for two people)','cuisines']
    for c in key_cols:
        if c in df.columns:
            print(f"\n{c}:", df[c].dropna().unique()[:10])

profile(zomato, "ZOMATO")
profile(swiggy, "SWIGGY")
