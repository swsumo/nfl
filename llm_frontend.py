# NFL Expert Model
from dotenv import load_dotenv
import streamlit as st
import os
import textwrap
import google.generativeai as genai

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Helper functions
def to_markdown(text):
    text = text.replace('\u2022', '  *')
    return textwrap.indent(text, '> ', predicate=lambda _: True)

def get_gemini_response(question):
    """Fetch response from Gemini model."""
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(question)
    return response.text

def predict_winner(home_team, away_team):
    """Predict winner between home and away team."""
    prompt = f"Based on NFL historical data and team performance, who is likely to win: {home_team} (home) vs {away_team} (away)?"
    return get_gemini_response(prompt)

# List of all NFL teams (for dropdown)
nfl_teams = [
    "Arizona Cardinals", "Atlanta Falcons", "Baltimore Ravens", "Buffalo Bills", 
    "Carolina Panthers", "Chicago Bears", "Cincinnati Bengals", "Cleveland Browns", 
    "Dallas Cowboys", "Denver Broncos", "Detroit Lions", "Green Bay Packers", 
    "Houston Texans", "Indianapolis Colts", "Jacksonville Jaguars", "Kansas City Chiefs", 
    "Las Vegas Raiders", "Los Angeles Chargers", "Los Angeles Rams", "Miami Dolphins", 
    "Minnesota Vikings", "New England Patriots", "New Orleans Saints", "New York Giants", 
    "New York Jets", "Philadelphia Eagles", "Pittsburgh Steelers", "San Francisco 49ers", 
    "Seattle Seahawks", "Tampa Bay Buccaneers", "Tennessee Titans", "Washington Commanders"
]

# Streamlit app setup
st.set_page_config(page_title="NFL Expert Model")
st.header("NFL Expert Model")

# Winner Prediction
st.subheader("Winner Prediction")

# Dropdown for team selection
home_team = st.selectbox("Select Home Team:", nfl_teams)
away_team = st.selectbox("Select Away Team:", nfl_teams)

# Ensure home and away teams are different
if home_team == away_team:
    st.error("Please select different teams for home and away.")
else:
    if st.button("Predict Winner"):
        result = predict_winner(home_team, away_team)
        st.write(f"Prediction: {result}")
