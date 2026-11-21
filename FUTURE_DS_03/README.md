# FUTURE INTERNs — Task 3
## Marketing Funnel & Conversion Performance Analysis

### Project contents
- `data/marketing_funnel.csv` — synthetic lead-level dataset (6,000 records)
- `notebooks/Task_3_Marketing_Funnel_Analysis.ipynb` — Google Colab notebook
- `analysis.py` — reusable data-loading and analysis functions
- `app.py` — interactive Streamlit dashboard
- `outputs/` — precomputed funnel, channel, campaign, device and monthly summaries
- `insights_report.md` — findings, metrics, recommendations and limitations
- `requirements.txt` — Python dependencies

### Important data note
The dataset is synthetic and generated for this portfolio project. Do not describe its metrics as actual company or client results.

### Run in Google Colab
1. Open the notebook in `notebooks/`.
2. Upload `data/marketing_funnel.csv` when prompted.
3. Run all cells from top to bottom.

### Run Streamlit locally (Mac/Linux)
```bash
cd FUTURE_DS_03
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

### Key metrics
- Funnel conversion rate: stage count / previous stage count × 100
- Lead-to-customer rate: converted leads / total leads × 100
- CPL: marketing spend / leads
- CPA: marketing spend / converted customers
- ROAS: attributed revenue / marketing spend

### GitHub
Suggested repository name: `FUTURE_DS_03`
