from pathlib import Path
import pandas as pd
import numpy as np
DATA_PATH=Path(__file__).parent/"data"/"customer_churn.csv"
def load_data(path=DATA_PATH):
    d=pd.read_csv(path)
    d["TotalCharges"]=pd.to_numeric(d["TotalCharges"],errors="coerce")
    d["TotalCharges"]=d["TotalCharges"].fillna(d["TotalCharges"].median())
    d["PaymentMethod"]=d["PaymentMethod"].fillna("Unknown")
    d=d.drop_duplicates(subset=["CustomerID"])
    d["ChurnFlag"]=d["Churn"].map({"Yes":1,"No":0})
    d["TenureGroup"]=pd.cut(d["Tenure"],[-1,6,12,24,48,72],labels=["0-6 months","7-12 months","13-24 months","25-48 months","49-72 months"])
    d["MonthlyChargeBand"]=pd.cut(d["MonthlyCharges"],[0,40,70,100,200],labels=["Low (≤40)","Medium (41-70)","High (71-100)","Very High (>100)"])
    return d
def get_kpis(d):
    n=d.CustomerID.nunique(); c=int(d.ChurnFlag.sum())
    return {"customers":n,"churned":c,"retained":n-c,"churn_rate":c/n*100 if n else 0,"retention_rate":(n-c)/n*100 if n else 0,"avg_monthly_charges":d.MonthlyCharges.mean(),"avg_tenure":d.Tenure.mean()}
def churn_by(d,col):
    x=d.groupby(col,observed=False).agg(Customers=("CustomerID","nunique"),Churned=("ChurnFlag","sum"),Churn_Rate=("ChurnFlag","mean")).reset_index()
    x["Churn_Rate"]*=100
    return x
