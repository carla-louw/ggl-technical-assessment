import pandas as pd
from pathlib import Path
from sklearn.preprocessing import MinMaxScaler

pd.set_option("display.max_columns", None)  # Show all columns
pd.set_option("display.max_rows", None)  # Show all rows

print("Importing data...")

# Folder paths
clean_folder = Path(__file__).resolve().parent.parent / "Data" / "Clean"
import_game_clusters = Path(__file__).resolve().parent.parent / "Part_3_Game_similarity" / "game_clusters.csv"
import_casino_clusters = Path(__file__).resolve().parent.parent / "Part_4_Casino_cohorts" / "casino_clusters.csv"

# Import data
df = pd.read_csv(clean_folder / "player_activity_clean.csv", sep=";")
df = df[["CASINOID", "GAMEID", "TOTALWAGER", "TOTALSPINS"]]

game_clusters = pd.read_csv(import_game_clusters)
game_clusters.drop_duplicates(inplace=True)
game_clusters.rename(columns={"cluster": "GAME_CLUSTER"}, inplace=True)

casino_clusters = pd.read_csv(import_casino_clusters)
casino_clusters.rename(columns={"cluster": "COHORT"}, inplace=True)

df = df.merge(casino_clusters, on="CASINOID", how="left")
df = df.merge(game_clusters, on="GAMEID", how="left")

# Part 5.1: Recommend games per casino
#----------------------------------------
metric_cols = ["TOTALWAGER", "TOTALSPINS"]
scaler = MinMaxScaler()

game_scores = df.groupby(["COHORT", "GAMEID"])[metric_cols].mean().reset_index()
game_scores[metric_cols] = scaler.fit_transform(game_scores[metric_cols])
game_scores["score"] = game_scores[metric_cols].mean(axis=1)
game_scores = game_scores[["COHORT", "GAMEID", "score"]]

cluster_scores = df.groupby(["COHORT", "GAME_CLUSTER"])[metric_cols].mean().reset_index()
cluster_scores[metric_cols] = scaler.fit_transform(cluster_scores[metric_cols])
cluster_scores["cluster_score"] = cluster_scores[metric_cols].mean(axis=1)
cluster_scores = cluster_scores[["COHORT", "GAME_CLUSTER", "cluster_score"]]

all_games = game_clusters[["GAMEID", "GAME_CLUSTER"]]

def recommend_games(casino_id, top_n=10):
    cohort = casino_clusters.loc[casino_clusters["CASINOID"] == casino_id, "COHORT"].values[0]
    live_games = df.loc[df["CASINOID"] == casino_id, "GAMEID"].unique()

    candidates = all_games[~all_games["GAMEID"].isin(live_games)].copy()
    candidates["COHORT"] = cohort

    candidates = candidates.merge(game_scores, on=["COHORT", "GAMEID"], how="left")
    candidates = candidates.merge(cluster_scores, on=["COHORT", "GAME_CLUSTER"], how="left")

    candidates["reason"] = "Performs well with casinos in your cohort"
    candidates.loc[candidates["score"].isna(), "reason"] = "No cohort history yet, estimated from similar games"
    candidates["score"] = candidates["score"].fillna(candidates["cluster_score"])

    candidates.dropna(subset=["score"], inplace=True)
    candidates.sort_values("score", ascending=False, inplace=True)

    return candidates[["GAMEID", "score", "reason"]].head(top_n)

# Part 5.2: Ranked output for a few example casinos
#-----------------------------------------------------
example_casinos = ["CASINO_111", "CASINO_103", "CASINO_15"]

for casino_id in example_casinos:
    print(f"\nTop recommended games for {casino_id}:")
    print(recommend_games(casino_id))
