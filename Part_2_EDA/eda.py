import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt

pd.set_option("display.max_columns", None)  # Show all columns
pd.set_option("display.max_rows", None)  # Show all rows

print("Running data EDA script (1-2min)...")

# Folder path
formatted_folder = Path(__file__).resolve().parent.parent / "Data" / "Formatted"
clean_folder = Path(__file__).resolve().parent.parent / "Data" / "Clean"
export_folder = Path(__file__).resolve().parent.parent / "Part_2_EDA"

# Import formatted data
df = pd.read_csv(formatted_folder / "player_activity_formatted.csv", sep=";")

# Part 2.1: Check for missing values
#--------------------------------------
# print(df.isnull().sum())

# Part 2.2: Check for duplicated values
#-----------------------------------------
# print(df.duplicated().sum())

# Part 2.3: Check for columns with no variance
#------------------------------------------------
cols_no_var = df.columns[df.nunique() == 1]
# print(cols_no_var)

# Drop columns with no variance
df = df.drop(columns=cols_no_var)

# Part 2.4: Add average wager and average payout
#--------------------------------------------------
new_cols = pd.DataFrame({
    "AVEWAGER_PER_SPIN": df["TOTALWAGER"] / df["TOTALSPINS"],
    "AVEPAYOUT_PER_SPIN": df["TOTALPAYOUT"] / df["TOTALSPINS"],
})
df = pd.concat([df, new_cols], axis=1)

# Part 2.5: Statistical summary
#---------------------------------
# print(df.describe().T)

# Part 2.6: plot Total Wager and Total Payout vs Total Spins
#--------------------------------------------------------------
print("Creating the plot...")

plt.figure(figsize=(10, 5))
plt.scatter(df["TOTALSPINS"], df["TOTALWAGER"], alpha=0.5, label="Total Wager")
plt.scatter(df["TOTALSPINS"], df["TOTALPAYOUT"], alpha=0.5, label="Total Payout")
plt.xlabel("Total Spins")
plt.ylabel("Amount")
plt.title("Total Wager and Total Payout vs Total Spins")
plt.legend()
plt.savefig(export_folder / "total_wager_vs_total_payout.png")

df.to_csv(clean_folder / "player_activity_clean.csv", sep=";", index=False)
print("Data has been successfully and exported to 'Data/Clean/player_activity_clean.csv'")