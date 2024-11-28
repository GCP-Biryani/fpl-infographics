import streamlit as st
from charts import *
#
# page config
st.set_page_config(
    page_title="Player stats analysis", page_icon=":soccer:",layout="wide"
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
# # Player data frames
FWD_DF = pd.read_csv("FWD_data.csv")
MID_DF = pd.read_csv("MID_data.csv")
DEF_DF = pd.read_csv("DEF_data.csv")
GKP_DF = pd.read_csv("GKP_data.csv")
#
st.markdown(
    "#### Player stats Analysis :chart_with_upwards_trend:"
)
# tabs
tabF,tabM,tabD,tabG,tabS = st.tabs(["Forwards","Midfielders","Defenders","Goal Keepers","Season Stars:star:"])
with tabF:
    player_stat_tabs(FWD_DF,'fwd')
with tabM:
    player_stat_tabs(MID_DF,'mid')
with tabD:
    player_stat_tabs(DEF_DF,'def')
# Goal keeper
with tabG:
    # FWD_DF_XGC = GKP_DF.sort_values('expected_goals_conceded',ascending=False).head(20)
    FWD_DF_XGC = GKP_DF.sort_values('expected_goals_conceded',ascending=False)
    FWD_DF_XGC = FWD_DF_XGC[FWD_DF_XGC['total_points'] > 0]
    tab1, tab2, tab3, tab4, tab5,tab6 = st.tabs(["Defense Performance","Total Points","Form","Points per Million","Points per Game","saves"])
    with tab1:
        price = st.slider("Select the max price",4.0,7.0,6.0,step=0.1,key='GKP')
        FWD_DF_XGC = FWD_DF_XGC[FWD_DF_XGC['now_cost'] <= price]
        fig_FWD_DF_perf = px.scatter(FWD_DF_XGC, x='goals_conceded', y='expected_goals_conceded',text='web_name')
        x_mean = FWD_DF_XGC['goals_conceded'].mean()
        y_mean = FWD_DF_XGC['expected_goals_conceded'].mean()
        fig_FWD_DF_perf.add_hline(y=y_mean,line_dash="dot",line_color='Blue')
        fig_FWD_DF_perf.add_vline(x=x_mean,line_dash="dot",line_color='Blue')
        fig_FWD_DF_perf.update_layout(autosize=False,width=1400,height=650)
        st.plotly_chart(fig_FWD_DF_perf, theme="streamlit", use_container_width=False)
        st.caption('lower-left quadrant better choice')
    with tab2:
        st.caption('Interactive - you can select the price bracket using mouse pointer ')
        fig = get_scatter(GKP_DF,'total_points')
        st.plotly_chart(fig,theme=None)
    with tab3:
        st.caption('Interactive - you can select the price bracket using mouse pointer ')
        fig = get_scatter(GKP_DF,'form')
        st.plotly_chart(fig,theme=None)
    with tab4:
        st.caption('Interactive - you can select the price bracket using mouse pointer ')
        fig = get_scatter(GKP_DF,'money_value')
        st.plotly_chart(fig,theme=None)
    with tab5:
        st.caption('Interactive - you can select the price bracket using mouse pointer ')
        fig = get_scatter(GKP_DF,'points_per_game')
        st.plotly_chart(fig,theme=None)
    with tab6:
        st.caption('Interactive - you can select the price bracket using mouse pointer ')
        fig = get_scatter(GKP_DF,'saves')
        st.plotly_chart(fig,theme=None)
with tabS:
    PLAYERS_DF = pd.read_csv("players_data.csv")
    PLAYERS_DF = PLAYERS_DF.rename(columns={'web_name':'Name'})
    PLAYERS_DF['goal_involvements'] = PLAYERS_DF['goals_scored'] + PLAYERS_DF['assists']
    PLAYERS_DF['money_value'] = PLAYERS_DF['total_points'] / PLAYERS_DF['now_cost']
    ##########
    def GET_DF(STAT):
        TOP_DF = PLAYERS_DF.sort_values(STAT,ascending=False).head(1)
        PHOTO = TOP_DF.photo.to_string(index=False)
        TOP_DF['IMAGE'] = f'https://resources.premierleague.com/premierleague/photos/players/250x250/p{PHOTO}'
        TOP_DF['IMAGE'] = TOP_DF['IMAGE'].str.replace('jpg','png')
        TOP_DF = TOP_DF[['IMAGE','Name',STAT]]
        return TOP_DF
############
    def DATA_EDITOR(DF):
        return st.data_editor(DF,column_config={"IMAGE": st.column_config.ImageColumn(label="")},hide_index=True,disabled=True)
############
    col1, col3,col4,col5,col6 = st.columns(5)
    with col1:
        st.caption("### :green[Goals]")
        TOP_GS = GET_DF("goals_scored")
        DATA_EDITOR(TOP_GS)   
    with col3:
        st.caption("### :green[Assists]")
        TOP_A = GET_DF("assists")
        DATA_EDITOR(TOP_A)
    with col4:
        st.caption("### :green[Goal Involvements]")
        TOP_GI = GET_DF("goal_involvements")
        DATA_EDITOR(TOP_GI)
    with col5:
        st.caption("### :green[Shots]")
        TOP_SHOTS = GET_DF("shots")
        DATA_EDITOR(TOP_SHOTS)
    with col6:
        st.caption("### :green[Key passes]")
        TOP_KP = GET_DF("key_passes")
        DATA_EDITOR(TOP_KP)
############
    col1, col2, col3,col4 = st.columns(4)
    with col1:
        st.caption("### :green[xG]")
        TOP_XG = GET_DF("expected_goals")
        DATA_EDITOR(TOP_XG)
    with col2:
        st.caption("### :green[Non-penalty xG]")
        TOP_NPXG = GET_DF("np_xg")
        DATA_EDITOR(TOP_NPXG)
    with col3:
        st.caption("### :green[xA]")
        TOP_XA = GET_DF("expected_assists")
        DATA_EDITOR(TOP_XA)
    with col4:
        st.caption("### :green[xGI]")
        TOP_XGI = GET_DF("expected_goal_involvements")
        DATA_EDITOR(TOP_XGI)
############
    col2, col4,col5 = st.columns(3)
    with col2:
        st.caption("### :green[Total Points]")
        TOP_XA = GET_DF("total_points")
        DATA_EDITOR(TOP_XA)
    with col4:
        st.caption("### :green[Points per Million]")
        TOP_MV = GET_DF("money_value")
        DATA_EDITOR(TOP_MV)
    with col5:
        st.caption("### :green[Points per Game]")
        TOP_PPG = GET_DF("points_per_game")
        DATA_EDITOR(TOP_PPG)
############
    col1, col2, col3 = st.columns(3)
    with col1:
        st.caption("### :green[Clean sheets]")
        TOP_DF = PLAYERS_DF.sort_values('clean_sheets',ascending=False).head(1)
        TOP_DF = TOP_DF[['team','clean_sheets']]
        DATA_EDITOR(TOP_DF)
    with col2:
        st.caption("### :green[Goals conceded]")
        TOP_DF = PLAYERS_DF.sort_values('goals_conceded',ascending=False).head(1)
        TOP_DF = TOP_DF[['team','goals_conceded']]
        DATA_EDITOR(TOP_DF)
    with col3:
        st.caption("### :green[saves]")
        TOP_SV = GET_DF("saves")
        DATA_EDITOR(TOP_SV)
############