import pandas as pd
import numpy as np
from scipy.stats import chi2_contingency
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

print("Step 1: Loading processed dataset...")
df = pd.read_csv('olist_processed_returns.csv')

# ==========================================
# PART 1: STATISTICAL HYPOTHESIS TESTING
# ==========================================
print("\n--- PART 1: CHI-SQUARE STATISTICAL TEST ---")
df['delay_category'] = np.where(df['delivery_delay_days'] > 0, 'Late', 'On-Time/Early')

contingency_table = pd.crosstab(df['delay_category'], df['is_returned'])
chi2, p_val, dof, expected = chi2_contingency(contingency_table)

print(f"Chi-Square Statistic: {chi2:.4f}")
print(f"p-value: {p_val:.4e}")
if p_val < 0.05:
    print("STATISTICAL VERDICT: Reject Null Hypothesis (H0). Delivery delays statistically INCREASE return rates (p < 0.05).")
else:
    print("STATISTICAL VERDICT: Fail to reject Null Hypothesis (H0).")

# ==========================================
# PART 2: CUSTOMER K-MEANS CLUSTERING
# ==========================================
print("\n--- PART 2: K-MEANS CUSTOMER CLUSTERING ---")
print("Aggregating customer behavioral metrics...")

# Aggregate to Customer Level
customer_profile = df.groupby('customer_id').agg(
    total_spend=('total_payment', 'sum'),
    total_orders=('order_id', 'nunique'),
    return_count=('is_returned', 'sum'),
    avg_freight=('freight_value', 'mean')
).reset_index()

customer_profile['return_rate'] = customer_profile['return_count'] / customer_profile['total_orders']

# Feature Matrix Selection & Scaling
features = ['total_spend', 'total_orders', 'return_rate', 'avg_freight']
X = customer_profile[features].fillna(0)

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Fit K-Means Model (k = 3)
kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
customer_profile['Cluster_ID'] = kmeans.fit_predict(X_scaled)

# Map human-readable labels based on cluster centroids
cluster_summary = customer_profile.groupby('Cluster_ID')[features].mean()
print("\nCluster Centroids Summary:")
print(cluster_summary)

# Save clusters mapping file for Power BI link
output_clusters = 'customer_clusters.csv'
customer_profile[['customer_id', 'Cluster_ID', 'return_rate']].to_csv(output_clusters, index=False)

print("\n--------------------------------------------------")
print(f"SUCCESS! Customer cluster file saved as '{output_clusters}'.")
print("Cluster Distribution:")
print(customer_profile['Cluster_ID'].value_counts())
print("--------------------------------------------------")