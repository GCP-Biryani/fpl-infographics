import streamlit as st
import pandas as pd
import plotly.express as px
import soccerdata as sd
from charts import *
#
#
# page config
st.set_page_config(
    page_title="Team stats analysis", page_icon=":soccer:",layout="wide"
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
    st.page_link("pages/2_Teams_analysis.py", label="Team Analysis", icon=":material/monitoring:",help="Each teams expected goals, expected goals against charts gives you a view of attack & defense permonce of the team over the season")
    st.page_link("pages/3_Player_history.py", label="Player season history", icon=":material/history:",help="Player gameweek history with stats like expected,points,BPS")
    st.page_link("pages/4_Team_form_&_FDR.py", label="Team Form & FDR", icon=":material/flowsheet:",help="Team recent form - goals scored, points per game,clean sheets, no of games team scrored in")
    st.page_link("pages/6_Set_Piece_Takers.py", label="Set-Piece takers", icon=":material/flag:",help="Penalties, corners, free kicks - whos on them")
    st.page_link("pages/8_Injuries_&_Cards.py", label="Injuries & Cards", icon=":material/style:",help="Latest injury news & Yellow, red cards table")
    st.page_link("pages/9_Price_changes.py", label="Price changes & Predictions", icon=":material/currency_pound:",help="Today price change and predicted price changes for the next few days")
    st.page_link("pages/12_Transfer_watchlist.py", label="Transfer recommondations", icon=":material/transfer_within_a_station:",help="Get your team performance, mini-league performance and Watch list picks based on expected goal involvements, points per game, Form, next gameweek expected points and Infuence+Creativity+Threat rank")
    st.page_link("pages/10_Mini-league_Analyser.py", label="Mini-leagye (ML) Analyser", icon=":material/analytics:",help="Mini-league analysis - player ownership, captain choice, league race, each team xGI, bench points, team value")
    st.page_link("pages/11_Compare_Teams.py", label="ML Teams comparision tool", icon=":material/compare_arrows:",help="compare teams from mini-league and see common picks and differentials + points by each position")
    st.page_link("pages/fbref_compare.py", label="Players comparision tool", icon=":material/compare:",help="Compare player stats using radar charts for performance,shooting,passing,defensive stats")
    st.page_link("pages/12_ALL_Player_Stats.py", label="ALL STATS", icon=":material/select_all:",help="All available stats for all players")
#

# #
st.markdown(
    "#### Team stats Analysis :chart_with_upwards_trend: - Attack, Defense, Expected vs Actual"
)
# Team dataframes
fbref = sd.FBref(leagues="ENG-Premier League", seasons=2024)
DF_ARS = pd.read_csv('fbref-Arsenal.csv')
DF_AVL = pd.read_csv('fbref-Aston Villa.csv')
DF_BOU = pd.read_csv('fbref-Bournemouth.csv')
DF_BRE = pd.read_csv('fbref-Brentford.csv')
DF_BRI = pd.read_csv('fbref-Brighton.csv')
DF_CHE = pd.read_csv('fbref-Chelsea.csv')
DF_CRY = pd.read_csv('fbref-Crystal Palace.csv')
DF_EVE = pd.read_csv('fbref-Everton.csv')
DF_FUL = pd.read_csv('fbref-Fulham.csv')
DF_IPS = pd.read_csv('fbref-Ipswich Town.csv')
DF_LEI = pd.read_csv('fbref-Leicester City.csv')
DF_LIV = pd.read_csv('fbref-Liverpool.csv')
DF_MNC = pd.read_csv('fbref-Manchester City.csv')
DF_MNU = pd.read_csv('fbref-Manchester Utd.csv')
DF_NEW = pd.read_csv('fbref-Newcastle Utd.csv')
DF_NFO = pd.read_csv('fbref-NFO.csv')
DF_SOU = pd.read_csv('fbref-Southampton.csv')
DF_TOT = pd.read_csv('fbref-Tottenham.csv')
DF_WHU = pd.read_csv('fbref-West Ham.csv')
DF_WOL = pd.read_csv('fbref-Wolves.csv')

# team tabs
tab1,tab2,tab3,tab4,tab5,tab6,tab7,tab8,tab9,tab10,tab11,tab12,tab13,tab14,tab15,tab16,tab17,tab18,tab19,tab20 = st.tabs(["ARS","AVL","BOU", "BRE","BRI","CHE","CRY","EVE","FUL","IPS","LEI","LIV","MNC","MNU","NEW","NFO","SOU","TOT","WHU","WOL"])
with tab1:
    chart_tabs(DF_ARS)
with tab2:
    chart_tabs(DF_AVL)
with tab3:
    chart_tabs(DF_BOU)
with tab4:
    chart_tabs(DF_BRE)
with tab5:
    chart_tabs(DF_BRI)
with tab6:
    chart_tabs(DF_CHE)
with tab7:
    chart_tabs(DF_CRY)
with tab8:
    chart_tabs(DF_EVE)
with tab9:
    chart_tabs(DF_FUL)
with tab10:
    chart_tabs(DF_IPS)
with tab11:
    chart_tabs(DF_LEI)
with tab12:
    chart_tabs(DF_LIV)
with tab13:
    chart_tabs(DF_MNC)
with tab14:
    chart_tabs(DF_MNU)
with tab15:
    chart_tabs(DF_NEW)
with tab16:
    chart_tabs(DF_NFO)
with tab17:
    chart_tabs(DF_SOU)
with tab18:
    chart_tabs(DF_TOT)
with tab19:
    chart_tabs(DF_WHU)
with tab20:
    chart_tabs(DF_WOL)
