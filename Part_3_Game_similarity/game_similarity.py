import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors
from sklearn.cluster import KMeans

pd.set_option("display.max_columns", None)  # Show all columns
pd.set_option("display.max_rows", None)  # Show all rows

print("Running game similarity script (1-2min)...")

print("Importing data...")

# Folder path
clean_folder = Path(__file__).resolve().parent.parent / "Data" / "Clean"
export_folder = Path(__file__).resolve().parent

# Import clean data
df = pd.read_csv(clean_folder / "player_activity_clean.csv", sep=";")

# Part 3.1: Build one feature row per game
#--------------------------------------------
cols_to_drop = ["AVEPAYOUT_PER_SPIN", "AVEWAGER_PER_SPIN", "NETWIN", "TOTALPAYOUT", "TOTALSPINS", "GOLIVE_DATE", "DATE", "CASINOID", "PLAYERID", "CURRENCYID", "TOTALWAGER"]
games = df.drop(columns=cols_to_drop).drop_duplicates().reset_index(drop=True)

game_ids = games["GAMEID"]
features = games.drop(columns=["GAMEID"])

scaled_features = pd.DataFrame(StandardScaler().fit_transform(features), columns=features.columns)

nn = NearestNeighbors(n_neighbors=6)  # 5 neighbours + the game itself
nn.fit(scaled_features)

def similar_games(game_id, n=5):
    idx = game_ids[game_ids == game_id].index[0]
    _, indices = nn.kneighbors(scaled_features.loc[[idx]], n_neighbors=n + 1)
    neighbour_ids = game_ids.loc[indices[0]].tolist()
    neighbour_ids.remove(game_id)
    return neighbour_ids[:n]

# Part 3.2: Examples & sanity check
#-------------------------------------
feature_cols = [c for c in df.columns if c.startswith("THEME_") or c.startswith("MECH_") or c.startswith("TYPE_")]
attributes = df.drop_duplicates("GAMEID").set_index("GAMEID")[feature_cols]

for example_game in game_ids.head(3):
    neighbours = similar_games(example_game)
    print(f"Games most similar to {example_game}: {neighbours}")

    top_match = neighbours[0]
    shared = (attributes.loc[example_game] & attributes.loc[top_match]).sum()
    total = attributes.loc[example_game].sum()
    print(f"  sanity check: top match {top_match} shares {shared}/{total} attributes with {example_game}")

# Part 3.3: KMeans clustering
#----------------------------------------------------------
print("Determining the optimal number of clusters using the elbow method...")
SSD = []
k_range = range(2, 50)
for k in k_range:
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    kmeans.fit(scaled_features.values)
    SSD.append(kmeans.inertia_)

fig, axes = plt.subplots(figsize=(6, 5))
axes.plot(k_range, SSD, marker='o')
axes.set_xlabel('Number of clusters (k)')
axes.set_ylabel('SSD')
axes.set_title('Elbow Plot')
plt.tight_layout()
plt.savefig(export_folder / "elbow_plot.png")

print("Fitting KMeans with the chosen number of clusters...")
num_of_clusters = 25
kmeans = KMeans(n_clusters=num_of_clusters, random_state=42, n_init=10)
labels = kmeans.fit_predict(scaled_features.values)

results = pd.DataFrame({"GAMEID": game_ids, "cluster": labels})
results.to_csv(export_folder / "game_clusters.csv", index=False)
print("Game clusters exported to game_clusters.csv")
