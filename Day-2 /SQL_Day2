import sqlite3
import pandas as pd

conn = sqlite3.connect('practice2.db')

# -- 1. ROW_NUMBER
query1 = '''
SELECT c.customer_id, ROW_NUMBER() OVER (PARTITION BY c.customer_id ORDER BY o.order_date) as rnk
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id;
'''
print("--- Q1: ROW_NUMBER ---")
print(pd.read_sql_query(query1, conn).head(), "\n")

# -- 2. RANK vs DENSE_RANK
query2 = '''
WITH CustomerRevenue AS (
    SELECT customer_id, SUM(order_value) as total_revenue
    FROM orders
    WHERE status = 'Delivered'
    GROUP BY customer_id
)
SELECT customer_id, 
       total_revenue,
       RANK() OVER (ORDER BY total_revenue DESC) as rank_standard,
       DENSE_RANK() OVER (ORDER BY total_revenue DESC) as rank_dense
FROM CustomerRevenue;
'''
print("--- Q2: RANK vs DENSE_RANK ---")
print(pd.read_sql_query(query2, conn).head(), "\n")

# -- 3. TOP-N PER GROUP 
query3 = '''
WITH RankedOrders AS (
    SELECT c.acquisition_channel, o.order_id, o.order_value,
           ROW_NUMBER() OVER (PARTITION BY c.acquisition_channel ORDER BY o.order_value DESC) as rn
    FROM orders o
    JOIN customers c ON o.customer_id = c.customer_id
)
SELECT acquisition_channel, order_id, order_value
FROM RankedOrders
WHERE rn <= 2;
'''
print("--- Q3: TOP-N PER GROUP ---")
print(pd.read_sql_query(query3, conn).head(6), "\n")

# -- 4. LAG / LEAD
query4 = '''
SELECT customer_id, order_date,
       LAG(order_date) OVER (PARTITION BY customer_id ORDER BY order_date) as previous_order,
       CAST(julianday(order_date) - julianday(LAG(order_date) OVER (PARTITION BY customer_id ORDER BY order_date)) AS INTEGER) as days_between
FROM orders;
'''
print("--- Q4: LAG / LEAD ---")
print(pd.read_sql_query(query4, conn).head(), "\n")

# -- 5. RUNNING TOTAL
query5 = '''
SELECT order_id, order_date, order_value,
       SUM(order_value) OVER (ORDER BY order_date) as running_revenue
FROM orders
WHERE status = 'Delivered';
'''
print("--- Q5: RUNNING TOTAL ---")
print(pd.read_sql_query(query5, conn).head(), "\n")

# -- 6. RUNNING TOTAL PER GROUP
query6 = '''
SELECT c.acquisition_channel, o.order_id, o.order_date, o.order_value,
       SUM(o.order_value) OVER (PARTITION BY c.acquisition_channel ORDER BY o.order_date) as channel_running_total
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
WHERE o.status = 'Delivered';
'''
print("--- Q6: RUNNING TOTAL PER GROUP ---")
print(pd.read_sql_query(query6, conn).head(), "\n")

# -- 7. MOVING AVERAGE
query7 = '''
SELECT customer_id, order_id, order_date, order_value,
       AVG(order_value) OVER (
           PARTITION BY customer_id 
           ORDER BY order_date 
           ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
       ) as moving_avg_3_orders
FROM orders;
'''
print("--- Q7: MOVING AVERAGE ---")
print(pd.read_sql_query(query7, conn).head(), "\n")

# -- 8. NTILE
query8 = '''
WITH CustRev AS (
    SELECT customer_id, SUM(order_value) as total_revenue
    FROM orders
    GROUP BY customer_id
)
SELECT customer_id, total_revenue,
       NTILE(4) OVER (ORDER BY total_revenue DESC) as revenue_quartile
FROM CustRev;
'''
print("--- Q8: NTILE ---")
print(pd.read_sql_query(query8, conn).head(), "\n")

# -- 9. FIRST_VALUE
query9 = '''
SELECT DISTINCT customer_id,
       FIRST_VALUE(order_date) OVER (PARTITION BY customer_id ORDER BY order_date) as first_order_date,
       FIRST_VALUE(order_value) OVER (PARTITION BY customer_id ORDER BY order_date) as first_order_value
FROM orders;
'''
print("--- Q9: FIRST_VALUE ---")
print(pd.read_sql_query(query9, conn).head(), "\n")

# -- 10. COMBINING LOGIC (CTEs + Window)
query10 = '''
WITH ChannelStats AS (
    SELECT c.acquisition_channel,
           SUM(CASE WHEN o.status = 'Delivered' THEN 1.0 ELSE 0 END) / COUNT(o.order_id) * 100 as pct_delivered
    FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
    GROUP BY c.acquisition_channel
)
SELECT acquisition_channel, pct_delivered,
       RANK() OVER (ORDER BY pct_delivered DESC) as channel_rank
FROM ChannelStats;
'''
print("--- Q10: CHANNEL RANKING ---")
print(pd.read_sql_query(query10, conn), "\n")

# -- STRETCH: Declining Spend (At-Risk Signal)
query_stretch = '''
WITH OrderHistory AS (
    SELECT customer_id, order_id, order_date, order_value,
           LAG(order_value) OVER (PARTITION BY customer_id ORDER BY order_date) as prev_order_value,
           ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date DESC) as recency_rank
    FROM orders
)
SELECT customer_id, order_value as latest_order_value, prev_order_value
FROM OrderHistory
WHERE recency_rank = 1 
  AND prev_order_value IS NOT NULL 
  AND order_value < prev_order_value;
'''
print("--- STRETCH: AT-RISK CUSTOMERS ---")
print(pd.read_sql_query(query_stretch, conn).head())

conn.close()
