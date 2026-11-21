from pathlib import Path
import pandas as pd
import numpy as np

DATA_PATH = Path(__file__).parent / "data" / "superstore_sales.csv"

def load_data(path=DATA_PATH):
    df = pd.read_csv(path, parse_dates=["Order Date", "Ship Date"])
    df.columns = df.columns.str.strip()
    df["City"] = df["City"].fillna("Unknown")
    df["Discount"] = df["Discount"].fillna(0)
    df = df.drop_duplicates(subset=["Order ID"])
    df = df[(df["Sales"] >= 0) & (df["Quantity"] > 0)]
    df["Month"] = df["Order Date"].dt.to_period("M").astype(str)
    df["Year"] = df["Order Date"].dt.year
    df["Profit Margin"] = np.where(df["Sales"] != 0, df["Profit"] / df["Sales"] * 100, 0)
    return df

def get_kpis(df):
    return {
        "total_sales": float(df["Sales"].sum()),
        "total_profit": float(df["Profit"].sum()),
        "total_orders": int(df["Order ID"].nunique()),
        "total_quantity": int(df["Quantity"].sum()),
        "profit_margin": float(df["Profit"].sum()/df["Sales"].sum()*100) if df["Sales"].sum() else 0,
        "average_order_value": float(df.groupby("Order ID")["Sales"].sum().mean())
    }

def monthly_sales(df):
    return df.groupby("Month", as_index=False).agg(Sales=("Sales","sum"), Profit=("Profit","sum"))

def category_performance(df):
    return df.groupby("Category", as_index=False).agg(Sales=("Sales","sum"), Profit=("Profit","sum"), Quantity=("Quantity","sum")).sort_values("Sales", ascending=False)

def regional_performance(df):
    return df.groupby("Region", as_index=False).agg(Sales=("Sales","sum"), Profit=("Profit","sum"), Orders=("Order ID","nunique")).sort_values("Sales", ascending=False)

def top_products(df, n=10):
    return df.groupby("Product Name", as_index=False).agg(Sales=("Sales","sum"), Profit=("Profit","sum"), Quantity=("Quantity","sum")).sort_values("Sales", ascending=False).head(n)

def discount_analysis(df):
    return df.groupby("Discount", as_index=False).agg(Sales=("Sales","sum"), Profit=("Profit","sum"), Orders=("Order ID","nunique")).sort_values("Discount")

if __name__ == "__main__":
    data = load_data()
    print("KPI SUMMARY")
    for k,v in get_kpis(data).items():
        print(f"{k}: {v:,.2f}" if isinstance(v,float) else f"{k}: {v:,}")
    print("\nCATEGORY PERFORMANCE\n", category_performance(data).to_string(index=False))
    print("\nREGIONAL PERFORMANCE\n", regional_performance(data).to_string(index=False))
    print("\nTOP 10 PRODUCTS\n", top_products(data).to_string(index=False))
