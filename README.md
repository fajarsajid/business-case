# 📊 Business Case: E-Commerce Revenue & Customer Analytics

This project simulates a real-world data analyst workflow for an online retail business.  
It covers the full analytics pipeline:

- Raw data ingestion  
- Data cleaning & feature engineering (Python)  
- Revenue trend analysis  
- Customer segmentation using RFM  
- Data warehousing in PostgreSQL  
- Business-driven SQL analytics  
- Version-controlled portfolio project  

The goal is to answer **business questions** such as:

- How is revenue trending over time?
- Who are the most valuable customers?
- Which customers are at risk of churn?
- How can the business increase repeat purchases?

---

## 🧱 Tech Stack

- **Python** – pandas, matplotlib
- **PostgreSQL** – data warehouse & analytics
- **SQL** – business queries
- **Git/GitHub** – version control & portfolio hosting

---

## 📂 Project Structure

business-case/
├── data/
│   ├── online_retail.csv        # Raw dataset
│   ├── cleaned_retail.csv       # Cleaned dataset (Python)
│   └── rfm_customers.csv        # RFM segmentation output
├── notebooks/
│   └── business_case_analysis.py
├── sql/
│   └── analysis_queries.sql     # Business SQL queries
└── README.md

---

## 🧼 Data Cleaning (Python)

Using `pandas`, the script:

- Removes null and invalid rows  
- Converts dates and numeric fields  
- Creates a `Revenue = Quantity * UnitPrice` column  
- Saves a clean dataset for analysis  

```python
df = df.dropna()
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
df["Revenue"] = df["Quantity"] * df["UnitPrice"]
df.to_csv("data/cleaned_retail.csv", index=False)
