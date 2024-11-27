import streamlit as st
import pandas as pd
import plotly.express as px
#
PLAYERS_DF = pd.read_csv("players_data.csv")
#
# page config
st.set_page_config(
    page_title="Injury news & Cards • FPL Infographics", page_icon=":soccer:",layout="wide"
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

# ############
YELLOW_DF = PLAYERS_DF.sort_values('yellow_cards',ascending=False).head(50)
YELLOW_DF.rename(columns={'web_name': 'Name'}, inplace=True)
RED_DF = PLAYERS_DF[PLAYERS_DF['red_cards'].ge(0)]
RED_DF = RED_DF.sort_values('red_cards',ascending=False).head(25)
RED_DF.rename(columns={'web_name': 'Name'}, inplace=True)

tab1, tab2,tab3= st.tabs(["Injuries :ambulance:","YELLOW Cards:large_yellow_square:","RED Cards:large_red_square:"])
with tab2:
    fig_YC = px.bar(YELLOW_DF, x='Name', y='yellow_cards',color='yellow_cards',color_continuous_scale='Blackbody_r')
    st.plotly_chart(fig_YC, theme="streamlit", use_container_width=False)
with tab3:
    fig_RC = px.bar(RED_DF, x='Name', y='red_cards',color='red_cards',color_continuous_scale='Blackbody_r')
    st.plotly_chart(fig_RC, theme="streamlit", use_container_width=False)
with tab1:
    D_DF = pd.read_csv("players_raw.csv")
    DOUBT_DF = D_DF[D_DF['status'] == 'd']
    DOUBT_DF['news_added'] = DOUBT_DF['news_added'].apply(lambda x: x.split('T')[0])
    DOUBT_DF = DOUBT_DF[['web_name','news','news_added']].sort_values('news_added',ascending=False)
    DOUBT_DF.rename(columns={'web_name': 'Name','news_added':'Updated'}, inplace=True)

    st.dataframe(data=DOUBT_DF,hide_index=True,use_container_width=False,width=1000, height=1500)