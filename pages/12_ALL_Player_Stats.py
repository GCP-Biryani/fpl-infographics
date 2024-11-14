import streamlit as st
import pandas as pd
import plotly.express as px

#
FWD_DF = pd.read_csv("FWD_data.csv")
MID_DF = pd.read_csv("MID_data.csv")
DEF_DF = pd.read_csv("DEF_data.csv")
GKP_DF = pd.read_csv("GKP_data.csv")
DEFENSE_DF = pd.concat([DEF_DF,GKP_DF]) 
ATTACK_DF = pd.concat([FWD_DF,MID_DF,DEF_DF])
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
        """[GCP Biryani](https://github.com/GCP-Biryani)"""
    )
#######
col_gen = ['web_name','position','team','now_cost','selected_by_percent','total_points','minutes','money_value']
GEN_DF = ATTACK_DF[col_gen]
GEN_DF = GEN_DF.sort_values('total_points',ascending=False)
col_gen_column_config={
        "web_name": "Name","now_cost":"Price","selected_by_percent":"Selected%","total_points":"Total Points","money_value":"PPM£"
    }
#
col_perf = ['web_name','position','team','form', 'points_per_game', 'goals_scored','np_goals','assists', 'bonus', 'shots', 'key_passes','penalties_missed']
PERF_DF = ATTACK_DF[col_perf]
PERF_DF = PERF_DF.sort_values('points_per_game',ascending=False)
col_perf_column_config={
        "web_name": "Name","points_per_game":"PPG","goals_scored":"Goals","np_goals":"np Goals","key_passes":"Key Passes","penalties_missed":"Missed Pens"
    }
#
col_exp = ['web_name','position','team','expected_goals', 'np_xg', 'expected_assists', 'expected_goal_involvements']
EXP_DF = ATTACK_DF[col_exp]
EXP_DF = EXP_DF.sort_values('expected_goal_involvements',ascending=False)
col_exp_column_config={
        "web_name": "Name","expected_goals":"xG","np_xg":"np XG","expected_assists":"xA","expected_goal_involvements":"xGI"
    }
#
col_def = ['web_name','position','team','clean_sheets', 'goals_conceded','expected_goals_conceded','own_goals','total_points','penalties_saved']
DEFENSE_DF = DEFENSE_DF[col_def]
DEFENSE_DF = DEFENSE_DF.sort_values('clean_sheets',ascending=False)
col_def_column_config={
        "web_name": "Name","clean_sheets":"CS","goals_conceded":"GC","own_goals":"OG","penalties_saved":"PS","expected_goals_conceded":"xGC","total_points":"Total Points"
    }
#######
tab1,tab2,tab3,tab4= st.tabs(["General","Attack Performance","Expected","Defense Performance"])
with tab1:
    st.dataframe(GEN_DF,column_config=col_gen_column_config,hide_index=True,use_container_width=False,height=1000,width=1000)
with tab2:
    st.dataframe(PERF_DF,column_config=col_perf_column_config,hide_index=True,use_container_width=False,height=1000,width=1000)
with tab3:
    st.dataframe(EXP_DF,column_config=col_exp_column_config,hide_index=True,use_container_width=False,height=1000,width=1000)
with tab4:
    st.dataframe(DEFENSE_DF,column_config=col_def_column_config,hide_index=True,use_container_width=False,height=1000,width=1000)