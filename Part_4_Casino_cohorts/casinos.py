import pandas as pd
from pathlib import Path
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

pd.set_option("display.max_columns", None)  # Show all columns
pd.set_option("display.max_rows", None)  # Show all rows

print("Running the casino clustering script (1-2min)...")

# Folder path
clean_folder = Path(__file__).resolve().parent.parent / "Data" / "Clean"
import_folder = Path(__file__).resolve().parent.parent / "Part_3_Game_similarity"
export_folder = Path(__file__).resolve().parent.parent / "Part_4_Casino_cohorts"

# Import clean data
df = pd.read_csv(clean_folder / "player_activity_clean.csv", sep=";")
clusters = pd.read_csv(import_folder / "game_clusters.csv")
clusters.drop_duplicates(inplace=True)

# Part 4.1: Prepare casino-level features
#-------------------------------------------
cols_to_keep = ["CASINOID", "GAMEID", "CURRENCYID", "TOTALWAGER", "TOTALPAYOUT", "TOTALSPINS", "NETWIN", "AVEWAGER_PER_SPIN", "AVEPAYOUT_PER_SPIN"]
df = df[cols_to_keep]
df.drop_duplicates(inplace=True)

df = df.merge(clusters, on="GAMEID", how="left")
df = pd.get_dummies(df, columns=["cluster", "CURRENCYID"], dtype=int)

monetary_cols = ["TOTALWAGER", "TOTALPAYOUT", "TOTALSPINS", "NETWIN", "AVEWAGER_PER_SPIN", "AVEPAYOUT_PER_SPIN"]
df.drop(columns=['GAMEID'] + monetary_cols, inplace=True)

df = df.groupby('CASINOID').mean().reset_index()

# Binarize the one-hot columns back to 0/1 (mean() left them as fractions)
categorical_cols = [col for col in df.columns if col.startswith("cluster_") or col.startswith("CURRENCYID_")]
df[categorical_cols] = (df[categorical_cols] > 0).astype(int)

# Part 4.2: Fit KMeans clustering
#-----------------------------------
def elbow_curve(df, k_range, export_path, title):
    SSD = []
    for k in k_range:
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        kmeans.fit(df.values)
        SSD.append(kmeans.inertia_)
    fig, axes = plt.subplots(figsize=(6, 5))
    axes.plot(k_range, SSD, marker='o')
    axes.set_xlabel('Number of clusters (k)')
    axes.set_ylabel('SSD')
    axes.set_title(title)
    plt.tight_layout()
    plt.savefig(export_path)
    plt.close()

print("Determining the optimal number of clusters using the elbow method...")
k_range = range(2, 20)
elbow_curve(df.drop(columns=['CASINOID']), k_range, export_folder / "elbow_plot.png", "Elbow Plot")

print("Fitting KMeans with the chosen number of clusters...")
num_of_clusters = 8
kmeans = KMeans(n_clusters=num_of_clusters, random_state=42, n_init=10)
labels = kmeans.fit_predict(df.drop(columns=['CASINOID']).values)

results = pd.DataFrame({'CASINOID': df['CASINOID'], 'cluster': labels})
results.to_csv(export_folder / "casino_clusters.csv", index=False)

# Part 4.3: Cohort profiles
#-----------------------------
df_raw = pd.read_csv(clean_folder / "player_activity_clean.csv", sep=";")
df_raw = df_raw[["CASINOID", "GAMEID", "CURRENCYID", "TOTALWAGER", "NETWIN"]]
df_raw.drop_duplicates(inplace=True)

df_raw = df_raw.merge(clusters, on="GAMEID", how="left")
df_raw = df_raw.merge(results, on="CASINOID", how="left")

casino_monetary = df_raw.groupby("CASINOID")[["TOTALWAGER", "NETWIN"]].mean().reset_index()
casino_monetary = casino_monetary.merge(results, on="CASINOID")
print("Average wager and net win by cohort:")
print(casino_monetary.groupby("cluster")[["TOTALWAGER", "NETWIN"]].mean().round(1))
print()

currencies_per_casino = df_raw.groupby("CASINOID")["CURRENCYID"].nunique().reset_index(name="N_CURRENCIES")
currencies_per_casino = currencies_per_casino.merge(results, on="CASINOID")
print("Average number of currencies used per casino, by cohort:")
print(currencies_per_casino.groupby("cluster")["N_CURRENCIES"].mean().round(1))
print()

game_clusters_per_casino = df_raw.groupby("CASINOID")["cluster_x"].nunique().reset_index(name="N_GAME_CLUSTERS")
game_clusters_per_casino = game_clusters_per_casino.merge(results, on="CASINOID")
print("Average number of game clusters played per casino, by cohort:")
print(game_clusters_per_casino.groupby("cluster")["N_GAME_CLUSTERS"].mean().round(1))
print()

print("Cohort sizes:")
print(results["cluster"].value_counts().sort_index())