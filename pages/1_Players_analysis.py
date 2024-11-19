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
    st.caption("--------------------")
    st.link_button("Personalised transfers list", "https://fplmate.streamlit.app", icon=":material/eye_tracking:")
    st.caption("Get your team performance, mini-league performance and Watch list picks based on expected goal involvements, points per game, Form, next gameweek expected points and Infuence+Creativity+Threat rank ")
   
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
tabF,tabM,tabD,tabG = st.tabs(["Forwards","Midfielders","Defenders","Goal Keepers"])
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