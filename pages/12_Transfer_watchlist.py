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
players_df = pd.read_csv('players_data.csv')
players_df.drop(players_df[players_df['status'] == 'u'].index, inplace=True)
players_df.drop(players_df[players_df['status'] == 'i'].index, inplace=True)
events_df = pd.read_csv('events.csv')
CURR_GW = events_df.loc[events_df['is_current'] == True]['id'].iloc[-1]
#
def get_picks_list(team_id):
    url = f"https://fantasy.premierleague.com/api/entry/%s/event/%s/picks/" % (team_id, CURR_GW)
    response = requests.get(url)
    data = response.json()
    picks = data.get("picks", [])
    picks_df = pd.DataFrame(picks)
    picks_list = picks_df['element'].to_list()
    return picks_list
def team_analysys(pickslist):
    df_my_team = players_df[players_df.id.isin(pickslist)]
    df_my_team = df_my_team[['web_name','photo','element_type','now_cost','selected_by_percent','total_points','points_per_game','money_value','form','goals_scored','expected_goals','assists','expected_assists','expected_goal_involvements','goal_involvements','ep_next','clean_sheets','bonus','next_3','next_3_avg_FDRs','next_5','next_5_avg_FDRs']]
    # Classic Leagues
    classic_df = pd.json_normalize(data['leagues']['classic'])
    classic_df = classic_df[['name','entry_rank','entry_last_rank','entry_percentile_rank']]
    # Tabs
    tab1, tab2 = st.tabs(["Your team performance indicators", "Mini-League performance"])
    with tab1:
        st.dataframe(df_my_team,hide_index=True,use_container_width=False,height=550,
                     column_config={"web_name":"Name","element_type":"Position","now_cost":"Cost","selected_by_percent":"Selected by (%)","total_points":"Total points","points_per_game":"PPG","money_value":"PPM£","goals_scored":"GS","expected_goals":"xG","assists":"A","expected_assists":"xA","expected_goal_involvements":"xGI","goal_involvements":"GI","ep_next": "xP(next GW)","clean_sheets":"CS",
                                    "photo": st.column_config.ImageColumn(label=""),
                                    "next_3_avg_FDRs":st.column_config.ProgressColumn(format="%f",min_value=0,max_value=5,),
                                    "next_5_avg_FDRs":st.column_config.ProgressColumn(format="%f",min_value=0,max_value=5,)
                                    })
    with tab2:
        st.dataframe(classic_df,hide_index=True,use_container_width=False)
#
def transfer_watchlist(pickslist):
    df_watchlist=players_df[~players_df.id.isin(pickslist)]
    df_watchlist = df_watchlist[['web_name','photo','element_type','now_cost','selected_by_percent','total_points','points_per_game','money_value','form','goals_scored','expected_goals','assists','expected_assists','expected_goal_involvements','goal_involvements','ep_next','clean_sheets','bonus','ict_index_rank','next_3','next_3_FDRs','next_3_avg_FDRs','next_5','next_5_FDRs','next_5_avg_FDRs','team']]
#
    df_watchlist_xgi = df_watchlist.sort_values('expected_goal_involvements',ascending=False).head(15)
    df_watchlist_xgi = df_watchlist_xgi[['web_name','element_type','now_cost','selected_by_percent','total_points','goals_scored','expected_goals','assists','expected_assists','expected_goal_involvements','goal_involvements']]
    df_watchlist_xgi_names = df_watchlist_xgi['web_name']
#
    df_watchlist_form = df_watchlist.sort_values('form',ascending=False).head(15)
    df_watchlist_form = df_watchlist_form[['web_name','element_type','now_cost','selected_by_percent','total_points','form','goals_scored','assists','goal_involvements']]
    df_watchlist_form_names = df_watchlist_form['web_name']
#
    df_watchlist_ppg = df_watchlist.sort_values('points_per_game',ascending=False).head(15)
    df_watchlist_ppg = df_watchlist_ppg[['web_name','element_type','now_cost','selected_by_percent','total_points','points_per_game','goals_scored','assists','goal_involvements']]
    df_watchlist_ppg_names = df_watchlist_ppg['web_name']
