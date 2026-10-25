import pandas as pd
import numpy as np

print("Step 1: Loading raw Olist CSV datasets...")
orders = pd.read_csv('olist_orders_dataset.csv')
items = pd.read_csv('olist_order_items_dataset.csv')
products = pd.read_csv('olist_products_dataset.csv')
payments = pd.read_csv('olist_order_payments_dataset.csv')
reviews = pd.read_csv('olist_order_reviews_dataset.csv')
translation = pd.read_csv('product_category_name_translation.csv')

# 1. Translate product categories from Portuguese to English
print("Step 2: Translating product categories...")
products = products.merge(translation, on='product_category_name', how='left')
products['product_category'] = products['product_category_name_english'].fillna('Other/Unknown')

# 2. Aggregate payments per order (ensures 1 order = 1 payment sum)
print("Step 3: Aggregating order payments...")
payment_agg = payments.groupby('order_id').agg(
    total_payment=('payment_value', 'sum'),
    primary_payment_type=('payment_type', lambda x: x.iloc[0])
).reset_index()

# 3. Merge main relational datasets
print("Step 4: Merging tables into master dataframe...")
df = orders.merge(items, on='order_id', how='inner')
df = df.merge(products[['product_id', 'product_category']], on='product_id', how='left')
df = df.merge(payment_agg, on='order_id', how='left')
df = df.merge(reviews[['order_id', 'review_score']], on='order_id', how='left')

# 4. Convert timestamps to datetime format
print("Step 5: Processing date fields...")
datetime_cols = ['order_purchase_timestamp', 'order_delivered_customer_date', 'order_estimated_delivery_date']
for col in datetime_cols:
    df[col] = pd.to_datetime(df[col])

# 5. Feature Engineering: Delivery Delays & Return Proxy Target
print("Step 6: Engineering features (Delivery Delays & Return Proxy)...")
df['delivery_delay_days'] = (df['order_delivered_customer_date'] - df['order_estimated_delivery_date']).dt.days

# Define Return Flag (1 = Canceled/Unavailable status OR 1-Star Review, 0 = Otherwise)
df['is_returned'] = np.where(
    (df['order_status'].isin(['canceled', 'unavailable'])) | (df['review_score'] == 1),
    1, 0
)

# 6. Save master processed dataset
output_file = 'olist_processed_returns.csv'
df.to_csv(output_file, index=False)

print("\n--------------------------------------------------")
print(f"SUCCESS! Master file saved as '{output_file}'.")
print(f"Total Records: {len(df):,}")
print(f"Overall Return Proxy Rate: {df['is_returned'].mean():.2%}")
print("--------------------------------------------------")