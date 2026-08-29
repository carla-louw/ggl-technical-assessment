import pickle
import numpy as np
import pandas as pd
from pathlib import Path

pd.set_option("display.max_columns", None)  # Show all columns
pd.set_option("display.max_rows", None)  # Show all rows

print("Importing data...")

# Folder paths
clean_folder = Path(__file__).resolve().parent.parent / "Data" / "Clean"
game_clusters_path = Path(__file__).resolve().parent.parent / "Part_3_Game_similarity" / "game_clusters.csv"
casino_clusters_path = Path(__file__).resolve().parent.parent / "Part_4_Casino_cohorts" / "casino_clusters.csv"
model_path = Path(__file__).resolve().parent.parent / "Part_7_Predicting_player_count" / "player_count_model.pkl"

df = pd.read_csv(clean_folder / "player_activity_clean.csv", sep=";")
game_clusters = pd.read_csv(game_clusters_path).drop_duplicates().rename(columns={"cluster": "GAME_CLUSTER"})
casino_clusters = pd.read_csv(casino_clusters_path).rename(columns={"cluster": "COHORT"})

with open(model_path, "rb") as f:
    saved = pickle.load(f)
model = saved["model"]
training_columns = saved["columns"]

# Part 8: Cold-start scenario
#--------------------------------
# CASINO_19 does not currently offer GAME_4599.

game_id = "GAME_4599"
casino_id = "CASINO_19"

feature_cols = [c for c in df.columns if c.startswith("THEME_") or c.startswith("MECH_") or c.startswith("TYPE_")]
game_row = df.loc[df["GAMEID"] == game_id, feature_cols].drop_duplicates().iloc[0]
game_cluster = game_clusters.loc[game_clusters["GAMEID"] == game_id, "GAME_CLUSTER"].values[0]
cohort = casino_clusters.loc[casino_clusters["CASINOID"] == casino_id, "COHORT"].values[0]

input_row = game_row.to_dict()
input_row["DAYS_LIVE"] = 0
input_row["GAME_CLUSTER"] = game_cluster
input_row["COHORT"] = cohort

X_new = pd.DataFrame([input_row])
X_new = pd.get_dummies(X_new, columns=["GAME_CLUSTER", "COHORT"])
X_new = X_new.reindex(columns=training_columns, fill_value=0)

prediction_log = model.predict(X_new)[0]
prediction = np.expm1(prediction_log)

print(f"\nPredicted distinct players for {game_id} at {casino_id} on day one: {prediction:.1f}")