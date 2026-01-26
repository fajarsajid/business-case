-- Monthly revenue trend
SELECT DATE_TRUNC('month', invoicedate) AS month,
       ROUND(SUM(revenue), 2) AS total_revenue
FROM ecommerce
GROUP BY 1
ORDER BY 1;

-- Top 10 products by revenue
SELECT description,
       ROUND(SUM(revenue), 2) AS product_revenue
FROM ecommerce
GROUP BY 1
ORDER BY product_revenue DESC
LIMIT 10;

-- Repeat customer percentage
WITH purchases AS (
  SELECT customerid, COUNT(DISTINCT invoiceno) AS orders
  FROM ecommerce
  GROUP BY 1
)
SELECT
  ROUND(COUNT(*) FILTER (WHERE orders > 1) * 100.0 / COUNT(*), 2) AS repeat_customer_pct
FROM purchases;

-- Top 10 customers by lifetime revenue
SELECT customerid,
       ROUND(SUM(revenue), 2) AS lifetime_revenue
FROM ecommerce
GROUP BY 1
ORDER BY lifetime_revenue DESC
LIMIT 10;

-- Revenue by country (top 10)
SELECT country,
       ROUND(SUM(revenue), 2) AS total_revenue
FROM ecommerce
GROUP BY 1
ORDER BY total_revenue DESC
LIMIT 10;

-- Month-over-month revenue growth
WITH monthly AS (
  SELECT DATE_TRUNC('month', invoicedate) AS month,
         SUM(revenue) AS revenue
  FROM ecommerce
  GROUP BY 1
)
SELECT month,
       ROUND(revenue, 2) AS revenue,
       ROUND(
         (revenue - LAG(revenue) OVER (ORDER BY month))
         / NULLIF(LAG(revenue) OVER (ORDER BY month), 0) * 100.0,
       2) AS mom_growth_pct
FROM monthly
ORDER BY month;