import os
import requests
import numpy as np
import streamlit as st
from dotenv import load_dotenv
from groq import Groq

# Load environment variables for API keys
load_dotenv()

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY", "417422402cmsh6e6ff0c00a5cb3fp1ca598jsn937b61106ee8")
RAPIDAPI_HOST = "nfl-api-data.p.rapidapi.com"
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "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")

# Function to fetch live scores
def fetch_live_scores():
    url = f"https://{RAPIDAPI_HOST}/nfl-livescores"
    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": RAPIDAPI_HOST
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        scores_data = response.json()  # Ensure JSON response
        if isinstance(scores_data, list):  # Check if it's a list
            return scores_data
        else:
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching live scores: {e}")
        return None

# Placeholder function for winner prediction (Random for now)
def predict_winner(home_team, away_team):
    """Predict winner between home and away team using the GROQ API."""
    prompt = f"Based on NFL historical data and team performance, who is likely to win: {home_team} (home) vs {away_team} (away)?"
    
    try:
        # Call the GROQ API to get a response based on the prompt
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "user", "content": prompt}
            ],
            model="llama-3.3-70b-versatile"
        )

        # Extract the response content from the GROQ API's completion
        winner = chat_completion.choices[0].message.content.strip()

        # Remove unwanted part of the response if present
        unwanted_text = "Keep in mind that this prediction is based on general trends and past performance."
        if unwanted_text in winner:
            winner = winner.replace(unwanted_text, "").strip()

        return winner

    except Exception as e:
        # Handle any errors with the API call
        return f"Error occurred while predicting: {str(e)}"


# Initialize the Groq client with the API key for model predictions (optional)
client = Groq(api_key=GROQ_API_KEY)

def fetch_groq_prediction(prompt):
    try:
        chat_completion = client.chat.completions.create(
            messages=[{
                "role": "user",
                "content": prompt
            }],
            model="llama-3.3-70b-versatile",
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"Error with Groq API: {e}"

# Streamlit app
st.title("NFL Game Winner Prediction")
st.markdown("""
    Predict the winner of an NFL game between two selected teams.
    Use the prediction below or check the live scores!
""")

# Fetch and display live scores
live_scores = fetch_live_scores()

if live_scores:
    st.subheader("Live NFL Scores")
    for game in live_scores:
        team1 = game.get("team1_name", "Unknown Team 1")
        team2 = game.get("team2_name", "Unknown Team 2")
        score1 = game.get("team1_score", "N/A")
        score2 = game.get("team2_score", "N/A")
        st.write(f"{team1} {score1} - {team2} {score2}")

# Team selection for prediction
teams = [
    "Arizona Cardinals", "Atlanta Falcons", "Baltimore Ravens", "Buffalo Bills",
    "Carolina Panthers", "Chicago Bears", "Cincinnati Bengals", "Cleveland Browns",
    "Dallas Cowboys", "Denver Broncos", "Detroit Lions", "Green Bay Packers",
    "Houston Texans", "Indianapolis Colts", "Jacksonville Jaguars", "Kansas City Chiefs",
    "Las Vegas Raiders", "Los Angeles Chargers", "Los Angeles Rams", "Miami Dolphins",
    "Minnesota Vikings", "New England Patriots", "New Orleans Saints", "New York Giants",
    "New York Jets", "Philadelphia Eagles", "Pittsburgh Steelers", "San Francisco 49ers",
    "Seattle Seahawks", "Tampa Bay Buccaneers", "Tennessee Titans", "Washington Commanders"
]

# User input for teams
team1 = st.selectbox("Select Team 1", options=teams)
team2 = st.selectbox("Select Team 2", options=teams)

# Ensure different teams are selected
if team1 == team2:
    st.warning("Please select two different teams.")
else:
    # When the user clicks "Predict Winner"
    if st.button("Predict Winner"):
        # Use the prediction function to get the winner
        winner = predict_winner(team1, team2)

        # Display the result
        st.success(f"The predicted winner is: **{winner}**")
        
