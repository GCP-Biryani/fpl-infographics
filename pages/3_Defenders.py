import streamlit as st
import pandas as pd
import plotly.express as px
#

CURR_GW = st.session_state.CURR_GW
#
DEF_DF = pd.read_csv("DEF_data.csv")
DEF_DF_history = pd.read_csv("DEF_history.csv")

# page config
st.set_page_config(
    page_title="Defender Stats • FPL Infographics", page_icon=":soccer:",layout="wide"
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
    "##### Defenders"
)
FWD_DF_XGI = DEF_DF.sort_values('expected_goal_involvements',ascending=False).head(25)
FWD_DF_TP = DEF_DF.sort_values('total_points',ascending=False).head(25)
FWD_DF_FORM = DEF_DF.sort_values('form',ascending=False).head(25)
FWD_DF_PPM = DEF_DF.sort_values('money_value',ascending=False).head(25)
FWD_DF_PPG = DEF_DF.sort_values('points_per_game',ascending=False).head(25)
FWD_DF_SHOTS = DEF_DF.sort_values('shots',ascending=False).head(25)
FWD_DF_KP = DEF_DF.sort_values('key_passes',ascending=False).head(25)
# Top Players tabs
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs(["Performance","Total Points", "xGI","Form","Shots","Key passes","Points per Million","Points per Game"])

with tab1:
    fig_FWD_DF_perf = px.scatter(FWD_DF_XGI, x='goal_involvements', y='expected_goal_involvements',text='web_name')
    x_mean = FWD_DF_XGI['goal_involvements'].mean()
    y_mean = FWD_DF_XGI['expected_goal_involvements'].mean()
    fig_FWD_DF_perf.add_hline(y=y_mean,line_dash="dot")
    fig_FWD_DF_perf.add_vline(x=x_mean,line_dash="dot")
    fig_FWD_DF_perf.update_layout(autosize=False,width=1500,height=600)
    st.plotly_chart(fig_FWD_DF_perf, theme="streamlit", use_container_width=False)
with tab2:
    fig_FWD_DF_TP = px.bar(FWD_DF_TP, x='web_name', y='total_points',color='total_points')
    st.plotly_chart(fig_FWD_DF_TP, theme="streamlit", use_container_width=False)
with tab3:
    fig_FWD_DF_XGI = px.bar(FWD_DF_XGI, x='web_name', y='expected_goal_involvements',color='expected_goal_involvements')
    st.plotly_chart(fig_FWD_DF_XGI, theme="streamlit", use_container_width=False)
with tab4:
    fig_FWD_DF_FORM = px.bar(FWD_DF_XGI, x='web_name', y='form',color='form')
    st.plotly_chart(fig_FWD_DF_FORM, theme="streamlit", use_container_width=False)
with tab5:
    fig_FWD_DF_SHOTS = px.bar(FWD_DF_SHOTS, x='web_name', y='shots',color='shots')
    st.plotly_chart(fig_FWD_DF_SHOTS, theme="streamlit", use_container_width=False)
with tab6:
    fig_FWD_DF_KP = px.bar(FWD_DF_KP, x='web_name', y='key_passes',color='key_passes')
    st.plotly_chart(fig_FWD_DF_KP, theme="streamlit", use_container_width=False)
with tab7:
    fig_FWD_DF_VALUE = px.bar(FWD_DF_PPM, x='web_name', y='money_value',color='money_value')
    st.plotly_chart(fig_FWD_DF_VALUE, theme="streamlit", use_container_width=False)
with tab8:
    fig_FWD_DF_PPG = px.bar(FWD_DF_PPG, x='web_name', y='points_per_game',color='points_per_game')
    st.plotly_chart(fig_FWD_DF_PPG, theme="streamlit", use_container_width=False)

############
st.markdown(
    "##### Weekly stats for Top-25 points getters"
)
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Points","xGI","ICT","BPS","Minutes"])
with tab1:
    pivot_data = DEF_DF_history.pivot_table(index='name', columns='round', values='total_points', aggfunc='sum')
    fwd_h_tp = px.imshow(pivot_data, text_auto=True, aspect="auto",color_continuous_scale='Blackbody_r')
    fwd_h_tp.update_layout(autosize=False,width=1500,height=800)
    st.plotly_chart(fwd_h_tp, theme="streamlit", use_container_width=False)
with tab2:
    pivot_data = DEF_DF_history.pivot_table(index='name', columns='round', values='expected_goal_involvements', aggfunc='sum')
    fwd_h_xgi = px.imshow(pivot_data, text_auto=True, aspect="auto",color_continuous_scale='Blackbody_r')
    fwd_h_xgi.update_layout(autosize=False,width=1600,height=800,)
    st.plotly_chart(fwd_h_xgi, theme="streamlit", use_container_width=False)
with tab3:
    fwd_h_ict = px.line(DEF_DF_history, x="round", y="ict_index",color="name",markers=True, title='Weekly ICT')
    fwd_h_ict.update_layout(autosize=False,width=1400,height=800,)
    st.plotly_chart(fwd_h_ict, theme="streamlit", use_container_width=False)
with tab4:
    fwd_h_bps = px.line(DEF_DF_history, x="round", y="bps",color="name",markers=True, title='Weekly BPS')
    fwd_h_bps.update_layout(autosize=False,width=1400,height=800,)
    st.plotly_chart(fwd_h_bps, theme="streamlit", use_container_width=False)
with tab5:
    fwd_h_min = px.line(DEF_DF_history, x="round", y="minutes",color="name",markers=True, title='Weekly Minutes')
    fwd_h_min.update_layout(autosize=False,width=1400,height=800,)
    st.plotly_chart(fwd_h_min, theme="streamlit", use_container_width=False)