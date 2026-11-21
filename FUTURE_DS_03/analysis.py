from pathlib import Path
import pandas as pd
import numpy as np

DATA = Path(__file__).parent / "data" / "marketing_funnel.csv"

def load_data(path=DATA):
    df = pd.read_csv(path, parse_dates=["LeadDate"])
    required = ["LeadID","Channel","Campaign","LandingPageVisited","FormSubmitted",
                "QualifiedLead","DemoScheduled","Converted","MarketingSpend","Revenue"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
    return df

def funnel_summary(df):
    stages = [
        ("Leads", len(df)),
        ("Landing Page Visits", int(df["LandingPageVisited"].sum())),
        ("Form Submissions", int(df["FormSubmitted"].sum())),
        ("Qualified Leads", int(df["QualifiedLead"].sum())),
        ("Demos Scheduled", int(df["DemoScheduled"].sum())),
        ("Conversions", int(df["Converted"].sum()))
    ]
    out = pd.DataFrame(stages, columns=["Stage","Count"])
    out["ConversionFromPreviousPct"] = [100.0] + [
        (out.loc[i,"Count"] / out.loc[i-1,"Count"] * 100
         if out.loc[i-1,"Count"] else 0.0) for i in range(1,len(out))
    ]
    out["ConversionFromLeadsPct"] = out["Count"] / len(df) * 100
    return out

def channel_performance(df):
    out = df.groupby("Channel").agg(
        Leads=("LeadID","count"), Visits=("LandingPageVisited","sum"),
        Forms=("FormSubmitted","sum"), Qualified=("QualifiedLead","sum"),
        Demos=("DemoScheduled","sum"), Conversions=("Converted","sum"),
        Spend=("MarketingSpend","sum"), Revenue=("Revenue","sum")
    ).reset_index()
    out["LeadToCustomerPct"] = out["Conversions"] / out["Leads"] * 100
    out["LeadToFormPct"] = out["Forms"] / out["Leads"] * 100
    out["CostPerLead"] = out["Spend"] / out["Leads"]
    out["CostPerAcquisition"] = np.where(out["Conversions"] > 0, out["Spend"] / out["Conversions"], np.nan)
    out["ROAS"] = np.where(out["Spend"] > 0, out["Revenue"] / out["Spend"], 0)
    return out.sort_values("LeadToCustomerPct", ascending=False)

if __name__ == "__main__":
    data = load_data()
    print("Rows:", len(data))
    print(funnel_summary(data).to_string(index=False))
    print("\\nChannel performance:\\n", channel_performance(data).round(2).to_string(index=False))
