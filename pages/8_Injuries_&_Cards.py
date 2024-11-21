import streamlit as st
import pandas as pd
import plotly.express as px
#
PLAYERS_DF = pd.read_csv("players_data.csv")
#
# page config
st.set_page_config(
    page_title="Injury news & Cards • FPL Infographics", page_icon=":soccer:",layout="wide"
)
LOGO = "logo.png"
st.logo(
    LOGO,
    icon_image=LOGO,
    )

# sidebar
with st.sidebar:
    st.title(""":soccer: *Injuries & Cards*""")
    st.caption("Latest injury news & Yellow, red cards table")
############
YELLOW_DF = PLAYERS_DF.sort_values('yellow_cards',ascending=False).head(50)
YELLOW_DF.rename(columns={'web_name': 'Name'}, inplace=True)
RED_DF = PLAYERS_DF[PLAYERS_DF['red_cards'].ge(0)]
RED_DF = RED_DF.sort_values('red_cards',ascending=False).head(25)
RED_DF.rename(columns={'web_name': 'Name'}, inplace=True)

tab1, tab2,tab3= st.tabs(["Injuries :ambulance:","YELLOW Cards:large_yellow_square:","RED Cards:large_red_square:"])
with tab2:
    fig_YC = px.bar(YELLOW_DF, x='Name', y='yellow_cards',color='yellow_cards',color_continuous_scale='Blackbody_r')
    st.plotly_chart(fig_YC, theme="streamlit", use_container_width=False)
with tab3:
    fig_RC = px.bar(RED_DF, x='Name', y='red_cards',color='red_cards',color_continuous_scale='Blackbody_r')
    st.plotly_chart(fig_RC, theme="streamlit", use_container_width=False)
with tab1:
    D_DF = pd.read_csv("players_raw.csv")
    DOUBT_DF = D_DF[D_DF['status'] == 'd']
    DOUBT_DF['news_added'] = DOUBT_DF['news_added'].apply(lambda x: x.split('T')[0])
    DOUBT_DF = DOUBT_DF[['web_name','news','news_added']].sort_values('news_added',ascending=False)
    DOUBT_DF.rename(columns={'web_name': 'Name','news_added':'Updated'}, inplace=True)

    st.dataframe(data=DOUBT_DF,hide_index=True,use_container_width=False,width=1000, height=1500)