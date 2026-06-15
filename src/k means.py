import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

df = pd.read_excel("maths dataset.xlsx")
df_2023 = df[df["YEAR"] == 2023].copy()

features = ['Pm2.5 levels', 'Traffic congestion %', 'Population density(people/km²)', 'green coverage']  # Update with your actual column names
X = df_2023[features]

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

kmeans = KMeans(n_clusters=5, random_state=42)
df_2023['Cluster'] = kmeans.fit_predict(X_scaled)

cluster_profiles = df_2023.groupby('Cluster')[features].mean()

print("Cluster Profiles (Feature Averages):\n", cluster_profiles)


def interpret_cluster(row):
    if row['Pm2.5 levels'] > 150 and row['green coverage'] < 10:
        return 'High Pollution, Low Green'
    elif row['Pm2.5 levels'] < 120 and row['green coverage'] > 20:
        return 'Low Pollution, High Green'
    elif row['Pm2.5 levels'] > 150:
        return 'High Pollution'
    elif row['green coverage'] < 10:
        return 'Low Green Coverage'
    else:
        return 'Moderate/Green Balanced'

cluster_profiles['Cluster_Label'] = cluster_profiles.apply(interpret_cluster, axis=1)

df_2023['Cluster_Label'] = df_2023['Cluster'].map(cluster_profiles['Cluster_Label'])


print("\nCity-wise Cluster Assignments:\n", df_2023[['CITY', 'Cluster', 'Cluster_Label']])



import seaborn as sns
import matplotlib.pyplot as plt


plt.figure(figsize=(10, 8))
scatter = sns.scatterplot(
    data=df_2023,
    x='Pm2.5 levels',
    y='green coverage',
    hue='Cluster',
    palette='tab10',
    s=200,
    edgecolor='k',

)

# Annotate each point with the city name (larger and bold)
for i in range(df_2023.shape[0]):
    plt.text(
        df_2023['Pm2.5 levels'].iloc[i] + 1,  # offset to avoid overlap
        df_2023['green coverage'].iloc[i],
        df_2023['CITY'].iloc[i],
        fontsize=12,  # Increased font size
        fontweight='bold'  # Make the text bold
    )


plt.title('Cities by Cluster: Pollution vs Green Coverage')
plt.xlabel('Pm2.5 Levels')
plt.ylabel('Green Coverage')
plt.legend(title='Cluster')
plt.grid(True)
plt.tight_layout()
plt.show()