#
    df_watchlist_ict = df_watchlist.sort_values('ict_index_rank',ascending=True).head(15)
    df_watchlist_ict = df_watchlist_ict[['web_name','element_type','now_cost','selected_by_percent','total_points','goals_scored','expected_goals','assists','expected_assists','expected_goal_involvements','goal_involvements','bonus','ict_index_rank']]   
    df_watchlist_ict_names = df_watchlist_ict['web_name']
#
    df_watchlist_next_ep = df_watchlist.sort_values('ep_next',ascending=False).head(15)
    df_watchlist_next_ep = df_watchlist_next_ep[['web_name','element_type','now_cost','selected_by_percent','total_points','ep_next','goals_scored','expected_goals','assists','expected_assists','expected_goal_involvements','goal_involvements']]
#
    df_watchlist_names = pd.concat([df_watchlist_xgi_names,df_watchlist_ppg_names,df_watchlist_form_names,df_watchlist_ict_names])
    df_watchlist_names = df_watchlist_names.unique()
    df_watchlist_stats = players_df[players_df.web_name.isin(df_watchlist_names)]
    df_watchlist_table = df_watchlist_stats[['web_name','photo','team','position','now_cost','expected_goal_involvements','form','points_per_game','money_value','ict_index_rank','next_3_avg_FDRs','next_5_avg_FDRs']]
# plots
    fig_xgi = px.bar(df_watchlist_xgi, x='web_name', y='expected_goal_involvements',color='expected_goal_involvements')
    fig_form = px.bar(df_watchlist_form, x='web_name', y='form',color='form')
    fig_ppg = px.bar(df_watchlist_ppg, x='web_name', y='points_per_game',color='points_per_game')
    fig_ep = px.bar(df_watchlist_next_ep, x='web_name', y='ep_next',color='ep_next')
# Tabs
    tab1, tab2, tab3, tab4,tab5 = st.tabs(["Multi-factor list","Expected Goal Involvements", "Form", "Points per Game", "Expected points - next gameweek"])
    with tab1:
        st.markdown(
            "##### Based on: :green["
            + "XGI, Form, PPG, ICT Index ranking & FDR"
            + """] 
            """
        )
        st.caption("Click on any column to sort by that stat")
        st.dataframe(df_watchlist_table,hide_index=True,use_container_width=False,height=1025,width=1200,
                     column_config={
                         "web_name":"Name",
                         "now_cost":"Price",
                         "expected_goal_involvements":"xGI",
                         "points_per_game":"PPG",
                         "money_value":"PPM£",
                         "next_3_avg_FDRs":st.column_config.ProgressColumn(format="%f",min_value=0,max_value=5,),
                         "next_5_avg_FDRs":st.column_config.ProgressColumn(format="%f",min_value=0,max_value=5,),
                         "photo": st.column_config.ImageColumn(label="")
                         })
    with tab2:
        st.plotly_chart(fig_xgi, theme=None, use_container_width=False)
    with tab3:
        st.plotly_chart(fig_form, theme=None, use_container_width=False)
    with tab4:
        st.plotly_chart(fig_ppg, theme=None, use_container_width=False)
    with tab5:
         st.plotly_chart(fig_ep, theme=None, use_container_width=False)
## main
if 'team_id' not in st.session_state:
        st.session_state['team_id'] = ''
team_id = st.text_input("Enter your FPL ID")
##############################
if st.button('Analyse & get transfer watchlist'):
    with st.spinner("Analysis ongoing"):
        url = f"https://fantasy.premierleague.com/api/entry/{team_id}"
        response = requests.get(url)
        data = response.json()
        first_name = data.get("player_first_name")
        last_name = data.get("player_last_name")
        player_name = first_name + " "+ last_name
        team_name = data.get("name")
        overall_points = data.get("summary_overall_points")
        overall_rank = data.get("summary_overall_rank")
        #
        st.subheader(f"Hello :blue[{player_name}] ")
        st.caption(f"**Team** : :green[{team_name}] ")
        st.caption(f"**Overall points** : :green[{overall_points}] ")
        st.caption(f"**Overall rank** : :green[{overall_rank}] ")
        st.divider()
        my_picks = get_picks_list(team_id)
        tab1,tab2 = st.tabs(["Your Team", "Transfer Watchlist"])
        with tab1:
            team_analysys(my_picks)
        with tab2:
            transfer_watchlist(my_picks)
        st.balloons()
##############################