import plotly.express as px
import streamlit as st
import pandas as pd
from charts import *
#
# create perf chart
def player_stat_perf(df):
    DF_XGI = df.sort_values('expected_goal_involvements',ascending=False)
    DF_XGI = DF_XGI[DF_XGI['total_points'] > 0]
    fig = px.scatter(DF_XGI, x='goal_involvements', y='expected_goal_involvements',text='web_name',size="total_points",color="total_points",color_continuous_scale='turbo')
    x_mean = df['goal_involvements'].mean()
    y_mean = df['expected_goal_involvements'].mean()
    fig.add_hline(y=y_mean,line_dash="dot",line_color='Blue')
    fig.add_vline(x=x_mean,line_dash="dot",line_color='Blue')
    fig.update_layout(autosize=False,width=1400,height=750)
    return fig
#Creates tabs for entry_type
# tabF,tabM,tabD,tabZ = st.tabs(["Forwards","Midfielders","Defenders","Goalie"])
def player_stat_tabs(df,chart_key):
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs(["Performance","Total Points", "xGI","Form","Shots","Key passes","Points per Million","Points per Game"])
    with tab1:
        fig = player_stat_perf(df)
        st.plotly_chart(fig, theme=None, use_container_width=False,key=chart_key)
        st.caption('upper-right quadrant better choice')
    with tab2:
        st.caption('Interactive - you can select the price bracket using mouse pointer ')
        fig = get_scatter(df,'total_points')
        st.plotly_chart(fig,theme=None)
    with tab3:
        st.caption('Interactive - you can select the price bracket using mouse pointer ')
        fig = get_scatter(df,'expected_goal_involvements')
        st.plotly_chart(fig,theme=None)
    with tab4:
        st.caption('Interactive - you can select the price bracket using mouse pointer ')
        fig = get_scatter(df,'form')
        st.plotly_chart(fig,theme=None)
    with tab5:
        st.caption('Interactive - you can select the price bracket using mouse pointer ')
        fig = get_scatter(df,'shots')
        st.plotly_chart(fig,theme=None)
    with tab6:
        st.caption('Interactive - you can select the price bracket using mouse pointer ')
        fig = get_scatter(df,'key_passes')
        st.plotly_chart(fig,theme=None)
    with tab7:
        st.caption('Interactive - you can select the price bracket using mouse pointer ')
        fig = get_scatter(df,'money_value')
        st.plotly_chart(fig,theme=None)
    with tab8:
        st.caption('Interactive - you can select the price bracket using mouse pointer ')
        fig = get_scatter(df,'points_per_game')
        st.plotly_chart(fig,theme=None)