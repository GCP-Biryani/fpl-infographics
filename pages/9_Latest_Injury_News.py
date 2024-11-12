import streamlit as st
import pandas as pd
import plotly.express as px
pd.options.mode.chained_assignment = None

#
PLAYERS_DF = pd.read_csv("players_data.csv")
#
# page config
st.set_page_config(
    page_title="Latest Injury News • FPL Infographics", page_icon=":soccer:",layout="wide"
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
    "##### Doubtful for this Gameweek"
)
D_DF = pd.read_csv("players_raw.csv")
DOUBT_DF = D_DF[D_DF['status'] == 'd']
DOUBT_DF['news_added'] = DOUBT_DF['news_added'].apply(lambda x: x.split('T')[0])
DOUBT_DF = DOUBT_DF[['web_name','news','news_added']].sort_values('news_added',ascending=False)
DOUBT_DF.rename(columns={'web_name': 'Name','news_added':'Updated'}, inplace=True)

st.dataframe(data=DOUBT_DF,hide_index=True,use_container_width=False,width=800, height=1500)