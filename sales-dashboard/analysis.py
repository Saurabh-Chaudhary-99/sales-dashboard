import pandas as pd
import matplotlib.pyplot as plt


# Load dataset
df = pd.read_csv("data/sales.csv")

# Show first 5 rows
print(df.head())

# Check columns
print("\nColumns:\n", df.columns)

# Check missing values
print("\nMissing values:\n", df.isnull().sum())

df["Order Date"] = pd.to_datetime(df["Order Date"],dayfirst=True)

#create new columns
df["Year"] = df["Order Date"].dt.year
df["Month"] = df["Order Date"].dt.month
df["Month Name"] = df["Order Date"].dt.strftime("%b")

print("\nConverted Date Columns:")
print(df[["Order Date", "Year", "Month", "Month Name"]].head())

# Basic info
# print("\nInfo:")
# print(df.info())

# Correct month order
month_order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
               "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

df["Month Name"] = pd.Categorical(df["Month Name"], categories=month_order, ordered=True)

# Monthly sales
monthly_sales = df.groupby("Month Name")["Sales"].sum().sort_index()

print("\nMonthly Sales:\n", monthly_sales)

# Plot
monthly_sales.plot(kind="bar")
plt.title("Monthly Sales Trend")
plt.xlabel("Month")
plt.ylabel("Total Sales")
plt.xticks(rotation=45)
plt.show()

# Top 5 products by sales
top_products = df.groupby("Product Name")["Sales"].sum().sort_values(ascending=False).head(5)

print("\nTop 5 Products:\n", top_products)

# Plot
plt.figure(figsize=(12, 7))
top_products.plot(kind="barh")
plt.title("Top 5 Products by Sales")
plt.xlabel("Sales")
plt.ylabel("Product")
plt.tight_layout()
plt.show()

# Top 5 customers by sales
top_customers = df.groupby("Customer Name")["Sales"].sum().sort_values(ascending=False).head(5)

print("\nTop 5 Customers:\n", top_customers)

# Plot
plt.figure(figsize=(10, 6))
top_customers.plot(kind="barh")

plt.title("Top 5 Customers by Sales")
plt.xlabel("Sales")
plt.ylabel("Customer")

plt.tight_layout()
plt.show()

# Region-wise sales
region_sales = df.groupby("Region")["Sales"].sum().sort_values(ascending=False)

print("\nRegion-wise Sales:\n", region_sales)

# Plot
plt.figure(figsize=(8, 5))
region_sales.plot(kind="bar")

plt.title("Sales by Region")
plt.xlabel("Region")
plt.ylabel("Total Sales")

plt.xticks(rotation=45)
plt.tight_layout()
plt.show()