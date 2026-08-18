"""
Day 1 Python Practice — RFM Segmentation from Scratch
Dataset: practice_orders.csv (order_id, customer_id, order_date, order_value)

Do NOT look at your old RFM notebook. Build this fresh using only pandas.
Fill in each TODO. Print outputs after each step to sanity-check yourself.
"""
import pandas as pd

# ---- Load data ----
df = pd.read_csv("practice_orders.csv", parse_dates=["order_date"])
print(df.head())
# print(df.dtypes)

# ---- Step 1: Set your "analysis date" ----
# This is the reference point for calculating Recency (usually: day after last order in dataset, or today's date)
# TODO: set analysis_date = the day after the max order_date in the dataset

analysis_date = (df["order_date"].max() + pd.Timedelta(days = 1))
print(analysis_date)


# ---- Step 2: Calculate Recency, Frequency, Monetary per customer ----
# Recency  = days between analysis_date and each customer's most recent order
# Frequency = count of orders per customer
# Monetary = sum of order_value per customer
#
# Hint: you'll need a groupby('customer_id').agg({...}) with a custom recency calc
# TODO: build a dataframe `rfm` with columns: customer_id, recency, frequency, monetary
recency = (
    analysis_date - df.groupby("customer_id")["order_date"].max()
).dt.days

frequency = df.groupby("customer_id")["order_id"].count()
monetary = df.groupby("customer_id")["order_value"].sum()

rfm = pd.DataFrame({
    "customer_id" : recency.index,
    "Recency" : recency.values,
    "Frequency" : frequency.values,
    "Monetary" : monetary.values
})

# print(rfm)

# ---- Step 3: Score each dimension 1-5 using quantiles ----
# Use pd.qcut() to bucket each of R, F, M into 5 quantile-based groups
# IMPORTANT: Recency is inverted — LOWER recency (more recent) = HIGHER score (5)
#            Frequency/Monetary — HIGHER value = HIGHER score (5)
# TODO: create rfm['R_score'], rfm['F_score'], rfm['M_score'] (each 1-5)
rfm["R_score"] = pd.qcut(rfm["Recency"], 5, labels=[5, 4, 3, 2, 1])
rfm["F_score"] = pd.qcut(
    rfm["Frequency"].rank(method="first"),
    5,
    labels=[1, 2, 3, 4, 5]
)
rfm["M_score"] = pd.qcut(rfm["Monetary"], 5, labels=[1, 2, 3, 4, 5])

# print(rfm)


# ---- Step 4: Combine into RFM segment label ----
# TODO: create rfm['RFM_score'] = R_score + F_score + M_score (or concatenate as string "543")
rfm["RFM_score"] = ( 
    rfm["R_score"].astype(int) 
    + rfm["F_score"].astype(int) 
    + rfm["M_score"].astype(int) 
)
# print(rfm)

# ---- Step 5: Bucket customers into named segments ----
# e.g. RFM_score >= 12 -> "Champions"
#      RFM_score 9-11  -> "Loyal"
#      RFM_score 6-8   -> "At Risk"
#      RFM_score < 6   -> "Lost"
# TODO: create rfm['segment'] using pd.cut() or a custom function + .apply()
rfm['segment'] = pd.cut(rfm["RFM_score"], bins = [0, 5, 8, 11, float("inf")], labels= ["Lost", "At Risk", "Loyal", "Champions"])
# print(rfm)

# ---- Step 6: Sanity check your output ----
# TODO: print value_counts() of rfm['segment']
# print(rfm["segment"].value_counts())

# TODO: print the top 5 customers by monetary value and confirm their segment makes sense
top_5 = rfm.sort_values("Monetary", ascending=False).head(5)
# print(top_5[["customer_id", "Monetary", "RFM_score", "segment"]])

# ---- Stretch goal (if you finish early) ----
# TODO: which segment has the highest average order_value?
df_with_segment = df.merge(
    rfm[["customer_id", "segment"]],
    on="customer_id",
    how="left"
)

avg_order_value = df_with_segment.groupby("segment")["order_value"].mean()
print(avg_order_value)

# TODO: what % of total revenue comes from "Champions"? (this is the kind of insight interviewers want you to surface unprompted)
champions_revenue = rfm.loc[rfm["segment"] == "Champions", "Monetary"].sum()
total_revenue = rfm["Monetary"].sum()
champions_revenue_pct = round(((champions_revenue / total_revenue) * 100),2)
print(champions_revenue_pct)