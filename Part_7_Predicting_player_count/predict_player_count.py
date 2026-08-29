import pickle
import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score

pd.set_option("display.max_columns", None)  # Show all columns
pd.set_option("display.max_rows", None)  # Show all rows

print("Importing data...")

# Folder paths
clean_folder = Path(__file__).resolve().parent.parent / "Data" / "Clean"
game_clusters_path = Path(__file__).resolve().parent.parent / "Part_3_Game_similarity" / "game_clusters.csv"
casino_clusters_path = Path(__file__).resolve().parent.parent / "Part_4_Casino_cohorts" / "casino_clusters.csv"
export_folder = Path(__file__).resolve().parent

df = pd.read_csv(clean_folder / "player_activity_clean.csv", sep=";")

game_clusters = pd.read_csv(game_clusters_path).drop_duplicates()
game_clusters.rename(columns={"cluster": "GAME_CLUSTER"}, inplace=True)

casino_clusters = pd.read_csv(casino_clusters_path)
casino_clusters.rename(columns={"cluster": "COHORT"}, inplace=True)

# Part 7.1: Build one row per (casino, game) pair
#---------------------------------------------------
feature_cols = [c for c in df.columns if c.startswith("THEME_") or c.startswith("MECH_") or c.startswith("TYPE_")]

agg = {"PLAYERID": "nunique", "GOLIVE_DATE": "first"}
agg.update({c: "first" for c in feature_cols})
pairs = df.groupby(["CASINOID", "GAMEID"]).agg(agg).reset_index()
pairs.rename(columns={"PLAYERID": "PLAYER_COUNT"}, inplace=True)

most_recent_date = pd.to_datetime(df["DATE"]).max()
pairs["DAYS_LIVE"] = (most_recent_date - pd.to_datetime(pairs["GOLIVE_DATE"])).dt.days

pairs = pairs.merge(game_clusters, on="GAMEID", how="left")
pairs = pairs.merge(casino_clusters, on="CASINOID", how="left")

feature_columns = feature_cols + ["DAYS_LIVE", "GAME_CLUSTER", "COHORT"]
X = pd.get_dummies(pairs[feature_columns], columns=["GAME_CLUSTER", "COHORT"])
y = pairs["PLAYER_COUNT"]

y_log = np.log1p(y)

# Part 7.2: Train/test split
#------------------------------
X_train, X_test, y_train_log, y_test_log = train_test_split(X, y_log, test_size=0.2, random_state=42)
y_test = np.expm1(y_test_log)

# Part 7.3: Baseline - predict the average player count
#---------------------------------------------------------
baseline_pred = np.full(len(y_test), fill_value=np.expm1(y_train_log.mean()))
baseline_mae = mean_absolute_error(y_test, baseline_pred)
baseline_r2 = r2_score(y_test, baseline_pred)

# Part 7.4: Model
#-------------------
print("Training model...")
model = RandomForestRegressor(n_estimators=200, random_state=42, n_jobs=-1)
model.fit(X_train, y_train_log)

predictions = np.expm1(model.predict(X_test))
model_mae = mean_absolute_error(y_test, predictions)
model_r2 = r2_score(y_test, predictions)

print(f"\nBaseline (predict the average) - MAE: {baseline_mae:.1f} players, R2: {baseline_r2:.3f}")
print(f"Model (RandomForestRegressor) - MAE: {model_mae:.1f} players, R2: {model_r2:.3f}")

# Part 7.5: What drives the prediction
#--------------------------------------
importances = pd.Series(model.feature_importances_, index=X.columns)

def group_name(col):
    for prefix in ["THEME_", "MECH_", "TYPE_", "GAME_CLUSTER_", "COHORT_"]:
        if col.startswith(prefix):
            return prefix.rstrip("_")
    return col

grouped_importance = importances.groupby(group_name).sum().sort_values(ascending=False)
print("\nFeature importance by group:")
print(grouped_importance)

print("\nTop 10 individual features:")
print(importances.sort_values(ascending=False).head(10))

# Save the trained model + exact training columns for Part 8 to reuse
with open(export_folder / "player_count_model.pkl", "wb") as f:
    pickle.dump({"model": model, "columns": X.columns.tolist()}, f)
print(f"\nModel saved to {export_folder / 'player_count_model.pkl'}")
