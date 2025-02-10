import plotly.express as px
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
####################
# Team charts
####################
def get_scatter(df,metric):
    fig = px.scatter(df, x="now_cost", y=metric,
	         size="total_points", color="total_points",color_continuous_scale='turbo',text='web_name')
    fig.update_layout(autosize=False,width=1400,height=600)
    return fig
# Retun area chart for team stats
def xg_xga(df):
    # fig = px.area(df, x='opponent', y=['xG','xGA'])
    # fig.update_traces(stackgroup = 'one')
    # return fig
    data = [go.Bar(x=df['fixture'], y=df['xG'], name='xG', text=df['xG']),
             go.Bar(x=df['fixture'], y=df['xGA'], name='xGA', width=0.5, text=df['xGA'])]
    layout = go.Layout(barmode='overlay',autosize=True)
    return dict(data = data, layout = layout)
# Retun bar chart for team Attack
def xg_goals(df):
    fig = px.bar(df, x='fixture', y=['xG','GF'],barmode='group',text_auto=True)
    return fig
# Retun bar chart for team defense
def xga_goalsa(df):
    fig = px.bar(df, x='fixture', y=['xGA','GA'],barmode='group',text_auto=True)
    return fig
# Retun 3 tabs with team stat charts
def chart_tabs(df):
    taba,tabb,tabc = st.tabs(["Overview","Attack","Defense"])
    with taba:
        fig = xg_xga(df)
        st.plotly_chart(fig,theme=None)
        st.markdown('''
            * xG (BLUE Line)= Expected Goals
            * XGA (RED Line) = Expected Goals Against'''
        )
    with tabb:
        fig = xg_goals(df)
        st.plotly_chart(fig,theme=None)
        st.markdown('''
            * xG (BLUE Bar)= Expected Goals
            * GF (RED Bar) = Actual Goals scored'''
        )
    with tabc:
        fig = xga_goalsa(df)
        st.plotly_chart(fig,theme=None)
        st.markdown('''
            * xGA (BLUE Bar)= expected goals conceded
            * GA (RED Bar) = Actual goals conceded'''
        )
###########################
# Player history Charts
###########################
def gw_history_heatmap(df, metric):
    pivot_data = df.pivot_table(index='name', columns='round', values=metric, aggfunc='sum')
    fig = px.imshow(pivot_data, text_auto=True, aspect="auto",color_continuous_scale='Blackbody_r')
    fig.update_layout(autosize=False,width=1500,height=800)
    # st.plotly_chart(fig, theme=None, use_container_width=False)
    return fig
##
def gw_history_tabs(df):
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Points","xGI","ICT","BPS","Minutes"])
    with tab1:
        fig = gw_history_heatmap(df,'total_points')
        st.plotly_chart(fig, theme=None, use_container_width=False)
    with tab2:
        fig = gw_history_heatmap(df,'expected_goal_involvements')
        st.plotly_chart(fig, theme=None, use_container_width=False)
    with tab3:
        fig = gw_history_heatmap(df,'ict_index')
        st.plotly_chart(fig, theme=None, use_container_width=False)
    with tab4:
        fig = gw_history_heatmap(df,'bps')
        st.plotly_chart(fig, theme=None, use_container_width=False)
    with tab5:
        fig = gw_history_heatmap(df,'minutes')
        st.plotly_chart(fig, theme=None, use_container_width=False)
####################
### Player Charts
####################
# create perf chart
def player_stat_perf(df):
    price = st.slider("Select the max price",3.8,15.5,15.5,step=0.1,key=df.size)
    df = df[df['now_cost'] <= price]
    DF = df.sort_values('expected_goal_involvements',ascending=False)
    DF = DF[DF['total_points'] > 0]
    fig = px.scatter(DF, x='goal_involvements', y='expected_goal_involvements',text='web_name',size="total_points",color="total_points",color_continuous_scale='turbo')
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
###########################
### Mini-league plots
###########################
def plot_total_points(df):
    fig = px.bar(
        df, x="Team_Name", y="Season_Points",color="Season_Points",color_continuous_scale='Rainbow', title="Total Points",text_auto=True
    )
    fig.update_xaxes(title_text="Team name")
    fig.update_yaxes(title_text="Total season points")
    fig.update_layout(xaxis={'categoryorder':'total descending'})
    fig.update_layout(autosize=False,width=1200,height=600,)
    return fig

