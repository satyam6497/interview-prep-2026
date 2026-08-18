import sqlite3
import pandas as pd

conn = sqlite3.connect('SQL/SQLite_Practice/practice.db')
cursor = conn.cursor()


# Q1.List each order with the customer's city and acquisition_channel.
query1 = """
SELECT o.order_id, c.city, c.acquisition_channel
FROM orders o
JOIN customers c
ON o.customer_id = c.customer_id;
"""

# df = pd.read_sql_query(query1, conn)
# print(df)

# Q2. Total revenue (sum of order_value) and number of orders, per city only include Delivered orders.
query2 = """
SELECT c.city,
SUM(o.order_value) as Total_Revenue,
SUM(o.order_id) as No_of_orders
FROM orders o
JOIN customers c
ON o.customer_id = c.customer_id
WHERE o.status = "Delivered"
GROUP BY c.city;
"""

# df = pd.read_sql_query(query2, conn)
# print(df)

#Q3. Which cities have more than 100 delivered orders?
query3 = """
SELECT c.city, COUNT(*) as Delievered_Orders
FROM customers c
JOIN orders o
ON o.customer_id = c.customer_id
WHERE o.status = "Delivered"
GROUP BY c.city
HAVING COUNT(*) > 100;
"""

# df = pd.read_sql_query(query3, conn)
# print(df)

# Q4. Find customers who have NEVER placed an order.
query4 = """
SELECT c.customer_id
FROM customers c
LEFT JOIN orders o
ON o.customer_id = c.customer_id
WHERE o.order_id IS NULL;
"""
# df = pd.read_sql_query(query4, conn)
# print(df)

#Q5. Find all orders with order_value greater than the overall average order_value.
query5 = """
SELECT o.order_id
FROM orders o
where o.order_value > (SELECT AVG(order_value)
                       FROM orders
);
"""
# df = pd.read_sql_query(query5, conn)
# print(df)

#Q6. Find customers who have placed at least one Cancelled order.
query6 = """
SELECT DISTINCT c.customer_id
FROM customers c
JOIN orders o
ON o.customer_id = c.customer_id
WHERE o.status = "Cancelled";
"""
# df = pd.read_sql_query(query6, conn)
# print(df)

#Q7.For each acquisition_channel, show total revenue and average order value, Delivered orders only.
query7 = """
SELECT c.acquisition_channel,
SUM(o.order_value) as total_revenue,
AVG(o.order_value) as average_order_value
FROM customers c
JOIN orders o
ON o.customer_id = c.customer_id
WHERE o.status = "Delivered"
GROUP BY c.acquisition_channel;
"""
# df = pd.read_sql_query(query7, conn)
# print(df)

# Q8.For each customer, find the number of days between their signup_date and their FIRST order_date.
query8 = """
SELECT c.customer_id, c.signup_date,
JULIANDAY(MIN(o.order_date)) - JULIANDAY(c.signup_date) AS date_difference
FROM customers c
JOIN orders o
ON o.customer_id = c.customer_id
GROUP BY c.customer_id, c.signup_date;
"""
# df = pd.read_sql_query(query8, conn)
# print(df)

 
# Q9.For each acquisition_channel, calculate: total orders, delivered orders, cancelled orders, returned orders, and the % delivered (delivered / total * 100)
query9 = """
SELECT c.acquisition_channel, COUNT(o.order_id) AS total_orders,
SUM(CASE WHEN o.status = "Delivered" THEN 1 ELSE 0 END) AS delivered_orders,
SUM(CASE WHEN o.status = "Cancelled" THEN 1 ELSE 0 END) AS cancelled_orders,
SUM(CASE WHEN o.status = "Returned" THEN 1 ELSE 0 END) AS returned_orders,
(SUM(CASE WHEN o.status = "Delivered" THEN 1 ELSE 0 END)*100)/COUNT(o.order_id) AS "%_delivered"
FROM customers c
JOIN orders o
ON o.customer_id = c.customer_id
GROUP BY c.acquisition_channel;
"""
# df = pd.read_sql_query(query9, conn)
# print(df)


#Q10. Find the top 3 customers by total revenue (sum of order_value, Delivered only).
query10 = """
SELECT customer_id, SUM(order_value) AS total_revenue
FROM orders
WHERE status = 'Delivered'
GROUP BY customer_id
ORDER BY total_revenue DESC
LIMIT 3;
"""
df = pd.read_sql_query(query10, conn)
print(df)
conn.close()
