import streamlit as st
import pandas as pd
import requests

#
url = 'https://fantasy.premierleague.com/api/bootstrap-static/'
r = requests.get(url)
json1 = r.json()
events_df = pd.DataFrame(json1['events'])
CURR_GW = events_df.loc[events_df['is_current'] == True]['id'].iloc[-1]
#
st.session_state.CURR_GW = CURR_GW

# page config
st.set_page_config(
    page_title="Home • FPL Infographics", page_icon=":soccer:",layout="wide"
)
LOGO = "logo.png"
st.logo(
    LOGO,
    icon_image=LOGO,
    )

# sidebar
with st.sidebar:
    
    st.title(":soccer: FPL Infographics")
    st.caption(
        """Latest gameweek data: :blue["""
        + str(CURR_GW)
        + """]  
                [thecloudtechnologist](https://github.com/thecloudtechnologist)"""
    )


# landing
st.title(":soccer: :green[FPL] *Infographics*")
st.markdown(
    """**Welcome to FPL Infographics - Your Ultimate Fantasy Premier League analysis graphs!**

FPL Infographics will help you make wise decisions by making use of the analysed stats represented as various graphs
"""
)

# latest gameweek
st.markdown(
    "##### Latest data from Gameweek :blue["
    + str(CURR_GW)
    + """] 
Use our latest data, stats, and models to prepare your team for success in :blue Gameweek """
    + str(CURR_GW + 1)
    + "."
)

# development updates
st.markdown(
"""##### Which graphs/stats are provided?
    
    * Top Players by each position based on:
        * Total points, 
        * xGI
        * GI vs xGI quadrant analysis
        * Form 
        * Points per Million
        * Pointer per game 
        * next GW expected points
    
    * Weekly player (top) stats for each position. 
        * points
        * xG 
        * xGI, 
        * BPS, 
        * ICT 
        * Minutes

    * Set piece info
        * Penalties Order
        * Direct free kicks
        * Corners and indirect free kicks

    * discipline
        * Yellow cards
        * Red cards

    * Injuries/Doubts
        * Doubtful players and News
    """
)