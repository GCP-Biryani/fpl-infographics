import plotly.express as px
import streamlit as st
# Gets scatter plot with Xaxis as cost and total points as bubbles 
def get_scatter(df,metric):
    fig = px.scatter(df, x="now_cost", y=metric,
	         size="total_points", color="total_points",color_continuous_scale='turbo',text='web_name')
    fig.update_layout(autosize=False,width=1400,height=600)
    return fig
##
# Retun area chart for team stats
def xg_xga(df):
    fig = px.area(df, x='opponent', y=['xG','xGA'])
    fig.update_traces(stackgroup = None,fill = 'tozeroy')
    return fig
# Retun bar chart for team Attack
def xg_goals(df):
    fig = px.bar(df, x='opponent', y=['xG','GF'],barmode='group')
    return fig
# Retun bar chart for team defense
def xga_goalsa(df):
    fig = px.bar(df, x='opponent', y=['xGA','GA'],barmode='group')
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
##############
# Return heatmap
def gw_history_heatmap(df, metric):
    pivot_data = df.pivot_table(index='name', columns='round', values=metric, aggfunc='sum')
    fig = px.imshow(pivot_data, text_auto=True, aspect="auto",color_continuous_scale='Blackbody_r')
    fig.update_layout(autosize=False,width=1500,height=800)
    # st.plotly_chart(fig, theme=None, use_container_width=False)
    return fig
# Retuns tabs with GW history 
def gw_history_tabs(df):
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Points","xGI","ICT","BPS","Minutes"])
    with tab1:
        fig = gw_history_heatmap(df,'total_points')
        st.plotly_chart(fig, theme=None, use_container_width=False)
        # pivot_data = df.pivot_table(index='name', columns='round', values=metric, aggfunc='sum')
        # fwd_h_tp = px.imshow(pivot_data, text_auto=True, aspect="auto",color_continuous_scale='Blackbody_r')
        # fwd_h_tp.update_layout(autosize=False,width=1500,height=800)
        # st.plotly_chart(fwd_h_tp, theme=None, use_container_width=False)
    with tab2:
        fig = gw_history_heatmap(df,'expected_goal_involvements')
        st.plotly_chart(fig, theme=None, use_container_width=False)
        
        # pivot_data = df.pivot_table(index='name', columns='round', values=metric, aggfunc='sum')
        # fwd_h_xgi = px.imshow(pivot_data, text_auto=True, aspect="auto",color_continuous_scale='Blackbody_r')
        # fwd_h_xgi.update_layout(autosize=False,width=1600,height=800,)
        # st.plotly_chart(fwd_h_xgi, theme=None, use_container_width=False)
    with tab3:
        fig = gw_history_heatmap(df,'ict_index')
        st.plotly_chart(fig, theme=None, use_container_width=False)
        
        # fwd_h_ict = px.line(df, x="round", y=metric,color="name",markers=True, title='Weekly ICT')
        # fwd_h_ict.update_layout(autosize=False,width=1400,height=800,)
        # st.plotly_chart(fwd_h_ict, theme=None, use_container_width=False)
    with tab4:
        fig = gw_history_heatmap(df,'bps')
        st.plotly_chart(fig, theme=None, use_container_width=False)
        
        # fwd_h_bps = px.line(df, x="round", y=metric,color="name",markers=True, title='Weekly BPS')
        # fwd_h_bps.update_layout(autosize=False,width=1400,height=800,)
        # st.plotly_chart(fwd_h_bps, theme=None, use_container_width=False)
    with tab5:
        fig = gw_history_heatmap(df,'minutes')
        st.plotly_chart(fig, theme=None, use_container_width=False)
        
        # fwd_h_min = px.line(df, x="round", y=metric,color="name",markers=True, title='Weekly Minutes')
        # fwd_h_min.update_layout(autosize=False,width=1400,height=800,)
        # st.plotly_chart(fwd_h_min, theme=None, use_container_width=False)