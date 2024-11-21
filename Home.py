import streamlit as st
import pandas as pd
import requests
#
url = 'https://fantasy.premierleague.com/api/bootstrap-static/'
r = requests.get(url)
json1 = r.json()
events_df = pd.DataFrame(json1['events'])
CURR_GW = events_df.loc[events_df['is_current'] == True]['id'].iloc[-1]
#
# page config
st.set_page_config(
    page_title="Welcome to FPL Infographics", page_icon=":soccer:",layout="wide"
)
LOGO = "logo.png"
st.logo(
    LOGO,
    icon_image=LOGO,
    )
# sidebar
with st.sidebar:
    st.title(""":soccer: *FPL Infographics*""")
    st.caption("FPL infographics can be incredibly helpful in making informed decisions by visualizing key stats and data in an easily digestible format. By transforming complex numbers and trends into graphs and tables, you can better understand player performances, team trends, and matchups.")


# landing
st.title(":soccer: :rainbow[*FPL Infographics*]")
st.subheader(
    """**Your Ultimate Fantasy Premier League analysis graphs!**
"""
)

# latest gameweek
st.markdown(
    "##### Latest data update - Gameweek :blue["
    + str(CURR_GW)
    + """] 
 :blue[Use our latest data, stats, and models to prepare your team for success in Gameweek """
    + str(CURR_GW + 1)
    + ".]"
)
#
col1,col2,col3 = st.columns(3)
with col1:
    st.subheader("Player Analysis",divider='green')
    st.page_link("pages/1_Players_analysis.py", label=":green[**Player stats analysis**]", icon=":material/analytics:")
    st.caption("players performance, expected - goals, assists, involvements, shots, key passses, points per game, points per million and more.. ")
    st.page_link("pages/3_Player_history.py", label=":green[**Player's season history**] ", icon=":material/history:")
    st.caption("Player gameweek history with stats like expected,points,BPS ")
    st.page_link("pages/6_Set_Piece_Takers.py", label=":green[**Set-piece takers**] ", icon=":material/flag:")
    st.caption("Penalties, corners, free kicks - whos on them")
    st.page_link("pages/8_Injuries_&_Cards.py", label=":green[**Injuries:material/medical_services: & cards:material/style:**] ", icon=":material/info:")
    st.caption("Latest injury news & Yellow, red cards table")
with col3:
    st.subheader("Teams Analysis",divider='blue')
    st.page_link("pages/2_Teams_analysis.py", label=":blue[**Team STATS analysis**]", icon=":material/monitoring:")
    st.caption("Each teams expected goals, expected goals against charts gives you a view of attack & defense permonce of the team over the season")
    st.page_link("pages/4_Team_form_&_FDR.py", label=":blue[**Team form & FDR analysis**]", icon=":material/flowsheet:")
    st.caption("Team recent form - goals scored, points per game,clean sheets, no of games team scrored in")
with col2:
    st.subheader("Tools",divider='red')
    st.page_link("pages/12_Transfer_watchlist.py", label=":red[**Personalised transfer recommondations**]", icon=":material/analytics:")
    st.caption("Get your team performance, mini-league performance and Watch list picks based on expected goal involvements, points per game, Form, next gameweek expected points and Infuence+Creativity+Threat rank")
    st.page_link("pages/10_Mini-league_Analyser.py", label=":red[**Mini-league analyser**]", icon=":material/transfer_within_a_station:")
    st.caption("Mini-league analysis - player ownership, captain choice, league race, each team xGI, bench points, team value" )
    st.page_link("pages/11_Compare_Teams.py", label=":red[**Compare Teams**]", icon=":material/compare:")
    st.caption("compare teams from mini-league and see common picks and differentials + points by each position")
    st.page_link("pages/9_Price_changes.py", label=":red[**Price changes & predictions**]", icon=":material/currency_pound:")
    st.caption("Today price change and predicted price changes for the next few days")