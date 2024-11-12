import streamlit as st
import pandas as pd
import plotly.express as px
import soccerdata as sd
#
#
# page config
st.set_page_config(
    page_title="Team xG vs xAG", page_icon=":soccer:",layout="wide"
)
LOGO = "logo.png"
st.logo(
    LOGO,
    icon_image=LOGO,
    )
# sidebar
with st.sidebar:
    st.markdown(""":soccer: :green[FPL] *Infographics*""")
    st.caption(
        """[GCP Biryani](https://github.com/GCP-Biryani)"""
    )
#
fbref = sd.FBref(leagues="ENG-Premier League", seasons=2024)
DF_ARS = fbref.read_team_match_stats(stat_type="schedule", team="Arsenal")
DF_AVL = fbref.read_team_match_stats(stat_type="schedule", team="Aston Villa")
DF_BOU = fbref.read_team_match_stats(stat_type="schedule", team="Bournemouth")
DF_BRE = fbref.read_team_match_stats(stat_type="schedule", team="Brentford")
DF_BRI = fbref.read_team_match_stats(stat_type="schedule", team="Brighton")
DF_CHE = fbref.read_team_match_stats(stat_type="schedule", team="Chelsea")
DF_CRY = fbref.read_team_match_stats(stat_type="schedule", team="Crystal Palace")
DF_EVE = fbref.read_team_match_stats(stat_type="schedule", team="Everton")
DF_FUL = fbref.read_team_match_stats(stat_type="schedule", team="Fulham")
DF_IPS = fbref.read_team_match_stats(stat_type="schedule", team="Ipswich Town")
DF_LEI = fbref.read_team_match_stats(stat_type="schedule", team="Leicester City")
DF_LIV = fbref.read_team_match_stats(stat_type="schedule", team="Liverpool")
DF_MNC = fbref.read_team_match_stats(stat_type="schedule", team="Manchester City")
DF_MNU = fbref.read_team_match_stats(stat_type="schedule", team="Manchester Utd")
DF_NEW = fbref.read_team_match_stats(stat_type="schedule", team="Newcastle Utd")
DF_NFO = fbref.read_team_match_stats(stat_type="schedule", team="Nott'ham Forest")
DF_SOU = fbref.read_team_match_stats(stat_type="schedule", team="Southampton")
DF_TOT = fbref.read_team_match_stats(stat_type="schedule", team="Tottenham")
DF_WHU = fbref.read_team_match_stats(stat_type="schedule", team="West Ham")
DF_WOL = fbref.read_team_match_stats(stat_type="schedule", team="Wolves")

tab1,tab2,tab3,tab4,tab5,tab6,tab7,tab8,tab9,tab10,tab11,tab12,tab13,tab14,tab15,tab16,tab17,tab18,tab19,tab20 = st.tabs(["ARS","AVL","BOU", "BRE","BRI","CHE","CRY","EVE","FUL","IPS","LEI","LIV","MNC","MNU","NEW","NFO","SOU","TOT","WHU","WOL"])
with tab1:
    st.line_chart(
    DF_ARS,
    x="opponent",
    y=["xG", "xGA"],
    use_container_width=False
)
with tab2:
    st.line_chart(
    DF_AVL,
    x="opponent",
    y=["xG", "xGA"],
    use_container_width=False
)