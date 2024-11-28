import streamlit as st
import pandas as pd
import requests
import plotly.express as px
from bs4 import BeautifulSoup
from io import StringIO
from tabulate import tabulate
pd.options.mode.chained_assignment = None

#
PLAYERS_DF = pd.read_csv("players_data.csv")
#
# page config
st.set_page_config(
    page_title="Latest price changes • FPL Infographics", page_icon=":soccer:",layout="wide"
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
############
st.markdown(
    "##### :money_mouth_face: Price changes & price predictions"
)
tab1, tab2 = st.tabs(["Today price changes","Price change predictions"])
with tab2:
    url = 'https://www.livefpl.net/prices'          # Price Change prediction
    header = ({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'})
    html_text = requests.get(url, headers=header).text
    soup = BeautifulSoup(html_text, 'lxml')
    table = soup.find_all('table')[2]
    df = pd.read_html(StringIO(str(table)))[0]
    headers = []
    rows = []
    for i, row in enumerate(table.find_all('tr')):
        if i == 0:
            headers = [el.text.strip() for el in row.find_all('th')]
        else:
            rows.append([el.text.strip() for el in row.find_all('td')])

    table = tabulate(
        rows, 
        headers=["State", "Predicted Rises", "Predicted Falls"], 
        tablefmt="rounded_grid"
    )
    st.dataframe(df,hide_index=True,width=1300,column_config={
        "Unnamed: 0":"Prediction",
        "Predicted Falls": st.column_config.TextColumn(
            "Predicted Falls",
            width=750,
        )})
with tab1:
    url = 'https://www.livefpl.net/price_changes'          # Price Changes
    header = ({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'})
    html_text = requests.get(url, headers=header).text
    soup = BeautifulSoup(html_text, 'lxml')
    table = soup.find_all('table')[0]
    df = pd.read_html(StringIO(str(table)))[0]
    headers = []
    rows = []
    for i, row in enumerate(table.find_all('tr')):
        if i == 0:
            headers = [el.text.strip() for el in row.find_all('th')]
        else:
            rows.append([el.text.strip() for el in row.find_all('td')])

    table1 = tabulate(
        rows, 
        headers=["Player", "Team", "Old price", "New Price"], 
        tablefmt="rounded_grid"
    )
    st.dataframe(df,hide_index=True,width=1400)