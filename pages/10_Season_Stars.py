import streamlit as st
import pandas as pd

#
#
PLAYERS_DF = pd.read_csv("players_data.csv")
PLAYERS_DF = PLAYERS_DF.rename(columns={'web_name':'Name'})
PLAYERS_DF['goal_involvements'] = PLAYERS_DF['goals_scored'] + PLAYERS_DF['assists']
PLAYERS_DF['money_value'] = PLAYERS_DF['total_points'] / PLAYERS_DF['now_cost']
#
# page config
st.set_page_config(
    page_title="Season Stars • FPL Infographics", page_icon=":soccer:",layout="wide"
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
##########
def GET_DF(STAT):
    TOP_DF = PLAYERS_DF.sort_values(STAT,ascending=False).head(1)
    PHOTO = TOP_DF.photo.to_string(index=False)
    TOP_DF['IMAGE'] = f'https://resources.premierleague.com/premierleague/photos/players/250x250/p{PHOTO}'
    TOP_DF['IMAGE'] = TOP_DF['IMAGE'].str.replace('jpg','png')
    TOP_DF = TOP_DF[['IMAGE','Name',STAT]]
    return TOP_DF
############
def DATA_EDITOR(DF):
    return st.data_editor(DF,column_config={"IMAGE": st.column_config.ImageColumn(label="")},hide_index=True,disabled=True)
############
st.header("Season Stars",divider=True)
#
col1, col2, col3,col4,col5,col6 = st.columns(6)
with col1:
    st.caption("### :green[Goals]")
    TOP_GS = GET_DF("goals_scored")
    DATA_EDITOR(TOP_GS)
with col2:
    st.caption("### :green[Non-penalty Goals]")
    TOP_NGS = GET_DF("np_goals")
    DATA_EDITOR(TOP_NGS)    
with col3:
    st.caption("### :green[Assists]")
    TOP_A = GET_DF("assists")
    DATA_EDITOR(TOP_A)
with col4:
    st.caption("### :green[Goal Involvements]")
    TOP_GI = GET_DF("goal_involvements")
    DATA_EDITOR(TOP_GI)
with col5:
    st.caption("### :green[Shots]")
    TOP_SHOTS = GET_DF("shots")
    DATA_EDITOR(TOP_SHOTS)
with col6:
    st.caption("### :green[Key passes]")
    TOP_KP = GET_DF("key_passes")
    DATA_EDITOR(TOP_KP)
############
#
col1, col2, col3,col4 = st.columns(4)
with col1:
    st.caption("### :green[xG]")
    TOP_XG = GET_DF("expected_goals")
    DATA_EDITOR(TOP_XG)
with col2:
    st.caption("### :green[Non-penalty xG]")
    TOP_NPXG = GET_DF("np_xg")
    DATA_EDITOR(TOP_NPXG)
with col3:
    st.caption("### :green[xA]")
    TOP_XA = GET_DF("expected_assists")
    DATA_EDITOR(TOP_XA)
with col4:
    st.caption("### :green[xGI]")
    TOP_XGI = GET_DF("expected_goal_involvements")
    DATA_EDITOR(TOP_XGI)
############
#
col2, col4,col5 = st.columns(3)
with col2:
    st.caption("### :green[Total Points]")
    TOP_XA = GET_DF("total_points")
    DATA_EDITOR(TOP_XA)
with col4:
    st.caption("### :green[Points per Million]")
    TOP_MV = GET_DF("money_value")
    DATA_EDITOR(TOP_MV)
with col5:
    st.caption("### :green[Points per Game]")
    TOP_PPG = GET_DF("points_per_game")
    DATA_EDITOR(TOP_PPG)
############
#
col1, col2, col3 = st.columns(3)
with col1:
    st.caption("### :green[Clean sheets]")
    TOP_CS = GET_DF("clean_sheets")
    DATA_EDITOR(TOP_CS)
with col2:
    st.caption("### :green[Goals conceded]")
    TOP_GC = GET_DF("goals_conceded")
    DATA_EDITOR(TOP_GC)
with col3:
    st.caption("### :green[Own goals]")
    TOP_OG = GET_DF("own_goals")
    DATA_EDITOR(TOP_OG)
############
#
col1, col2, col3 = st.columns(3)
with col1:
    st.caption("### :green[penalties_missed]")
    TOP_PM = GET_DF("penalties_missed")
    DATA_EDITOR(TOP_PM)
with col2:
    st.caption("### :green[yellow_cards]")
    TOP_YC = GET_DF("yellow_cards")
    DATA_EDITOR(TOP_YC)
with col3:
    st.caption("### :green[red_cards]")
    TOP_RC = GET_DF("red_cards")
    DATA_EDITOR(TOP_RC)
############
#
col1, col2,col3 = st.columns(3)
with col1:
    st.caption("### :green[saves]")
    TOP_SV = GET_DF("saves")
    DATA_EDITOR(TOP_SV)
with col2:
    st.caption("### :green[penalties_saved]")
    TOP_PS = GET_DF("penalties_saved")
    DATA_EDITOR(TOP_PS)