# Business Sales Performance Analytics — Future Interns Task 1

## Project objective
Analyze business sales data to identify revenue trends, top-selling products, high-value categories, and regional performance.

## Dataset
`data/superstore_sales.csv` contains 8,000 reproducibly generated Superstore-style transaction records. **This is synthetic demonstration data, not real company/customer data.** The dataset is generated with a fixed random seed so the results can be reproduced.

Columns include Order ID, Order Date, Ship Date, Region, State, City, Segment, Category, Sub-Category, Product Name, Sales, Quantity, Discount, and Profit.

## Tools
Python, Pandas, NumPy, Plotly, Streamlit, Google Colab.

## Run in Google Colab
1. Upload `superstore_sales.csv` to Colab.
2. Run the notebook cells in `notebooks/Task_1_Sales_Analysis.ipynb`.
3. Download the cleaned data and generated charts if required.

## Run dashboard locally
```bash
pip install -r requirements.txt
streamlit run app.py
```
Keep `data/superstore_sales.csv` in the `data/` folder beside `app.py`.

## Analysis
The project calculates total sales, total profit, order count, units sold, profit margin and average order value. It also analyzes monthly performance, category performance, regional performance, top products, and discount impact.

## Important
Do not describe synthetic findings as actual company results. State clearly in reports and presentations that the data is synthetic and the analysis demonstrates a business analytics workflow.
