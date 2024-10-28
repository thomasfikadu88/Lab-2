# %% import dataframe from pickle file
import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_pickle("UK.pkl")
df['Description'] = df['Description'].str.strip()


df.head()


# %% convert dataframe to invoice-based transactional format
Collection = (df.groupby(['InvoiceNo', 'Description'])['StockCode']
          .sum().unstack().reset_index().fillna(0)
          .set_index('InvoiceNo'))

Collection = Collection.applymap(lambda x: 1 if str(x).isdigit() and int(x) > 0 else 0)


Collection.head()



# %% apply apriori algorithm to find frequent items and association rules

frequent_itemsets = apriori(Collection, min_support=0.01, use_colnames=True, low_memory=True)
rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1)
rules
# %% count of frequent itemsets that have more then 1/2/3 items,
# and the frequent itemsets that has the most items
frequent_itemsets['length'] = frequent_itemsets['itemsets'].apply(lambda x: len(x))

# Count of itemsets with more than 1, 2, or 3 items
count_1_itemset = frequent_itemsets[frequent_itemsets['length'] > 1].shape[0]
count_2_itemset = frequent_itemsets[frequent_itemsets['length'] > 2].shape[0]
count_3_itemset = frequent_itemsets[frequent_itemsets['length'] > 3].shape[0]

max_itemset = frequent_itemsets[frequent_itemsets['length'] == frequent_itemsets['length'].max()]

print(f"Count of itemsets with more than 1 item: {count_1_itemset}")
print(f"Count of itemsets with more than 2 items: {count_2_itemset}")
print(f"Count of itemsets with more than 3 items: {count_3_itemset}")
print(f"Frequent itemset with the most items:\n{max_itemset}")


# %% top 10 lift association rules

top_10_lift_rules = rules.sort_values("lift", ascending=False).head(10)
print("Top 10 association rules by lift:\n", top_10_lift_rules)


# %% scatterplot support vs confidence
import seaborn as sns
import matplotlib.pyplot as plt

sns.scatterplot(x=rules["support"], y=rules["confidence"], alpha=0.3)
plt.xlabel("Support")
plt.ylabel("Confidence")
plt.title("Support vs Confidence")


# %% scatterplot support vs lift
sns.scatterplot(x=rules["support"], y=rules["lift"], alpha=0.3)
plt.xlabel("Support")
plt.ylabel("Confidence")
plt.title("Support vs Lift")