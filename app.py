import streamlit as st
import numpy as np
import pandas as pd
import pickle

st.set_page_config(
    page_title="IPL 2024 Score prediction",
    page_icon="🏏",)
# st.title("IPL 2024 Score prediction")

with open("./ipl_model.pkl", "rb") as f:
    model = pickle.load(f)


teams = sorted(['Kolkata Knight Riders',
                'Chennai Super Kings',
                'Rajasthan Royals',
                'Sunrisers Hyderabad',
                'Royal Challengers Bengaluru',
                'Gujarat Titans',
                'Delhi Capitals',
                'Punjab Kings',
                'Mumbai Indians',
                'Lucknow Super Giants'])

cities = sorted(['Mumbai', 'Pune', 'Navi Mumbai', 'Kolkata', 'Ahmedabad', 'Lucknow',
                 'Chandigarh', 'Bengaluru', 'Hyderabad', 'Chennai', 'Delhi',
                 'Guwahati', 'Jaipur', 'Dharamsala', 'Mohali', 'Visakhapatnam'])


def score_predict(batting_team,
                  bowling_team,
                  runs, wickets, overs, runs_last_5, wickets_last_5, fours, sixes, city, model=model) -> int:
    cols = ['overs', 'runs', 'wickets', 'last5_runs', 'last5_wickets', 'fours',
            'sixes', 'total', 'batting_team_Chennai Super Kings',
            'batting_team_Delhi Capitals', 'batting_team_Gujarat Titans',
            'batting_team_Kolkata Knight Riders',
            'batting_team_Lucknow Super Giants', 'batting_team_Mumbai Indians',
            'batting_team_Punjab Kings', 'batting_team_Rajasthan Royals',
            'batting_team_Royal Challengers Bengaluru',
            'batting_team_Sunrisers Hyderabad', 'bowling_team_Chennai Super Kings',
            'bowling_team_Delhi Capitals', 'bowling_team_Gujarat Titans',
            'bowling_team_Kolkata Knight Riders',
            'bowling_team_Lucknow Super Giants', 'bowling_team_Mumbai Indians',
            'bowling_team_Punjab Kings', 'bowling_team_Rajasthan Royals',
            'bowling_team_Royal Challengers Bengaluru',
            'bowling_team_Sunrisers Hyderabad', 'city_Ahmedabad', 'city_Bengaluru',
            'city_Chandigarh', 'city_Chennai', 'city_Delhi', 'city_Dharamsala',
            'city_Guwahati', 'city_Hyderabad', 'city_Jaipur', 'city_Kolkata',
            'city_Lucknow', 'city_Mohali', 'city_Mumbai', 'city_Navi Mumbai',
            'city_Pune', 'city_Visakhapatnam']
    pred_array = pd.DataFrame([[0 for _ in range(len(cols))]], columns=cols)
    pred_array.drop('total', axis=1, inplace=True)
    pred_array['overs'] = overs
    pred_array['runs'] = runs
    pred_array['wickets'] = wickets
    pred_array['last5_runs'] = runs_last_5
    pred_array['last5_wickets'] = wickets_last_5
    pred_array['fours'] = fours
    pred_array['sixes'] = sixes
    pred_array[f"batting_team_{batting_team}"] = 1
    pred_array[f"bowling_team_{bowling_team}"] = 1
    pred_array[f"city_{city}"] = 1

    pred = model.predict(pred_array.values)
    return int(round(pred[0]))


with st.form("Model inputs"):
    col1, col2 = st.columns(2)
    ba_idx, bo_idx = np.random.choice(len(teams), 2)
    if "bat_team" not in st.session_state:
        st.session_state.bat_team = teams[ba_idx]
    if "bowl_team" not in st.session_state:
        st.session_state.bowl_team = teams[bo_idx]
    with col1:
        bat_team = st.selectbox(
            'Batting Team', teams, key="bat_team")
    with col2:
        bowl = st.selectbox(
            'Bowling Team', teams, key="bowl_team")

    # Create a slider with the custom formatting function

    def str_format(x): return f"{x//6}.{x % 6}"
    if "city" not in st.session_state:
        st.session_state.city = cities[ba_idx]
    city = st.selectbox('city', cities,key="city")

    overs_slider = st.select_slider("Overs", options=range(
        30, 121, 1), format_func=str_format)
    col1, col2 = st.columns(2)

    with col1:
        runs = st.number_input("Runs", 0, 800, format="%d")
        fours = st.number_input("Fours", 0, 120, format="%d")
        last5_rus = st.number_input(
            "Runs scored in last 5 overs", 0, 180, format="%d")

    with col2:
        wickets = st.number_input("Wickets", 0, 10, format="%d")
        sixes = st.number_input("Sixes", 0, 120, format="%d")
        last5_wickets = st.number_input(
            "Wickets lost in last 5 overs", 0, 10, format="%d")

    submitted = st.form_submit_button("Submit")
if submitted:
    if bat_team == bowl:
        st.error("Please choose different batting and bowling teams")
    elif last5_rus > runs:
        st.error(
            "Please make sure that runs scored in last 5 overs are less than or equal to total runs scored")
    elif last5_wickets > wickets:
        st.error(
            "Please make sure that wickets lost in last 5 overs are less than or equal to total wickets lost")
    else:
        st.markdown(f"# **Predicted runs are: {score_predict(batting_team=bat_team, bowling_team=bowl, runs=runs, wickets=wickets, overs=str_format(overs_slider), runs_last_5=last5_rus, wickets_last_5=last5_wickets, fours=fours, sixes=sixes, city=city)}**")

st.markdown("This app is inspired from the works of [Satyajit Pattnaik](https://www.youtube.com/@SatyajitPattnaik)")