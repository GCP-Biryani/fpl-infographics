import streamlit as st
from player_charts import *
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
    st.title(""":soccer: *Player stats analysis*""")
    st.caption("players performance, expected - goals, assists, involvements, shots, key passses, points per game, points per million and more..")
# Player data frames
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
        fig_FWD_DF_perf = px.scatter(FWD_DF_XGC, x='goals_conceded', y='expected_goals_conceded',text='web_name')
        x_mean = FWD_DF_XGC['goals_conceded'].mean()
        y_mean = FWD_DF_XGC['expected_goals_conceded'].mean()
        fig_FWD_DF_perf.add_hline(y=y_mean,line_dash="dot")
        fig_FWD_DF_perf.add_vline(x=x_mean,line_dash="dot")
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