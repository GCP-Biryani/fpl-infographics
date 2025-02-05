import streamlit as st
import pandas as pd
import plotly.express as px
from charts import *
import matplotlib.pyplot as plt
import seaborn as sns
#
events_df = pd.read_csv('events.csv')
fixtures = pd.read_csv('fixtures.csv')
CURR_GW = events_df.loc[events_df['is_current'] == True]['id'].iloc[-1]
#
# page config
st.set_page_config(
    page_title="Team FORM & FDR analysis:bar_chart:", page_icon=":soccer:",layout="wide"
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
# #
st.markdown(
    "#### FDR Analysis:bar_chart:"
)
##
def fixtures_by_team(fixtures, team, gameweek):
    away_df = fixtures.loc[fixtures['team_a'] == team]
    away = away_df.copy()
    away.rename(columns={'team_a': 'selected_team', 'team_h': 'opponent', 'team_a_difficulty': 'FDR', 'team_a_score': 'selected_team_score', 'team_h_score': 'opponent_score'}, inplace=True)
    away['h_or_a'] = 'Away'
    home_df = fixtures.loc[fixtures['team_h'] == team]
    home = home_df.copy()
    home.rename(columns={'team_h': 'selected_team', 'team_a': 'opponent', 'team_h_difficulty': 'FDR', 'team_h_score': 'selected_team_score',  'team_a_score': 'opponent_score'}, inplace=True)
    home['h_or_a'] = 'Home'
    combined = pd.concat([away, home])
    return combined.loc[combined['Gameweek'] <= gameweek].sort_values(by='Gameweek')
#######################
## FORM & FDR
#######################
tabx,taby = st.tabs(["FDR", "FDR Analysis"])
with tabx:
    gameweek = CURR_GW
    values = st.slider("Select the period", gameweek+1, 38, (gameweek+1, gameweek+3))
    GAMEWEEKS_PLAYED = values[0]
    period = (values[1] - values[0])+1
    #
    fixtures_going_forward = fixtures.loc[fixtures['Gameweek'] > gameweek]
    #
    pl_teams = fixtures['team_h'].unique()
    fixture_matrix_fdr = pd.DataFrame({'Teams': pl_teams})
    fixture_matrix_fdr['next_3_fdr'] = fixture_matrix_fdr['Teams'].apply(lambda x: fixtures_by_team(fixtures_going_forward, x, GAMEWEEKS_PLAYED+period)['FDR'].mean())
    fixture_matrix_fdr.sort_values(by='next_3_fdr', ascending=True, inplace=True)
    fixture_matrix_fdr.drop('next_3_fdr', axis=1, inplace=True)
    #
    fixture_matrix_matches = fixture_matrix_fdr.copy()
    for i in range(GAMEWEEKS_PLAYED, GAMEWEEKS_PLAYED+period):
        gw_fix = []
        for team in fixture_matrix_fdr['Teams'].values:
            fdr = fixtures_by_team(fixtures_going_forward, team, GAMEWEEKS_PLAYED+period)['FDR'].values[i-GAMEWEEKS_PLAYED]
            gw_fix.append(fdr)
        fixture_matrix_fdr['GW {}'.format(i)] = gw_fix

    for i in range(GAMEWEEKS_PLAYED, GAMEWEEKS_PLAYED+period):
        gw_fix = []
        for team in fixture_matrix_fdr['Teams'].values:
            opponent = fixtures_by_team(fixtures_going_forward, team, GAMEWEEKS_PLAYED+period)['opponent'].values[i-GAMEWEEKS_PLAYED]
            h_or_a = fixtures_by_team(fixtures_going_forward, team, GAMEWEEKS_PLAYED+period)['h_or_a'].values[i-GAMEWEEKS_PLAYED]
            gw_fix.append('{}, {}'.format(opponent, h_or_a))
        fixture_matrix_matches['GW {}'.format(i)] = gw_fix
    #
    fig, ax = plt.subplots(figsize=(15,15)) 
    ax = sns.heatmap(fixture_matrix_fdr.set_index('Teams'), annot=fixture_matrix_matches.set_index('Teams'), fmt='', linewidth=.5, cmap='RdYlGn_r')
    plt.tick_params(axis='both', which='major', labelsize=16, labelbottom = False, bottom=False, top = False, labeltop=True)
    fig1 = ax.get_figure()
    st.pyplot(fig=fig1)
with taby:
    TEAM_FDR_DF = pd.read_csv('team_fdr.csv', index_col=False)
    fdr_opt = st.radio(
    "Select a period",
    options=[
        "Avg FDR(Next 3)",
        "Avg FDR5(Next 5)",
        "Avg FDR(Next 10)",
        "Avg FDR(Remaining Season)",
    ],horizontal=True
    )
    fig = px.bar(TEAM_FDR_DF,x=fdr_opt,y='Team',color=fdr_opt,color_continuous_scale='plasma_r',text=fdr_opt,orientation='h')
    fig.update_layout(autosize=False,width=1500,height=700)
    st.plotly_chart(fig, theme=None)