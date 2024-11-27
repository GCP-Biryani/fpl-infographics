import requests
import pandas as pd
import streamlit as st
from functions import *
##############################
# page config
st.set_page_config(
    page_title="Compare FPL teams", page_icon=":soccer:",layout="wide"
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
##
players_df = pd.read_csv('players_data.csv')
events_df = pd.read_csv('events.csv')
gwplayed = events_df.loc[events_df['is_current'] == True]['id'].iloc[-1]
#
if 'league_id' not in st.session_state:
    st.header("Please complete mini-league analysis and come back here")
    st.stop()
if 'league_id' in st.session_state:
    league_id = st.session_state.league_id
##
url1 = "https://fantasy.premierleague.com/api/leagues-classic/%s/standings/" % (league_id)
json_minileague = requests.get(url1).json()
results = json_minileague['standings']['results']
df_results = pd.DataFrame(results)

##
# get picks list
def get_picks(id,gwplayed):
    url = "https://fantasy.premierleague.com/api/entry/%s/event/%s/picks/" % (id, gwplayed)
    json_pick = requests.get(url).json()
    picks_df = pd.DataFrame(json_pick['picks'])
    list = picks_df['element'].to_list()
    return list

def get_name(pick):
    name = players_df.loc[players_df['id']== pick]['web_name'].iloc[-1]
    position = players_df.loc[players_df['id']== pick]['element_type'].iloc[-1]
    points = players_df.loc[players_df['id']== pick]['event_points'].iloc[-1]
    photo = players_df.loc[players_df['id']== pick]['photo'].iloc[-1]
    return [name,photo,position,points]


####
drop_list = df_results['entry_name']
#
col1, col2 = st.columns(2)
with col1:
    your_team = st.selectbox("Select Team1",drop_list,key='yours')
with col2:
    their_team = st.selectbox("Select Team2",drop_list)
##
your_team_id = df_results.loc[df_results['entry_name'] == your_team]['entry'].iloc[-1]
their_team_id = df_results.loc[df_results['entry_name'] == their_team]['entry'].iloc[-1]
#
your_list = get_picks(your_team_id,gwplayed)
opp_list = get_picks(their_team_id,gwplayed)

def compare_teams(your_id,their_id,gw):
    col1, col2 = st.columns(2)
    with col1:
        
        pbp = points_by_position(your_list)
        st.plotly_chart(pbp,theme=None,use_container_width=False,key='your')
        common = list(set(your_list).intersection(opp_list))
        common_picks = []
        for i in common:
            new = get_name(i)
            common_picks.append(new)
        df_common = pd.DataFrame(common_picks, columns=["Name","photo","Position","GW points"]).sort_values(by=['Position'])
        st.header("Common Players")
        st.dataframe(df_common,hide_index=True,use_container_width=False,column_config={"photo": st.column_config.ImageColumn(label="Image",width="small")})
        st.header("Differentials")
        yours = set(your_list).difference(opp_list)
        your_picks = []
        for i in yours:
            new = get_name(i)
            your_picks.append(new)
        df_yours = pd.DataFrame(your_picks, columns=["Name","photo","Position","GW points"]).sort_values(by=['Position'])
        st.dataframe(df_yours, hide_index=True,height=600,width=450,use_container_width=False,column_config={"photo": st.column_config.ImageColumn(label="Image",width="small")})
####
    with col2:
        
        pbp = points_by_position(opp_list)
        st.plotly_chart(pbp,theme=None,use_container_width=False,key='opp')
        common = list(set(your_list).intersection(opp_list))
        common_picks = []
        for i in common:
            new = get_name(i)
            common_picks.append(new)
        df_common = pd.DataFrame(common_picks, columns=["Name","photo","Position","GW points"]).sort_values(by=['Position'])
        st.header("Common Players")
        st.dataframe(df_common,hide_index=True,use_container_width=False,column_config={"photo": st.column_config.ImageColumn(label="Image",width="small")})
        st.header("Differentials")
        theirs = set(opp_list).difference(your_list)
        their_picks = []
        for i in theirs:
            new = get_name(i)
            their_picks.append(new)
        df_theirs = pd.DataFrame(their_picks, columns=["Name","photo","Position","GW points"]).sort_values(by=['Position'])
        st.dataframe(df_theirs,hide_index=True,height=600,width=450,use_container_width=False,column_config={"photo": st.column_config.ImageColumn(label="Image",width="small")})
def points_by_position(picks_list):
    team_picks = []
    for i in picks_list:
        new = get_name(i)
        team_picks.append(new)
    df_team_picks = pd.DataFrame(team_picks, columns=["Name","photo","Position","Points"]).groupby('Position',as_index=False).sum()
    fig_pos_scores = px.pie(df_team_picks,values='Points',names='Position',hover_data=['Name'],color='Position',hole=0.2)
    return fig_pos_scores
#
#
st.caption("* Additional captain points are not counted")
compare_teams(your_team_id,their_team_id,gwplayed)