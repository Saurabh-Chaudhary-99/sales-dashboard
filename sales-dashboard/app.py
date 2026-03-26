import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------
# 🔥 Page Config
# -----------------------------
st.set_page_config(page_title="Sales Dashboard", layout="wide")

# -----------------------------
# 📥 Load Data
# -----------------------------
df = pd.read_csv("data/sales.csv")

# -----------------------------
# 🧹 Data Processing
# -----------------------------
df["Order Date"] = pd.to_datetime(df["Order Date"], dayfirst=True)
df["Month Name"] = df["Order Date"].dt.strftime("%b")

month_order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
               "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

df["Month Name"] = pd.Categorical(df["Month Name"], categories=month_order, ordered=True)

# -----------------------------
# 🎛️ Sidebar Filters
# -----------------------------
st.sidebar.header("🔍 Filters")

# Date filter
min_date = df["Order Date"].min()
max_date = df["Order Date"].max()

date_range = st.sidebar.date_input(
    "Select Date Range",
    [min_date, max_date],
    min_value=min_date,
    max_value=max_date
)

# Apply date filter
if len(date_range) == 2:
    start_date, end_date = date_range
    df = df[(df["Order Date"] >= pd.to_datetime(start_date)) &
            (df["Order Date"] <= pd.to_datetime(end_date))]

# Region filter
selected_region = st.sidebar.multiselect(
    "Select Region",
    options=df["Region"].unique(),
    default=df["Region"].unique()
)

# Category filter
selected_category = st.sidebar.multiselect(
    "Select Category",
    options=df["Category"].unique(),
    default=df["Category"].unique()
)

# Final filtered data
filtered_df = df[
    (df["Region"].isin(selected_region)) &
    (df["Category"].isin(selected_category))
]

# -----------------------------
# 🏷️ Title
# -----------------------------
st.title("📊 Sales Dashboard")

# -----------------------------
# 📊 KPIs
# -----------------------------
total_sales = int(filtered_df["Sales"].sum())
total_orders = filtered_df["Order ID"].nunique()
total_customers = filtered_df["Customer Name"].nunique()

col1, col2, col3 = st.columns(3)

col1.metric("💰 Total Sales", f"${total_sales}")
col2.metric("📦 Total Orders", total_orders)
col3.metric("👥 Customers", total_customers)

st.markdown("---")

# -----------------------------
# 📈 Monthly Sales
# -----------------------------
st.subheader("📈 Monthly Sales Trend")

monthly_sales = filtered_df.groupby("Month Name")["Sales"].sum().sort_index()

fig1, ax1 = plt.subplots()
monthly_sales.plot(kind="bar", ax=ax1)
plt.xticks(rotation=45)
st.pyplot(fig1)

# -----------------------------
# 🏆 Top Products
# -----------------------------
st.subheader("🏆 Top 5 Products")

top_products = filtered_df.groupby("Product Name")["Sales"].sum().sort_values(ascending=False).head(5)

fig2, ax2 = plt.subplots(figsize=(10, 6))
top_products.plot(kind="barh", ax=ax2)
plt.tight_layout()
st.pyplot(fig2)

# -----------------------------
# 👥 Top Customers
# -----------------------------
st.subheader("👥 Top 5 Customers")

top_customers = filtered_df.groupby("Customer Name")["Sales"].sum().sort_values(ascending=False).head(5)

fig3, ax3 = plt.subplots(figsize=(10, 6))
top_customers.plot(kind="barh", ax=ax3)
plt.tight_layout()
st.pyplot(fig3)

# -----------------------------
# 🌍 Region Sales
# -----------------------------
st.subheader("🌍 Sales by Region")

region_sales = filtered_df.groupby("Region")["Sales"].sum().sort_values(ascending=False)

fig4, ax4 = plt.subplots()
region_sales.plot(kind="bar", ax=ax4)
plt.xticks(rotation=45)
st.pyplot(fig4)

# -----------------------------
# 🥧 Category Sales Pie
# -----------------------------
st.subheader("📊 Sales by Category")

category_sales = filtered_df.groupby("Category")["Sales"].sum()

fig5, ax5 = plt.subplots()
category_sales.plot(kind="pie", autopct='%1.1f%%', ax=ax5)
ax5.set_ylabel("")
st.pyplot(fig5)

# -----------------------------
# 📉 Time Series Trend
# -----------------------------
st.subheader("📉 Sales Trend Over Time")

time_sales = filtered_df.groupby("Order Date")["Sales"].sum()

fig6, ax6 = plt.subplots()
time_sales.plot(ax=ax6)
plt.xticks(rotation=45)
st.pyplot(fig6)

# -----------------------------
# 🧠 Key Insights
# -----------------------------
st.markdown("---")
st.subheader("🧠 Key Insights")

top_product = filtered_df.groupby("Product Name")["Sales"].sum().idxmax()
top_customer = filtered_df.groupby("Customer Name")["Sales"].sum().idxmax()
top_region = filtered_df.groupby("Region")["Sales"].sum().idxmax()

st.write(f"🏆 Top Product: **{top_product}**")
st.write(f"👤 Top Customer: **{top_customer}**")
st.write(f"🌍 Top Region: **{top_region}**")

# -----------------------------
# 📋 Data Preview
# -----------------------------
st.markdown("---")
st.subheader("📋 Data Preview")

st.dataframe(filtered_df.head(50))

# -----------------------------
# 📥 Download Button
# -----------------------------
csv = filtered_df.to_csv(index=False).encode('utf-8')

st.download_button(
    label="📥 Download Filtered Data",
    data=csv,
    file_name="filtered_sales.csv",
    mime="text/csv"
)