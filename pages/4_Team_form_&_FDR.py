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
    st.markdown(""":soccer: :green[FPL] *Infographics*""")
    st.caption(
        """[GCP Biryani](https://github.com/GCP-Biryani)"""
    )
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
    option = st.selectbox(
    "Select the metric",
    ("Points Per Game(Last5)", "Goals Per Game(Last5)", "Points Per Game(Season)",'Clean Sheets', 'GAMES SCORED IN'),
    )
    fig = px.bar(TEAM_FORM_DF,x=option,y='Team',color=option,color_continuous_scale='plasma_r',text=option,orientation='h')
    fig.update_layout(autosize=False,width=1500,height=700)
    st.plotly_chart(fig, theme=None)
with taby:
    TEAM_FDR_DF = pd.read_csv('team_fdr.csv', index_col=False)
    fdr_opt = st.selectbox(
    "Select the metric",
    ('Avg FDR(Next 3)','Avg FDR5(Next 5)','Avg FDR(Next 10)','Avg FDR(Remaining Season)')
    )
    fig = px.bar(TEAM_FDR_DF,x=fdr_opt,y='Team',color=fdr_opt,color_continuous_scale='plasma_r',text=fdr_opt,orientation='h')
    fig.update_layout(autosize=False,width=1500,height=700)
    st.plotly_chart(fig, theme=None)