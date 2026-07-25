import pandas as pd
import numpy as np
import re
from pathlib import Path

# === Paths ===
zomato_path = Path("data/raw/zomato_bangalore.csv")
swiggy_path = Path("data/raw/swiggy_restaurants.csv")

# === Load ===
zomato = pd.read_csv(zomato_path, low_memory=False)
swiggy = pd.read_csv(swiggy_path, low_memory=False)

# ===============================
# 🧹 ZOMATO CLEANING
# ===============================

# Clean rating (remove '/5', 'NEW', and convert to numeric)
zomato['rate_clean'] = (
    zomato['rate']
    .astype(str)
    .str.extract(r'(\d+\.?\d*)')
    .astype(float)
)

# Clean cost (approx_cost(for two people))
zomato['cost_two_clean'] = (
    zomato['approx_cost(for two people)']
    .astype(str)
    .str.replace(',', '', regex=False)
    .astype(float)
)

# Visibility index = rating × log(1 + votes)
zomato['visibility_index'] = zomato.apply(
    lambda x: x['rate_clean'] * np.log1p(x['votes']) if pd.notnull(x['rate_clean']) else np.nan,
    axis=1
)

# Keep selected columns
zomato_clean = zomato[[
    'name', 'location', 'cuisines', 'rate_clean', 'votes', 'cost_two_clean',
    'visibility_index', 'online_order', 'book_table', 'listed_in(city)'
]]

# ===============================
# 🧹 SWIGGY CLEANING
# ===============================

# Clean ratings ('--' to NaN)
swiggy['rating_clean'] = pd.to_numeric(
    swiggy['avgRating'].replace('--', np.nan),
    errors='coerce'
)

# Clean cost (extract numeric from ₹xxx FOR TWO)
swiggy['cost_two_clean'] = swiggy['costForTwoStrings'].str.extract(r'(\d+)').astype(float)

# Delivery time (already numeric but ensure float)
swiggy['delivery_mins'] = swiggy['deliveryTime'].astype(float)

# Clean cuisines (convert from stringified list)
def clean_cuisine_list(c):
    if pd.isna(c): return np.nan
    c = re.sub(r"[\[\]']", '', str(c))
    return ', '.join([x.strip() for x in c.split() if x.strip() not in ['', ',']])
swiggy['cuisines_clean'] = swiggy['cuisines'].apply(clean_cuisine_list)

# Visibility index proxy (rating × log(total ratings))
swiggy['totalRatings'] = swiggy['totalRatingsString'].str.extract(r'(\d+)').astype(float)
swiggy['visibility_index'] = swiggy.apply(
    lambda x: x['rating_clean'] * np.log1p(x['totalRatings']) if pd.notnull(x['rating_clean']) else np.nan,
    axis=1
)

# Keep selected columns
swiggy_clean = swiggy[[
    'name', 'city', 'area', 'cuisines_clean', 'rating_clean',
    'delivery_mins', 'minDeliveryTime', 'maxDeliveryTime',
    'cost_two_clean', 'visibility_index'
]]

# ===============================
# 💾 SAVE CLEANED FILES
# ===============================
Path("data/processed").mkdir(parents=True, exist_ok=True)
zomato_clean.to_csv("data/processed/zomato_clean.csv", index=False)
swiggy_clean.to_csv("data/processed/swiggy_clean.csv", index=False)

print("✅ Cleaned files saved to data/processed/")
print("Zomato:", zomato_clean.shape, "columns:", zomato_clean.columns.tolist())
print("Swiggy:", swiggy_clean.shape, "columns:", swiggy_clean.columns.tolist())
