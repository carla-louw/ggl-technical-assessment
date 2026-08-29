# Part 1: Data prep and cleaning

**Disclaimer:** I did not use dbt for this section as I have no experience using it.

## Part 1.1: Look at data
**Purpose:** Firstly check if the data loads successfully into the dataframe. Secondly check if the correct data is being loaded and assigned to the variables.

**Outcome:** The data loads succesfully and the correct data is being loaded and assigned.

## Part 1.2: Look at data types
**Purpose:** Check if all columns contain the expected data type, for example a column containing numerical entries are of type float or int and not string.

**Outcome:** All of the data in all of the datasets are of the expected data type, so no conversions need to be made.

## Part 1.3: Convert monetary values to base currency
**Method:** Multiply the entries in the TOTALWAGER and TOTALPAYOUT columns from the fact_activity.csv dataset with the EXCHANGE_RATE_TO_BASE column from the dim_currency.csv dataset while matching on CURRENCYID.

**Outcome:** Figures are comparable across rows and currencies.

## Part 1.4: Add net win in base currency
**Method:** The feature NETWIN is calculated by subtracting TOTALPAYOUT from TOTALWAGER.

## Part 1.5: One-hot encode data
**Method:** Use one-hot encoding to add binary labels for each of the string labels in the THEMES and MECHANICS fields in the fact_activity.csv dataset. The same was applied to the GAMETYPE field in the dim_game.csv dataset.

**Outcome:** The array fields are usable for the work that follows.

## Part 1.6: Merge and export data
**Outcome:** Create one dataset to be used for all further analyses.