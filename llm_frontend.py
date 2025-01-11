import streamlit as st
import google.generativeai as gemini
import pandas as pd
import requests

# Configure Google Gemini API
gemini.configure(api_key="YOUR_GOOGLE_GEMINI_API_KEY")  # Replace with your valid API key

# RapidAPI Authentication
RAPIDAPI_KEY = "617a03432mshf2f3c8ac5cebb97p1a8e59jsne6c48986fdfd"  # Replace with your RapidAPI key
RAPIDAPI_HOST = "nfl-api.p.rapidapi.com"  # Host for RapidAPI's NFL API

# List of all NFL teams (for dropdown selection)
NFL_TEAMS = [
    "Arizona Cardinals", "Atlanta Falcons", "Baltimore Ravens", "Buffalo Bills",
    "Carolina Panthers", "Chicago Bears", "Cincinnati Bengals", "Cleveland Browns",
    "Dallas Cowboys", "Denver Broncos", "Detroit Lions", "Green Bay Packers",
    "Houston Texans", "Indianapolis Colts", "Jacksonville Jaguars", "Kansas City Chiefs",
    "Las Vegas Raiders", "Los Angeles Chargers", "Los Angeles Rams", "Miami Dolphins",
    "Minnesota Vikings", "New England Patriots", "New Orleans Saints", "New York Giants",
    "New York Jets", "Philadelphia Eagles", "Pittsburgh Steelers", "San Francisco 49ers",
    "Seattle Seahawks", "Tampa Bay Buccaneers", "Tennessee Titans", "Washington Commanders"
]

# Function to fetch historical data
def fetch_historical_data(team1, team2):
    # Replace this with real historical data
    data = {
        "Team1": [team1, team1, team2, team2],
        "Team2": [team2, team2, team1, team1],
        "Team1_Score": [24, 30, 20, 21],
        "Team2_Score": [20, 27, 24, 28],
        "Winner": [team1, team1, team2, team2],
    }
    return pd.DataFrame(data)

# Function to fetch live data from RapidAPI NFL API
def fetch_live_stats(team1, team2):
    url = f"https://{RAPIDAPI_HOST}/games?team1={team1}&team2={team2}"

    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": RAPIDAPI_HOST
    }
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()  # Returns live data as JSON
        else:
            return {"error": f"API Error: {response.status_code}"}
    except Exception as e:
        return {"error": f"Request failed: {str(e)}"}

# Function to generate prediction using Google Gemini
def predict_winner_with_live_data(team1, team2, historical_data, live_data):
    prompt = f"""
    You are an NFL expert. Predict the winner between {team1} and {team2}.
    Here is the historical data:
    {historical_data.to_string(index=False)}

    Here is the live data for today's game:
    {live_data}

    Based on this data, which team is more likely to win and why?
    """
    try:
        response = gemini.generate_text(prompt=prompt)
        return response['text']
    except Exception as e:
        return f"Error with Google Gemini: {str(e)}"

# Streamlit app
st.title("NFL Winner Predictor")
st.write("Predict the winner of an NFL game using historical and live data.")

# Dropdown for selecting teams
team1 = st.selectbox("Select Team 1:", NFL_TEAMS)
team2 = st.selectbox("Select Team 2:", NFL_TEAMS)

if team1 == team2:
    st.warning("Please select two different teams to predict the winner.")
else:
    if st.button("Predict Winner"):
        with st.spinner("Fetching data and making predictions..."):
            # Fetch historical data
            historical_data = fetch_historical_data(team1, team2)

            # Fetch live data from RapidAPI
            live_data = fetch_live_stats(team1, team2)

            if "error" in live_data:
                st.error(live_data["error"])
            else:
                # Generate prediction
                prediction = predict_winner_with_live_data(team1, team2, historical_data, live_data)
                st.success("Prediction Complete!")
                st.subheader("Predicted Winner:")
                st.write(prediction)
