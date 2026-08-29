import ast
import pandas as pd
from pathlib import Path
from sklearn.preprocessing import MultiLabelBinarizer

# Folder paths
raw_folder = Path(__file__).resolve().parent.parent / "Data" / "Raw"
formatted_folder = Path(__file__).resolve().parent.parent / "Data" / "Formatted"

# Import the data
df_currency = pd.read_csv(raw_folder / "dim_currency.csv", sep=";")
df_game = pd.read_csv(raw_folder / "dim_game.csv", sep=";")
df_activity = pd.read_csv(raw_folder / "fact_activity.csv", sep=";")

pd.set_option("display.max_columns", None)  # Show all columns
pd.set_option("display.max_rows", None)  # Show all rows

print("Running data modelling script (1-2min)...")

# Part 1.1: Look at data
#--------------------------
# print(df_currency.head())
# print(df_game.head())
# print(df_activity.head())

# Part 1.2: Look at data types
#--------------------------------
# print(df_currency.dtypes)
# print(df_game.dtypes)
# print(df_activity.dtypes)

# Part 1.3: Convert monetary values to base currency
#------------------------------------------------------
exchange_rate = df_currency.set_index('CURRENCYID')['EXCHANGE_RATE_TO_BASE']

cols_to_convert = ['TOTALWAGER', 'TOTALPAYOUT']
for col in cols_to_convert:
    df_activity[col] = df_activity[col] * df_activity['CURRENCYID'].map(exchange_rate)

# Part 1.4: Add net win in base currency
#------------------------------------------
df_activity['NETWIN'] = df_activity['TOTALWAGER'] - df_activity['TOTALPAYOUT']  

# Part 1.5: One-hot encode data
#---------------------------------

# One-hot encode THEMES and MECHANICS
df_game['THEMES'] = df_game['THEMES'].apply(ast.literal_eval)
df_game['MECHANICS'] = df_game['MECHANICS'].apply(ast.literal_eval)

mlb_theme = MultiLabelBinarizer()
theme_ohe = pd.DataFrame(
    mlb_theme.fit_transform(df_game['THEMES']),
    columns=[f'{c}' for c in mlb_theme.classes_],
    index=df_game.index)

mlb_mech = MultiLabelBinarizer()
mech_ohe = pd.DataFrame(
    mlb_mech.fit_transform(df_game['MECHANICS']),
    columns = [f'{c}' for c in mlb_mech.classes_],
    index = df_game.index)

df_game = pd.concat([df_game, theme_ohe, mech_ohe], axis=1)
df_game.drop(['THEMES'], axis=1, inplace=True)
df_game.drop(['MECHANICS'], axis=1, inplace=True)

# One-hot encode GAMETYPE
mlb_gametype = MultiLabelBinarizer()
df_game['GAMETYPE'] = df_game['GAMETYPE'].apply(lambda x: [x])
gametype_ohe = pd.DataFrame(
    mlb_gametype.fit_transform(df_game['GAMETYPE']),
    columns = [f'{c}' for c in mlb_gametype.classes_],
    index = df_game.index)
df_game = pd.concat([df_game, gametype_ohe], axis=1)
df_game.drop(['GAMETYPE'], axis=1, inplace=True)

# Part 1.6: Merge and export data
#-----------------------------------
df_merged = df_activity.merge(df_game, on='GAMEID', how='left')
df_merged.to_csv(formatted_folder / "player_activity_formatted.csv", sep=";", index=False)
print("Data has been successfully merged and exported to 'Data/Formatted/player_activity_formatted.csv'")