import streamlit as st
import pandas as pd
import plotly.express as px
import soccerdata as sd
from charts import *
#
#
# page config
st.set_page_config(
    page_title="Team stats analysis", page_icon=":soccer:",layout="wide"
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
st.markdown(
    "#### Team stats Analysis :chart_with_upwards_trend: - Attack, Defense, Expected vs Actual"
)
# Team dataframes
fbref = sd.FBref(leagues="ENG-Premier League", seasons=2024)
DF_ARS = pd.read_csv('fbref-Arsenal.csv')
DF_AVL = pd.read_csv('fbref-Aston Villa.csv')
DF_BOU = pd.read_csv('fbref-Bournemouth.csv')
DF_BRE = pd.read_csv('fbref-Brentford.csv')
DF_BRI = pd.read_csv('fbref-Brighton.csv')
DF_CHE = pd.read_csv('fbref-Chelsea.csv')
DF_CRY = pd.read_csv('fbref-Crystal Palace.csv')
DF_EVE = pd.read_csv('fbref-Everton.csv')
DF_FUL = pd.read_csv('fbref-Fulham.csv')
DF_IPS = pd.read_csv('fbref-Ipswich Town.csv')
DF_LEI = pd.read_csv('fbref-Leicester City.csv')
DF_LIV = pd.read_csv('fbref-Liverpool.csv')
DF_MNC = pd.read_csv('fbref-Manchester City.csv')
DF_MNU = pd.read_csv('fbref-Manchester Utd.csv')
DF_NEW = pd.read_csv('fbref-Newcastle Utd.csv')
DF_NFO = pd.read_csv('fbref-NFO.csv')
DF_SOU = pd.read_csv('fbref-Southampton.csv')
DF_TOT = pd.read_csv('fbref-Tottenham.csv')
DF_WHU = pd.read_csv('fbref-West Ham.csv')
DF_WOL = pd.read_csv('fbref-Wolves.csv')

# team tabs
tab1,tab2,tab3,tab4,tab5,tab6,tab7,tab8,tab9,tab10,tab11,tab12,tab13,tab14,tab15,tab16,tab17,tab18,tab19,tab20 = st.tabs(["ARS","AVL","BOU", "BRE","BRI","CHE","CRY","EVE","FUL","IPS","LEI","LIV","MNC","MNU","NEW","NFO","SOU","TOT","WHU","WOL"])
with tab1:
    chart_tabs(DF_ARS)
with tab2:
    chart_tabs(DF_AVL)
with tab3:
    chart_tabs(DF_BOU)
with tab4:
    chart_tabs(DF_BRE)
with tab5:
    chart_tabs(DF_BRI)
with tab6:
    chart_tabs(DF_CHE)
with tab7:
    chart_tabs(DF_CRY)
with tab8:
    chart_tabs(DF_EVE)
with tab9:
    chart_tabs(DF_FUL)
with tab10:
    chart_tabs(DF_IPS)
with tab11:
    chart_tabs(DF_LEI)
with tab12:
    chart_tabs(DF_LIV)
with tab13:
    chart_tabs(DF_MNC)
with tab14:
    chart_tabs(DF_MNU)
with tab15:
    chart_tabs(DF_NEW)
with tab16:
    chart_tabs(DF_NFO)
with tab17:
    chart_tabs(DF_SOU)
with tab18:
    chart_tabs(DF_TOT)
with tab19:
    chart_tabs(DF_WHU)
with tab20:
    chart_tabs(DF_WOL)
