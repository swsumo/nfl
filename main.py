'''
import os
import pandas as pd

# Create the output folder
output_folder = "dataset"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Path where the .xlsx files are stored
input_folder = "group"

# Convert each .xlsx file to .csv
for filename in os.listdir(input_folder):
    if filename.endswith(".xlsx"):
        # Read the .xlsx file
        file_path = os.path.join(input_folder, filename)
        df = pd.read_excel(file_path)

        # Save as .csv in the dataset folder
        output_file = os.path.join(output_folder, filename.replace(".xlsx", ".csv"))
        df.to_csv(output_file, index=False)
        print(f"Converted: {filename} -> {output_file}")

print(f"All files have been converted and saved to the '{output_folder}' folder.")

import pandas as pd

# File paths for the CSVs
team_offense_file = "dataset/team_offense.csv"
scoring_offense_file = "dataset/scoring_offense.csv"
conversions_file = "dataset/conversions.csv"
drive_averages_file = "dataset/drive_avg.csv"

# Read the CSV files
team_offense = pd.read_csv(team_offense_file)
scoring_offense = pd.read_csv(scoring_offense_file)
conversions = pd.read_csv(conversions_file)
drive_averages = pd.read_csv(drive_averages_file)

# Merge the tables on 'Tm' with unique suffixes
merged_data = pd.merge(team_offense, scoring_offense, on="Tm", how="outer", suffixes=("_team", "_score"))
merged_data = pd.merge(merged_data, conversions, on="Tm", how="outer", suffixes=("", "_conv"))
merged_data = pd.merge(merged_data, drive_averages, on="Tm", how="outer", suffixes=("", "_drive"))

# Save the combined dataset to a CSV file
output_file = "combined_data.csv"
merged_data.to_csv(output_file, index=False)

print(f"Combined dataset saved as {output_file}")
'''



import streamlit as st
import pandas as pd
import joblib
import json

# Load the trained model and feature columns
model = joblib.load('nfl_winner_model.pkl')
with open('feature_columns.json', 'r') as f:
    feature_columns = json.load(f)

# Load the dataset for team stats
data = pd.read_csv('engineered_data.csv')

# List of features for teams
features = [
    'PF', 'Offensive_Efficiency', 'Turnover_Ratio', 'Drive_Efficiency',
    'Conversion_Efficiency_3D', 'Conversion_Efficiency_4D', 'Pts/G'
]

# Streamlit app title
st.title("NFL Matchup Winner Predictor")

# Team selection
team1 = st.selectbox("Select Team 1 (Home)", data['Tm'].unique())
team2 = st.selectbox("Select Team 2 (Away)", data['Tm'].unique())

# Ensure teams are not the same
if team1 == team2:
    st.warning("Please select two different teams.")
else:
    # Extract team stats
    team1_data = data[data['Tm'] == team1][features].iloc[0]
    team2_data = data[data['Tm'] == team2][features].iloc[0]

    # Create a DataFrame for prediction
    matchup = pd.DataFrame({
        'Team1_PF': [team1_data['PF']],
        'Team2_PF': [team2_data['PF']],
        'Team1_Offensive_Efficiency': [team1_data['Offensive_Efficiency']],
        'Team2_Offensive_Efficiency': [team2_data['Offensive_Efficiency']],
        'Team1_Turnover_Ratio': [team1_data['Turnover_Ratio']],
        'Team2_Turnover_Ratio': [team2_data['Turnover_Ratio']],
        'Team1_Drive_Efficiency': [team1_data['Drive_Efficiency']],
        'Team2_Drive_Efficiency': [team2_data['Drive_Efficiency']],
        'Team1_Conversion_Efficiency_3D': [team1_data['Conversion_Efficiency_3D']],
        'Team2_Conversion_Efficiency_3D': [team2_data['Conversion_Efficiency_3D']],
        'Team1_Conversion_Efficiency_4D': [team1_data['Conversion_Efficiency_4D']],
        'Team2_Conversion_Efficiency_4D': [team2_data['Conversion_Efficiency_4D']],
        'Team1_Pts/G': [team1_data['Pts/G']],
        'Team2_Pts/G': [team2_data['Pts/G']],
    })

    # Reorder columns to match the trained model
    matchup = matchup[feature_columns]

    # Make a prediction
    prediction = model.predict(matchup)[0]
    winning_team = team1 if prediction == 1 else team2

    # Display the result
    st.success(f"The predicted winner is: **{winning_team}**")
