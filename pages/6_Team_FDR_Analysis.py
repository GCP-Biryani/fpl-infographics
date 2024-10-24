import streamlit as st
import pandas as pd
import plotly.express as px
#
#
TEAM_FORM_DF = pd.read_csv('team_form.csv', index_col=False)
TEAM_FDR_DF = pd.read_csv('team_fdr.csv', index_col=False)
#
st.set_page_config(
    page_title="Team FDR Analysis • FPL Infographics", page_icon=":toolbox:",layout="wide"
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

############
st.markdown(
    "##### Team FDR Analysis"
)
st.dataframe(data=TEAM_FDR_DF,hide_index=True,use_container_width=False,width=1200, height=800)