# E-Commerce Revenue & Customer Retention Analysis

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_csv("../data/online_retail.csv", encoding="latin1")

print("Original shape:", df.shape)

# --- DATA CLEANING ---

# 1. Remove cancelled orders (InvoiceNo starting with 'C')
df = df[~df["InvoiceNo"].astype(str).str.startswith("C")]

# 2. Remove rows with missing CustomerID
df = df.dropna(subset=["CustomerID"])

# 3. Remove negative or zero quantity and price
df = df[(df["Quantity"] > 0) & (df["UnitPrice"] > 0)]

# 4. Convert InvoiceDate to datetime
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

# 5. Create Revenue column
df["Revenue"] = df["Quantity"] * df["UnitPrice"]

print("Cleaned shape:", df.shape)

print("\nMissing values after cleaning:")
print(df.isna().sum())

# Save cleaned data for later SQL & Power BI use
df.to_csv("../data/cleaned_retail.csv", index=False)

print("\nCleaned dataset saved as data/cleaned_retail.csv")

# --- BUSINESS ANALYSIS ---

# 1. Monthly Revenue Trend
df["Month"] = df["InvoiceDate"].dt.to_period("M")

monthly_revenue = (
    df.groupby("Month")["Revenue"]
    .sum()
    .sort_index()
)

print("\nMonthly Revenue:")
print(monthly_revenue.head())

# Plot monthly revenue
plt.figure()
monthly_revenue.plot()
plt.title("Monthly Revenue Trend")
plt.xlabel("Month")
plt.ylabel("Revenue")
plt.tight_layout()
plt.show()


# 2. Top 10 Products by Revenue
top_products = (
    df.groupby("Description")["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print("\nTop 10 Products by Revenue:")
print(top_products)


# 3. Customer Lifetime Value (Top Customers)
customer_revenue = (
    df.groupby("CustomerID")["Revenue"]
    .sum()
    .sort_values(ascending=False)
)

print("\nTop 10 Customers by Revenue:")
print(customer_revenue.head(10))

# --- RFM ANALYSIS (Customer Segmentation) ---

# Snapshot date = one day after last purchase
snapshot_date = df["InvoiceDate"].max() + pd.Timedelta(days=1)

rfm = df.groupby("CustomerID").agg({
    "InvoiceDate": lambda x: (snapshot_date - x.max()).days,  # Recency
    "InvoiceNo": "nunique",                                   # Frequency
    "Revenue": "sum"                                          # Monetary
})

rfm.columns = ["Recency", "Frequency", "Monetary"]

print("\nRFM Sample:")
print(rfm.head())

# Flag churn risk:
# Customers who bought only once and haven't returned in 90+ days
rfm["ChurnRisk"] = np.where(
    (rfm["Recency"] > 90) & (rfm["Frequency"] == 1),
    "High Risk",
    "Low Risk"
)

print("\nChurn Risk Distribution:")
print(rfm["ChurnRisk"].value_counts())

# Save for later use in BI / SQL
rfm.to_csv("../data/rfm_customers.csv")
print("\nRFM table saved as data/rfm_customers.csv")

# --- RFM ANALYSIS (Customer Segmentation) ---

snapshot_date = df["InvoiceDate"].max() + pd.Timedelta(days=1)

rfm = df.groupby("CustomerID").agg(
    Recency=("InvoiceDate", lambda x: (snapshot_date - x.max()).days),
    Frequency=("InvoiceNo", "nunique"),
    Monetary=("Revenue", "sum")
)

print("\nRFM Sample:")
print(rfm.head())

rfm["ChurnRisk"] = np.where(
    (rfm["Recency"] > 90) & (rfm["Frequency"] == 1),
    "High Risk",
    "Low Risk"
)

print("\nChurn Risk Distribution:")
print(rfm["ChurnRisk"].value_counts())

rfm.to_csv("../data/rfm_customers.csv", index=True)
print("\nRFM table saved as data/rfm_customers.csv")

print("\n✅ REACHED END OF SCRIPT")
