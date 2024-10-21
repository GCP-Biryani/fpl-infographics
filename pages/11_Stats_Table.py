import streamlit as st
import pandas as pd
import plotly.express as px

#
Player_data_DF = pd.read_csv("players_data.csv")
#
# page config
st.set_page_config(
    page_title="Player statistics • FPL Infographics", page_icon=":soccer:",layout="wide"
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
        """[thecloudtechnologist](https://github.com/thecloudtechnologist)"""
    )
drop_cols = ['','']