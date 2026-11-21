import streamlit as st
import pandas as pd
import plotly.express as px
from analysis import load_data, get_kpis, monthly_sales, category_performance, regional_performance, top_products, discount_analysis

st.set_page_config(page_title="Business Sales Analytics", page_icon="📊", layout="wide")
st.title("📊 Business Sales Performance Analytics")
st.caption("Future Interns | Data Science & Analytics | Task 1")
st.info("Dataset note: This project uses a reproducible synthetic Superstore-style dataset for demonstration and portfolio practice.")

df = load_data()
with st.sidebar:
    st.header("Dashboard Filters")
    regions = st.multiselect("Region", sorted(df["Region"].unique()), default=sorted(df["Region"].unique()))
    categories = st.multiselect("Category", sorted(df["Category"].unique()), default=sorted(df["Category"].unique()))
    date_min, date_max = df["Order Date"].min().date(), df["Order Date"].max().date()
    date_range = st.date_input("Order date range", value=(date_min, date_max), min_value=date_min, max_value=date_max)

filtered = df[df["Region"].isin(regions) & df["Category"].isin(categories)].copy()
if isinstance(date_range, tuple) and len(date_range) == 2:
    filtered = filtered[(filtered["Order Date"].dt.date >= date_range[0]) & (filtered["Order Date"].dt.date <= date_range[1])]

if filtered.empty:
    st.warning("No records match the selected filters.")
    st.stop()

k = get_kpis(filtered)
c1,c2,c3,c4,c5 = st.columns(5)
c1.metric("Total Sales", f"${k['total_sales']:,.0f}")
c2.metric("Total Profit", f"${k['total_profit']:,.0f}")
c3.metric("Orders", f"{k['total_orders']:,}")
c4.metric("Units Sold", f"{k['total_quantity']:,}")
c5.metric("Profit Margin", f"{k['profit_margin']:.1f}%")

st.subheader("Revenue and Profit Trends")
m = monthly_sales(filtered)
fig = px.line(m, x="Month", y=["Sales","Profit"], markers=True, title="Monthly Sales and Profit")
st.plotly_chart(fig, use_container_width=True)

left,right = st.columns(2)
with left:
    st.subheader("Category Performance")
    cp = category_performance(filtered)
    st.plotly_chart(px.bar(cp, x="Category", y="Sales", color="Category", title="Sales by Category"), use_container_width=True)
with right:
    st.subheader("Regional Performance")
    rp = regional_performance(filtered)
    st.plotly_chart(px.bar(rp, x="Region", y="Sales", color="Region", title="Sales by Region"), use_container_width=True)

left,right = st.columns(2)
with left:
    st.subheader("Top 10 Products")
    tp = top_products(filtered)
    st.plotly_chart(px.bar(tp.sort_values("Sales"), x="Sales", y="Product Name", orientation="h", title="Top Products by Sales"), use_container_width=True)
with right:
    st.subheader("Discount vs Profit")
    da = discount_analysis(filtered)
    st.plotly_chart(px.bar(da, x="Discount", y="Profit", title="Total Profit by Discount Level"), use_container_width=True)

st.subheader("Detailed Tables")
tab1,tab2,tab3 = st.tabs(["Categories","Regions","Top Products"])
with tab1: st.dataframe(cp, use_container_width=True)
with tab2: st.dataframe(rp, use_container_width=True)
with tab3: st.dataframe(tp, use_container_width=True)

st.subheader("Business Recommendations")
st.markdown("""
- Prioritize categories and products that combine high sales with healthy profit.
- Investigate regions with strong revenue but weak profit margins before increasing spend.
- Review high-discount transactions and establish discount approval thresholds.
- Monitor monthly sales and profit together; revenue growth alone does not guarantee profitability.
- Use the dashboard filters to compare segments, regions and time periods before making decisions.
""")
st.download_button("Download filtered data (CSV)", filtered.to_csv(index=False).encode("utf-8"), "filtered_sales_data.csv", "text/csv")
