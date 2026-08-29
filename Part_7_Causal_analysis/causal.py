import pandas as pd
from dowhy import CausalModel
from pathlib import Path

pd.set_option("display.max_columns", None)  # Show all columns
pd.set_option("display.max_rows", None)  # Show all rows

print("Importing data...")

# Folder paths
clean_folder = Path(__file__).resolve().parent.parent / "Data" / "Clean"
this_folder = Path(__file__).resolve().parent.parent / "Part_7_Causal_analysis"

# Import clean data
data_df = pd.read_csv(clean_folder / "player_activity_clean.csv", sep=";")

# Import DAG
dag_df = pd.read_csv(this_folder / "dag.csv")
dag_df = pd.DataFrame(dag_df) 

def run_model_training_for_single_relationship(iteration, training_data_df, graph_df, causal_col_name, effect_col_name):

    cause = graph_df[causal_col_name][iteration]
    effect = graph_df[effect_col_name][iteration]

    # Define the causal model
    #-------------------------------
    model = CausalModel(
        data=training_data_df,
        treatment=[cause],
        outcome=effect
    )
    
    # Get estimand
    identified_estimand = model.identify_effect(proceed_when_unidentifiable=True)

    # Get estimate
    causal_estimate = model.estimate_effect(identified_estimand, method_name="backdoor.linear_regression")
    
    # Shows the cause and effect for the results entry and adds the causal value (Strength of effect) to the results entry
    line = [cause, effect, round(float(causal_estimate.value), 5)]
    
    return line

# iteration of the dag
for iteration in range(len(dag_df)):
    trained_line = run_model_training_for_single_relationship(iteration, data_df, dag_df, causal_col_name="Cause", effect_col_name="Effect")
    print(trained_line)
