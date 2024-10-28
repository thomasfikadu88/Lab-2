# %% Import excel to dataframe
import pandas as pd

import openpyxl as op

import seaborn as sns


df = pd.read_excel("Online Retail.xlsx")


# %%  Show the first 10 rows

df.head(10)

# %% Generate descriptive statistics regardless the datatypes

df.describe(include='all')

# %% Remove all the rows with null value and generate stats again

df_new = df.dropna()
df_new.describe(include='all')

# %% Remove rows with invalid Quantity (Quantity being less than 0)

df_new = df_new[df_new["Quantity"] >= 0]

# %% Remove rows with invalid UnitPrice (UnitPrice being less than 0)

df_new = df_new[df_new["UnitPrice"] >= 0]

# %% Only Retain rows with 5-digit StockCode

df_new = df_new[df_new["StockCode"].astype(str).str.len() == 5]

# %% strip all description

df_new['Description'] = df_new['Description'].str.strip()

# %% Generate stats again and check the number of rows
stats = df_new.describe(include='all')
row_count = df_new.shape[0]
row_count


# %% Plot top 5 selling countries
import matplotlib.pyplot as plt
import seaborn as sns

top5_selling_countries = df_new["Country"].value_counts()[:5]
sns.barplot(x=top5_selling_countries.index, y=top5_selling_countries.values)
plt.xlabel("Country")
plt.ylabel("Amount")
plt.title("Top 5 Selling Countries")


# %% Plot top 20 selling products, drawing the bars vertically to save room for product description

top20_products = df_new["Description"].value_counts().head(20)
sns.barplot(y=top20_products.index, x=top20_products.values, orient='h')  # Horizontal bars
plt.xlabel("Sales Count")
plt.ylabel(" Description")
plt.title("Top 20 Selling Products")
plt.show()

# %% Focus on sales in UK

UK_df = df[df["Country"] == "United Kingdom"]

#%% Show gross revenue by year-month
from datetime import datetime

df["YearMonth"] = df["InvoiceDate"].apply(
    lambda dt: datetime(year=dt.year, month=dt.month, day=1)
)



# %% save df in pickle format with name "UK.pkl" for next lab activity
# we are only interested in InvoiceNo, StockCode, Description columns
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
df["YearMonth"] = df["InvoiceDate"].apply(lambda dt: datetime(year=dt.year, month=dt.month, day=1))
monthly_revenue = df.groupby("YearMonth")["Quantity"].sum()
monthly_revenue.plot(kind="line")
plt.xlabel("Year-Month")
plt.ylabel("Gross Revenue")
plt.title("Gross Revenue by Year-Month")
plt.show()

# %% Save UK data in pickle format with only the specified columns
df_uk_filtered = df[["InvoiceNo", "Description","StockCode"]]
df_uk_filtered.to_pickle("UK.pkl")
df_uk_filtered