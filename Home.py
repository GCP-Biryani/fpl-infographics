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

FPL Infographics will help you make wise decisions by making use of the analysed stats represented as various graphs and tables
"""
)

# latest gameweek
st.markdown(
    "#### Latest data from Gameweek :blue["
    + str(CURR_GW)
    + """] 
###### Use our latest data, stats, and models to prepare your team for success in :blue Gameweek """
    + str(CURR_GW + 1)
    + "."
)
st.markdown(
    "#### Available Graphs and Analysis"
)

# development updates
st.markdown(
"""
    * Top Players by each position based on :bar_chart:
        * Total points, xGI, form, Points per Million, Pointer per game
        * GI vs xGI quadrant analysis

    * Weekly player (top) stats for each position. :chart_with_upwards_trend:
        * points, xG, xGI, BPS, ICT, Minutes

    * Team stats :soccer:
        * Form (last 5 match data - goals scored, cleansheets, points )
        * FDR (Next 3 ,5 and season averages)
    
    * Set piece info :goal_net:
        * Penalties Order, Direct free kicks, Corners and indirect free kicks

    * discipline :large_yellow_square: :large_red_square:
        * Yellow cards, Red cards

    * Latest Injury News :hospital:
        * Doubtful players and News 
"""
)