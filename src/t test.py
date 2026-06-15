import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import ttest_rel

df = pd.read_excel("maths dataset.xlsx")

df['YEAR'] = df['YEAR'].astype(int)
df['CITY'] = df['CITY'].astype(str)

metric_cols = [col for col in df.columns if col not in ['CITY', 'YEAR' ]]

df_pivot = df.pivot(index='CITY', columns='YEAR', values=metric_cols)

df_pivot.columns = [f"{metric}_{year}" for metric, year in df_pivot.columns]
df_pivot.reset_index(inplace=True)

metrics = sorted(list(set(col.split('_')[0] for col in df_pivot.columns if col.endswith('2020'))))

results = []

change_data = {metric: [] for metric in metrics}
p_values = []

sns.set(style="whitegrid")


for i, metric in enumerate(metrics, 1):
    col_2020 = f"{metric}_2020"
    col_2023 = f"{metric}_2023"

    if col_2020 in df_pivot and col_2023 in df_pivot:

        t_stat, p_val = ttest_rel(df_pivot[col_2020], df_pivot[col_2023])


        results.append({
            'Metric': metric,
            '2020 mean': df_pivot[col_2020].mean(),
            '2023 mean': df_pivot[col_2023].mean(),
            't-statistic': t_stat,
            'p-value': p_val,
            'Significant': 'Yes' if p_val < 0.05 else 'No'
        })


        change_data[metric] = df_pivot[col_2023] - df_pivot[col_2020]
        p_values.append(p_val)

results_df = pd.DataFrame(results)
pd.set_option('display.max_columns', None)  # Show all rows
print("\nPaired T-Test Results:\n", results_df)

plt.figure(figsize=(10, 6))
sns.boxplot(data=pd.DataFrame(change_data), palette="Set2")
plt.title("Boxplot of Changes (2020 to 2023)", fontsize=14)
plt.xlabel("Metrics")
plt.ylabel("Change (2023 - 2020)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

plt.figure(figsize=(10, 6))
sns.barplot(x=metrics, y=p_values)
plt.title("P-Values for Metric Changes (2020 to 2023)", fontsize=14)
plt.xlabel("Metrics")
plt.ylabel("P-Value")
plt.axhline(0.05, color='red', linestyle='--', label="Significance Threshold (0.05)")
plt.legend()
plt.tight_layout()
plt.show()


