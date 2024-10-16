import streamlit as st
import pandas as pd
import plotly.express as px
#

CURR_GW = st.session_state.CURR_GW
#
PLAYERS_DF = pd.read_csv("players_data.csv")
#
# page config
st.set_page_config(
    page_title="YELLOW & RED Cards • FPL Infographics", page_icon=":soccer:",layout="wide"
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
        """Latest gameweek data: :blue["""
        + str(CURR_GW)
        + """]  
                [thecloudtechnologist](https://github.com/thecloudtechnologist)"""
    )

############
st.markdown(
    "##### Cards"
)
YELLOW_DF = PLAYERS_DF.sort_values('yellow_cards',ascending=False).head(50)
YELLOW_DF.rename(columns={'web_name': 'Name'}, inplace=True)
RED_DF = PLAYERS_DF[PLAYERS_DF['red_cards'].ge(0)]
RED_DF = RED_DF.sort_values('red_cards',ascending=False).head(25)
RED_DF.rename(columns={'web_name': 'Name'}, inplace=True)

tab1, tab2= st.tabs(["YELLOW Cards","RED Cards"])
with tab1:
    fig_YC = px.bar(YELLOW_DF, x='Name', y='yellow_cards',color='yellow_cards',color_continuous_scale='Blackbody_r')
    st.plotly_chart(fig_YC, theme="streamlit", use_container_width=False)
with tab2:
    fig_RC = px.bar(RED_DF, x='Name', y='red_cards',color='red_cards',color_continuous_scale='Blackbody_r')
    st.plotly_chart(fig_RC, theme="streamlit", use_container_width=False)