def plot_GW_points(df):
    fig = px.bar(
        df, x="Team_Name", y="GW_Points",color="GW_Points",color_continuous_scale='Rainbow', title="GW Points",text_auto=True
    )
    fig.update_xaxes(title_text="Team name")
    fig.update_yaxes(title_text="GW points")
    fig.update_layout(xaxis={'categoryorder':'total descending'})
    fig.update_layout(autosize=False,width=1200,height=600,)
    return fig

def plot_total_bench_points(df):
    fig = px.bar(
        df, x="Team_Name", y="season_bench_points",color="season_bench_points",color_continuous_scale='Rainbow', title="Season points on benc",text_auto=True
    )
    fig.update_xaxes(title_text="Team name")
    fig.update_yaxes(title_text="Season points on bench")
    fig.update_layout(xaxis={'categoryorder':'total descending'})
    fig.update_layout(autosize=False,width=1200,height=600,)
    return fig

def plot_gw_bench_points(df):
    fig = px.bar(
        df, x="Team_Name", y="GW_bench_points",color="GW_bench_points",color_continuous_scale='Rainbow', title="Gameweek points left on bench",text_auto=True
    )
    fig.update_xaxes(title_text="Team name")
    fig.update_yaxes(title_text="Gameweek points on bench")
    fig.update_layout(xaxis={'categoryorder':'total descending'})
    fig.update_layout(autosize=False,width=1200,height=600,)
    return fig

def plot_total_vs_bench_points(df):
    # Create a new column that is the sum of total_points and bench_points
    df["total_and_bench_points"] = df["Season_Points"] + df["season_bench_points"]
    # Sort DataFrame by total_and_bench_points from greatest to least
    df = df.sort_values("total_and_bench_points", ascending=False)
    fig = px.bar(
        df,
        x="Team_Name",
        y=["Season_Points", "season_bench_points"],
        title="Total Points vs Points Left on Bench",
        text_auto=True,
    )
    fig.update_xaxes(title_text="Team Name")
    fig.update_yaxes(title_text="Points")
    fig.update_layout(xaxis={'categoryorder':'total descending'})
    fig.update_layout(autosize=False,width=1200,height=600,)
    return fig

def plot_team_vs_bench_value(df):
    # Create a new column that is the sum of total_points and bench_points
    df["team_and_bench_value"] = df["Team_Value"] + df["Bank"]
    # Sort DataFrame by total_and_bench_points from greatest to least
    df = df.sort_values("team_and_bench_value", ascending=False)
    fig = px.bar(
        df,
        x="Team_Name",
        y=["Team_Value", "Bank"],
        title="Team value vs bench value",
        text_auto=True,
    )
    fig.update_xaxes(title_text="Team Name")
    fig.update_yaxes(title_text="team_and_bench_value")
    fig.update_layout(xaxis={'categoryorder':'total descending'})
    fig.update_layout(autosize=False,width=1200,height=600,)
    return fig

def plot_gw_team_xgi(df):
    fig = px.bar(
        df, x="Team_Name", y="team_XGI",color="team_XGI",color_continuous_scale='Rainbow', title="Gameweek team XGI",text_auto=True
    )
    fig.update_xaxes(title_text="Team name")
    fig.update_yaxes(title_text="expected goal involvements")
    fig.update_layout(xaxis={'categoryorder':'total descending'})
    fig.update_layout(autosize=False,width=1200,height=600,)
    return fig

def plot_gw_team_vs_captain(df):
    fig = px.bar(
        df,
        x="Team_Name",
        y=["cap_vs_team", "GW_Captain_points"],
        title="Team vs Captain points",
        text_auto=True,
)
    fig.update_xaxes(title_text="Team Name")
    fig.update_yaxes(title_text="team_and_captain_points")
    fig.update_layout(xaxis={'categoryorder':'total descending'})
    fig.update_layout(autosize=False,width=1200,height=600,)
    return fig

def plot_gw_nGW_xp(df):
    fig = px.bar(
        df,
        x="Team_Name",
        y="nxp",
        title="Next GW XP based on same captain choice",
        color="nxp",
        color_continuous_scale='Rainbow',
        text_auto=True,
    )
    fig.update_xaxes(title_text="Team Name")
    fig.update_yaxes(title_text="Next GW expected points")
    fig.update_layout(xaxis={'categoryorder':'total descending'})
    fig.update_layout(autosize=False,width=1200,height=600,)
    return fig

def plot_gw_captain(df):
    fig = px.pie(df, values='count', names='GW_Captain', title='Gameweek captain choice',labels='GW_Captain')
    fig.update_traces(textposition='inside', textinfo='percent+value')
    fig.update_layout(autosize=False,width=1200,height=600,)
    return fig