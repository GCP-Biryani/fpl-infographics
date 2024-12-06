import streamlit as st
import requests
import pandas as pd
#
# page config
st.set_page_config(
    page_title="Player expected points (xP)", page_icon=":soccer:",layout="wide"
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
    st.page_link("pages/Expected_Points.py", label="Expected Points", icon=":material/psychology:",help="Expected points for selected gameweek")
    st.page_link("pages/12_ALL_Player_Stats.py", label="ALL STATS", icon=":material/select_all:",help="All available stats for all players")
#
events_df = pd.read_csv('events.csv')
CURR_GW = events_df.loc[events_df['is_current'] == True]['id'].iloc[-1]
df = pd.read_csv('fpl-form-predicted-points.csv')
def get_xp(id,gw,df):
    col = str(gw)+str('_pts')
    df_id = df.loc[df['ID'] == id, ['Name','Pos','Team',col]]
    return df_id
def get_my_team(team_id,CURR_GW,selected):
    url4 = f"https://fantasy.premierleague.com/api/entry/{team_id}/event/{CURR_GW}/picks/"
    json_pick = requests.get(url4).json()
    json_pick_df = pd.DataFrame(json_pick['picks'])
    picks = json_pick_df['element'].to_list()
#
    dfs = []
    for pick in picks:
        data = get_xp (pick,gw,df)
        dfs.append(data)
    final = pd.concat(dfs, ignore_index=True).sort_values(by=str(selected)+str('_pts'),ascending=False)
    st.dataframe(final,hide_index=True,use_container_width=False,height=600)
#
st.header('Expected Points (xP)')
gw = st.slider("Select the gameweek for predictions?", 15, 38, 15)
#
tab1,tab2,tab3,tab4,tab5 = st.tabs(['My Team', 'FWD', 'MID', 'DEF', 'GKP'])
with tab1:
    if 'team_id' not in st.session_state:
        st.session_state['team_id'] = ''
    team_id = st.text_input("Enter your FPL ID")
    if team_id:
        st.session_state['team_id'] = team_id
        with st.spinner("please wait..."):
            get_my_team(team_id,CURR_GW,gw)
with tab2:
    col = str(gw)+str('_pts')
    df_fwd = df.loc[df['Pos'] == 'FWD',['Name','Pos','Team',col]].sort_values(by=str(gw)+str('_pts'),ascending=False)
    st.dataframe(df_fwd,hide_index=True,use_container_width=False,width=600,height=1000)
with tab3:
    col1 = str(gw)+str('_pts')
    df_mid = df.loc[df['Pos'] == 'MID',['Name','Pos','Team',col1] ].sort_values(by=str(gw)+str('_pts'),ascending=False)
    st.dataframe(df_mid,hide_index=True,use_container_width=False,width=600,height=1000)
with tab4:
    col = str(gw)+str('_pts')
    df_def = df.loc[df['Pos'] == 'DEF',['Name','Pos','Team',col] ].sort_values(by=str(gw)+str('_pts'),ascending=False)
    st.dataframe(df_def,hide_index=True,use_container_width=False,width=600,height=1000)
with tab5:
    col = str(gw)+str('_pts')
    df_gkp = df.loc[df['Pos'] == 'GKP',['Name','Pos','Team',col] ].sort_values(by=str(gw)+str('_pts'),ascending=False)
    st.dataframe(df_gkp,hide_index=True,use_container_width=False,width=600,height=1000)