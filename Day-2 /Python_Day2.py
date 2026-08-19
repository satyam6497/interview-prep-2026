import pandas as pd

orders = pd.read_csv("practice_orders_with_status.csv", parse_dates= ["order_date"])
customers = pd.read_csv("practice_customers.csv", parse_dates=["signup_date"])

# print(customers.head())
# print(orders.head())

# =================================================================
# PART 1: FUNNEL MATH IN PANDAS (mirrors your SQL query #9 from Day 1)
# =================================================================
# Goal: for each acquisition_channel -> total orders, delivered, cancelled,
#       returned, and % delivered.
#
# Do this WITHOUT writing raw SQL. Think: merge, groupby, then either
# pivot_table or crosstab, or groupby + apply with a lambda.
 
# TODO: merge orders with customers on customer_id
df = pd.merge(customers, orders, on="customer_id", how="inner")
# print(df.head())
# TODO: build a table of acquisition_channel x status counts
#   Hint: pd.crosstab(merged['acquisition_channel'], merged['status']) is one clean way
Table1 = pd.crosstab(df['acquisition_channel'], df['status'])
# print(Table1.head())
 
# TODO: add a '% Delivered' column = Delivered / (Delivered+Cancelled+Returned) * 100
Table1['%Delivered'] = round(((Table1['Delivered'] / (Table1["Delivered"] + Table1["Cancelled"] + Table1["Returned"]))*100),2).astype(str) + "%"
# print(Table1.head())

 
 
# =================================================================
# PART 2: COHORT / RETENTION ANALYSIS
# =================================================================
# Goal: group customers by the MONTH they signed up (their "cohort"),
#       then see what % of each cohort placed an orde.apply(lambda x: x.n)r in each subsequent month.
# This is a genuinely hard pandas exercise - don't rush it.
 
# Step A: create a 'signup_month' column on customers (e.g. "2024-01")
# TODO
customers['signup_month'] = customers['signup_date'].dt.to_period('M')
# print(customers.head())
 
# Step B: create an 'order_month' column on orders
# TODO
orders['order_month'] = orders['order_date'].dt.to_period('M')
# print(orders.head())
 
# Step C: merge orders with customers (bring signup_month onto each order)
# TODO
Table2 = pd.merge(customers, orders, how = "inner", on= "customer_id")
# print(Table2.head())
 
# Step D: calculate "months since signup" for each order
#   Hint: this needs signup_month and order_month both as Period('M') objects,
#   then subtract them - the result is an integer number of months.
# TODO
Table2["months_since_signup"] = (Table2["order_month"] - Table2["signup_month"]).apply(lambda x: x.n)
# print(Table2.head())
 
# Step E: build the cohort table
#   Rows = signup_month (cohort), Columns = months_since_signup, Values = count of DISTINCT customers who ordered
#   Hint: groupby(['signup_month','months_since_signup'])['customer_id'].nunique().unstack()
# TODO
cohort_table = Table2.groupby(['signup_month','months_since_signup'])['customer_id'].nunique().unstack()
# print(cohort_table.head())
 
# Step F: convert counts to retention % (divide each row by that cohort's month-0 value)
# TODO
cohort_table = cohort_table.div(cohort_table.iloc[:, 0], axis=0) * 100
# print(cohort_table.head())
 
 
# Step G: print the retention table. This IS a cohort retention matrix -
#   the exact kind of table a growth/product analyst builds constantly.
print(cohort_table)

 
 
# =================================================================
# PART 3: CORRELATION CHECK
# =================================================================
# Goal: is there any relationship between how early a customer signed up
#       (tenure) and their total spend?
 
# TODO: calculate each customer's tenure in days (today - signup_date, or use a fixed reference date)
customers['tenure_days'] = (pd.Timestamp.today() - customers['signup_date']).dt.days
# TODO: calculate each customer's total order_value (sum)
customer_order_values = orders.groupby('customer_id')['order_value'].sum().reset_index()
customers = pd.merge(customers, customer_order_values, on='customer_id', how='left')

# TODO: merge these into one dataframe and run .corr() between tenure and total spend
correlation = customers['tenure_days'].corr(customers['order_value'])

# TODO: print the correlation coefficient and write ONE sentence interpreting it
#   (correlation near 0? weak positive? weak negative? what would you tell a stakeholder?)
print(f"Correlation between tenure and total spend: {correlation}")
