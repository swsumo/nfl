
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
