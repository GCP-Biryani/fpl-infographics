import streamlit as st
import pandas as pd
import requests
#
events_df = pd.read_csv('events.csv')
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
    #
    st.page_link("pages/1_Players_analysis.py", label="Player Analysis", icon=":material/analytics:",help="players performance, expected - goals, assists, involvements, shots, key passses, points per game, points per million and more..")
    st.page_link("pages/2_Teams_analysis.py", label="Team Analysis", icon=":material/monitoring:",help="Team form, Each teams expected goals, expected goals against charts gives you a view of attack & defense permonce of the team over the season")
    st.page_link("pages/3_Player_history.py", label="Player season history", icon=":material/history:",help="Player gameweek history with stats like expected,points,BPS")
    st.page_link("pages/4_Team_form_&_FDR.py", label="FDR", icon=":material/flowsheet:",help="Fixture difficulty rating")
    st.page_link("pages/6_Set_Piece_Takers.py", label="Set-Piece takers", icon=":material/flag:",help="Penalties, corners, free kicks - whos on them")
    st.page_link("pages/8_Injuries_&_Cards.py", label="Injuries & Cards", icon=":material/style:",help="Latest injury news & Yellow, red cards table")
    st.page_link("pages/9_Price_changes.py", label="Price changes & Predictions", icon=":material/currency_pound:",help="Today price change and predicted price changes for the next few days")
    st.page_link("pages/12_Transfer_watchlist.py", label="Transfer recommondations", icon=":material/transfer_within_a_station:",help="Get your team performance, mini-league performance and Watch list picks based on expected goal involvements, points per game, Form, next gameweek expected points and Infuence+Creativity+Threat rank")
    st.page_link("pages/10_Mini-league_Analyser.py", label="Mini-leagye (ML) Analyser", icon=":material/analytics:",help="Mini-league analysis - player ownership, captain choice, league race, each team xGI, bench points, team value")
    st.page_link("pages/11_Compare_Teams.py", label="ML Teams comparision tool", icon=":material/compare_arrows:",help="compare teams from mini-league and see common picks and differentials + points by each position")
    st.page_link("pages/fbref_compare.py", label="Players comparision tool", icon=":material/compare:",help="Compare player stats using radar charts for performance,shooting,passing,defensive stats")
    st.page_link("pages/12_ALL_Player_Stats.py", label="ALL STATS", icon=":material/select_all:",help="All available stats for all players")
#
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
st.caption("FPL infographics can be incredibly helpful in making informed decisions by visualizing key stats and data in an easily digestible format. By transforming complex numbers and trends into graphs and tables, you can better understand player performances, team trends, and matchups.")
#