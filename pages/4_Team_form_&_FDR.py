import streamlit as st
import pandas as pd
import plotly.express as px
import soccerdata as sd
from charts import *
#
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
    st.title(""":soccer: *Team form & FDR*""")
    st.caption("Team recent form - goals scored, points per game,clean sheets, no of games team scrored in")
#
st.markdown(
    "#### Team FORM & FDR Analysis:bar_chart:"
)

#######################
## FORM & FDR
#######################
tabx,taby = st.tabs(["From analysys", "FDR Analysis"])
with tabx:
    TEAM_FORM_DF = pd.read_csv('team_form.csv', index_col=False)
    options = ["Points Per Game(Last5)", "Goals Per Game(Last5)", "Points Per Game(Season)","Clean Sheets", "GAMES SCORED IN"]
    selection = st.radio("Select an indicator", options,horizontal=True)
    fig = px.bar(TEAM_FORM_DF,x=selection,y='Team',color=selection,color_continuous_scale='plasma_r',text=selection,orientation='h')
    fig.update_layout(autosize=False,width=1500,height=700)
    st.plotly_chart(fig, theme=None)
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