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
#
def xg_xga(df):
    fig = px.area(df, x='opponent', y=['xG','xGA'])
    fig.update_traces(stackgroup = None,fill = 'tozeroy')
    return fig
#
tab1,tab2,tab3,tab4,tab5,tab6,tab7,tab8,tab9,tab10,tab11,tab12,tab13,tab14,tab15,tab16,tab17,tab18,tab19,tab20 = st.tabs(["ARS","AVL","BOU", "BRE","BRI","CHE","CRY","EVE","FUL","IPS","LEI","LIV","MNC","MNU","NEW","NFO","SOU","TOT","WHU","WOL"])
with tab1:
    fig = xg_xga(DF_ARS)
    st.plotly_chart(fig,theme=None)
with tab2:
    fig = xg_xga(DF_AVL)
    st.plotly_chart(fig,theme=None)
with tab3:
    fig = xg_xga(DF_BOU)
    st.plotly_chart(fig,theme=None)
with tab4:
    fig = xg_xga(DF_BRE)
    st.plotly_chart(fig,theme=None)
with tab5:
    fig = xg_xga(DF_BRI)
    st.plotly_chart(fig,theme=None)
with tab6:
    fig = xg_xga(DF_CHE)
    st.plotly_chart(fig,theme=None)
with tab7:
    fig = xg_xga(DF_CRY)
    st.plotly_chart(fig,theme=None)
with tab8:
    fig = xg_xga(DF_EVE)
    st.plotly_chart(fig,theme=None)
with tab9:
    fig = xg_xga(DF_FUL)
    st.plotly_chart(fig,theme=None)
with tab10:
    fig = xg_xga(DF_IPS)
    st.plotly_chart(fig,theme=None)
with tab11:
    fig = xg_xga(DF_LEI)
    st.plotly_chart(fig,theme=None)
with tab12:
    fig = xg_xga(DF_LIV)
    st.plotly_chart(fig,theme=None)
with tab13:
    fig = xg_xga(DF_MNC)
    st.plotly_chart(fig,theme=None)
with tab14:
    fig = xg_xga(DF_MNU)
    st.plotly_chart(fig,theme=None)
with tab15:
    fig = xg_xga(DF_NEW)
    st.plotly_chart(fig,theme=None)
with tab16:
    fig = xg_xga(DF_NFO)
    st.plotly_chart(fig,theme=None)
with tab17:
    fig = xg_xga(DF_SOU)
    st.plotly_chart(fig,theme=None)
with tab18:
    fig = xg_xga(DF_TOT)
    st.plotly_chart(fig,theme=None)
with tab19:
    fig = xg_xga(DF_WHU)
    st.plotly_chart(fig,theme=None)
with tab20:
    fig = xg_xga(DF_WOL)
    st.plotly_chart(fig,theme=None)

st.markdown('''
    * xG (BLUE Line)= Expected Goals
    * XGA (RED Line) = Expected Goals Against'''
)