import streamlit as st
import pandas as pd
import plotly.express as px
from charts import *

#
FWD_DF_history  = pd.read_csv("FWD_history.csv")
MID_DF_history = pd.read_csv("MID_history.csv")
DEF_DF_history = pd.read_csv("DEF_history.csv")
GKP_DF_history = pd.read_csv("GKP_history.csv")
#
# page config
st.set_page_config(
    page_title="Player GW history • FPL Infographics", page_icon=":soccer:",layout="wide"
)
LOGO = "logo.png"
st.logo(
    LOGO,
    icon_image=LOGO,
    )
# sidebar
with st.sidebar:
    st.title(""":soccer: *Player GW Histories*""")
    st.caption("--------------------")
    st.link_button("Personalised transfers list", "https://fplmate.streamlit.app", icon=":material/eye_tracking:")
    st.caption("Get your team performance, mini-league performance and Watch list picks based on expected goal involvements, points per game, Form, next gameweek expected points and Infuence+Creativity+Threat rank ")
   
#
st.markdown(
    "#### Player gameweek history :page_with_curl:"
)
#######
tab1,tab2,tab3,tab4 = st.tabs(["FWD","MID","DEF","GKP"])
with tab1:
    gw_history_tabs(FWD_DF_history)
with tab2:
    gw_history_tabs(MID_DF_history)
with tab3:
    gw_history_tabs(DEF_DF_history)
with tab4:
    tab1, tab2, tab3, tab4 = st.tabs(["Weekly Points","xGC","Saves","Minutes"])
    with tab1:
        fig = gw_history_heatmap(GKP_DF_history,'total_points')
        st.plotly_chart(fig, theme=None, use_container_width=False)
    with tab2:
        fig = gw_history_heatmap(GKP_DF_history,'expected_goals_conceded')
        st.plotly_chart(fig, theme=None, use_container_width=False)
    with tab3:
        fig = gw_history_heatmap(GKP_DF_history,'saves')
        st.plotly_chart(fig, theme=None, use_container_width=False)
    with tab4:
        fig = gw_history_heatmap(GKP_DF_history,'minutes')
        st.plotly_chart(fig, theme=None, use_container_width=False)
