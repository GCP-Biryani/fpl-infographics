import pandas as pd
import streamlit as st
import numpy as np
# import mplsoccer as mp
from mplsoccer import Radar, FontManager, grid
import matplotlib.pyplot as plt

def rename_cols(df):
    df.columns = df.columns.map('_'.join)
    df.columns = df.columns.str.replace(' ', '')
    df.reset_index(inplace=True)
    return df
#
def combine_duplicates(df):
    df = df.groupby(['player']).agg('sum')
    return df
#
def get_player_stats(df, player_name, col):
    """Get player values for radar chart from DataFrame."""
    df = df[df['player'] == player_name]
    list = df[col].values.flatten().tolist()
    return list
##
def create_radar_chart(params, low, high, lower_is_better, player1_values, player2_values, player3_values, player1_name, player2_name, player3_name):
    """Create radar chart comparing two players."""
    radar = Radar(params, low, high,
              lower_is_better=lower_is_better,
              # whether to round any of the labels to integers instead of decimal places
              round_int=[False]*len(params),
              num_rings=4,  # the number of concentric circles (excluding center circle)
              # if the ring_width is more than the center_circle_radius then
              # the center circle radius will be wider than the width of the concentric circles
              ring_width=1, center_circle_radius=1)
    # Load fonts
    URL1 = ('https://raw.githubusercontent.com/googlefonts/SourceSerifProGFVersion/main/fonts/'
        'SourceSerifPro-Regular.ttf')
    serif_regular = FontManager(URL1)
    URL2 = ('https://raw.githubusercontent.com/googlefonts/SourceSerifProGFVersion/main/fonts/'
        'SourceSerifPro-ExtraLight.ttf')
    serif_extra_light = FontManager(URL2)
    URL3 = ('https://raw.githubusercontent.com/google/fonts/main/ofl/rubikmonoone/'
        'RubikMonoOne-Regular.ttf')
    rubik_regular = FontManager(URL3)
    URL4 = 'https://raw.githubusercontent.com/googlefonts/roboto/main/src/hinted/Roboto-Thin.ttf'
    robotto_thin = FontManager(URL4)
    URL5 = ('https://raw.githubusercontent.com/google/fonts/main/apache/robotoslab/'
        'RobotoSlab%5Bwght%5D.ttf')
    robotto_bold = FontManager(URL5)
    
    # creating the figure using the grid function from mplsoccer:
    fig, axs = grid(figheight=14, grid_height=0.915, title_height=0.06, endnote_height=0.025,
                title_space=0, endnote_space=0, grid_key='radar', axis=False)
    # plot radar
    radar.setup_axis(ax=axs['radar'])
    rings_inner = radar.draw_circles(ax=axs['radar'], facecolor='#ffb2b2', edgecolor='#fc5f5f')

    radar1, vertices1 = radar.draw_radar_solid(player1_values, ax=axs['radar'],
                                           kwargs={'facecolor': '#aa65b2',
                                                   'alpha': 0.6,
                                                   'edgecolor': '#216352',
                                                   'lw': 3})

    radar2, vertices2 = radar.draw_radar_solid(player2_values, ax=axs['radar'],
                                           kwargs={'facecolor': '#66d8ba',
                                                   'alpha': 0.6,
                                                   'edgecolor': '#216352',
                                                   'lw': 3})

    radar3, vertices3 = radar.draw_radar_solid(player3_values, ax=axs['radar'],
                                           kwargs={'facecolor': '#697cd4',
                                                   'alpha': 0.6,
                                                   'edgecolor': '#222b54',
                                                   'lw': 3})

    axs['radar'].scatter(vertices1[:, 0], vertices1[:, 1],
           c='#aa65b2', edgecolors='#502a54', marker='o', s=150, zorder=2)
    axs['radar'].scatter(vertices2[:, 0], vertices2[:, 1],
           c='#52be80', edgecolors='#216352', marker='o', s=150, zorder=2)
    axs['radar'].scatter(vertices3[:, 0], vertices3[:, 1],
           c='#697cd4', edgecolors='#222b54', marker='o', s=150, zorder=2)

    range_labels = radar.draw_range_labels(ax=axs['radar'], fontsize=25, fontproperties=robotto_thin.prop)
    param_labels = radar.draw_param_labels(ax=axs['radar'], fontsize=25, fontproperties=robotto_thin.prop)
    lines = radar.spoke(ax=axs['radar'], color='#a6a4a1', linestyle='--', zorder=2)
    # adding the endnote and title text (these axes range from 0-1, i.e. 0, 0 is the bottom left)
    # Note we are slightly offsetting the text from the edges by 0.01 (1%, e.g. 0.99)
    title1_text = axs['title'].text(0.01, 0.65, player1_name, fontsize=25, color='#aa65b2', fontproperties=robotto_bold.prop, ha='left', va='center')
    title2_text = axs['title'].text(0.5, 0.65, player2_name, fontsize=25, color='#52be80', fontproperties=robotto_bold.prop, ha='center', va='center')
    title3_text = axs['title'].text(0.99, 0.65, player3_name, fontsize=25, color='#697cd4', fontproperties=robotto_bold.prop, ha='right', va='center')
    
    endnote_text = axs['endnote'].text(0.99, 0.5, '@fpl infographics by Joseph', fontsize=15,
                                   fontproperties=robotto_thin.prop, ha='right', va='center')
    fig.set_facecolor('#BDBDBD')
    st.pyplot(fig)
##
def compare_players_and_create_radar(df, player1, player2, player3, selected_params, param_mapping, lower_is_better):
    """Compare two players and create a radar chart."""
    col = [param_mapping[param] for param in selected_params]
    player1_values = get_player_stats(df, player1, col)
    player2_values = get_player_stats(df, player2, col)
    player3_values = get_player_stats(df, player3, col)
    
    # Define lower and upper limits for each parameter
    predefined_low = [0] * len(selected_params)
    predefined_high = [1] * len(selected_params)

    low = np.minimum(predefined_low,(np.minimum(np.minimum(player1_values, player2_values), player3_values)))
    high = np.maximum(predefined_high,(np.maximum(np.maximum(player1_values, player2_values), player3_values)))
    # Ensure that high is greater than low for all parameters
    for i in range(len(low)):
        if low[i] >= high[i]:
            high[i] = low[i] + 1  # Adjust high to be greater than low
    
    create_radar_chart(selected_params, low, high, lower_is_better, player1_values, player2_values, player3_values, player1, player2, player3)
##
def player_season_compare():
    # User selects the type of comparison
    comparison_type = st.radio("Choose comparison type", ('Outfielder', 'Goalkeeper'))

    if comparison_type == 'Outfielder':
        with st.spinner('Loading outfielder data...'):
            df = pd.read_csv('fbref_players_data.csv')
        
        # Get list of players
        players = df['player'].unique().tolist()
        
        player1 = st.selectbox("Select the first player", players)
        player2 = st.selectbox("Select the second player", players)
        player3 = st.selectbox("Select the third player", players)
        
        param_mapping = {
        # standard
            "Goals": 'Performance_Gls',
            "Assists": 'Performance_Ast',
            "Goals + Assists": 'Performance_G+A',
            "Non-Penalty Goals": 'Performance_G-PK',
            "Penalty Goals": 'Performance_PK',
        # Expected
            "xG": 'Expected_xG',
            "npxG": 'Expected_npxG',
            "xAG": 'Expected_xAG',
            "npxG+xAG": 'Expected_npxG+xAG',
        # per 90s
            "Goals/90": "Per90Minutes_Gls",
            "Assists/90": "Per90Minutes_Ast",
            "Goals+Assists/90": "Per90Minutes_G+A",
            "Non-Penalty Goals/90": "Per90Minutes_G-PK",
            "Non-Penalty Goals+Assists/90":"Per90Minutes_G+A-PK",
            "xG/90": "Per90Minutes_xG",
            "xAG/90": "Per90Minutes_xAG",
            "xG+xAG/90": "Per90Minutes_xG+xAG",
            "npxG/90": "Per90Minutes_npxG",
            "npxG+xAG/90": "Per90Minutes_npxG+xAG",
        # shot and goal
            "Shot-Creating Actions": 'SCA_SCA',
            "Shot-Creating Actions per 90": 'SCA_SCA90',
            "Goal-Creating Actions": 'GCA_GCA',
            "Goal-Creating Actions per 90": 'GCA_GCA90',
        # Shooting
            "Shots": 'Standard_Sh',
            "Shots on Target": 'Standard_SoT',
            "Shots on Target %": 'Standard_SoT%',
            "Shots per goal":'Standard_G/Sh',
            "Shots on Target per goal":'Standard_G/SoT',
            "Shots/90": 'Standard_Sh/90',
            "Shots on Target/90": 'Standard_SoT/90',
            "Free Kick Goals": 'Standard_FK',
            "Penalty Kick Goals": 'Standard_PK',
        # Passing
            "Total Passes Completed": 'Total_Cmp',
            "Total Passes Attempted": 'Total_Att',
            "Total Pass Completion %": 'Total_Cmp%',
            "Key Passes": 'KP_',
            "Passes into Final Third": '1/3_',
            "Passes into Penalty Area": 'PPA_',
            "Crosses into Penalty Area": 'CrsPA_',
        # Possition
            "Touches in Attacking Third": 'Touches_Att3rd',
            "Touches in Attacking Penalty Area": 'Touches_AttPen',
            "Take-Ons Attempted": 'Take-Ons_Att',
        # defense
            "Tackles": 'Tackles_Tkl',
            "Tackles Won": 'Tackles_TklW',
            "Interceptions": 'Int_',
            "Tackles + Interceptions": 'Tkl+Int_',
            "Shots blocked": 'Blocks_Sh',
            "Clearances": 'Clr_',
            "Errors": 'Err_',
        
        }
        
        params = list(param_mapping.keys())
        selected_params = st.multiselect("Select parameters to compare (make sure to choose 3 or more parameters)", params, default=params[:5])
        
        lower_is_better_options = st.multiselect("Select parameters where lower is better", params)
        
        if st.button("Compare Players in Season"):
            compare_players_and_create_radar(
                df, 
                player1, 
                player2,
                player3, 
                selected_params, 
                param_mapping, 
                lower_is_better_options
            )
    elif comparison_type == 'Goalkeeper':
        st.text("Work in progress....")

team_crest = {'Everton': 'https://resources.premierleague.com/premierleague/badges/70/t11.png',
               'Aston Villa':'https://resources.premierleague.com/premierleague/badges/70/t7.png',
               'Brentford':'https://resources.premierleague.com/premierleague/badges/70/t94.png',
               'Crystal Palace':'https://resources.premierleague.com/premierleague/badges/70/t31.png',
               'Manchester Utd':'https://resources.premierleague.com/premierleague/badges/70/t1.png',
               'Fulham':'https://resources.premierleague.com/premierleague/badges/70/t54.png',
               'Ipswich Town':'https://resources.premierleague.com/premierleague/badges/70/t40.png',
               'Leicester City':'https://resources.premierleague.com/premierleague/badges/70/t13.png',
               'Tottenham':'https://resources.premierleague.com/premierleague/badges/70/t6.png',
               'West Ham':'https://resources.premierleague.com/premierleague/badges/70/t21.png',
               'Wolves':'https://resources.premierleague.com/premierleague/badges/70/t39.png',
               'Chelsea':'https://resources.premierleague.com/premierleague/badges/70/t8.png',
               'Brighton':'https://resources.premierleague.com/premierleague/badges/70/t36.png',
               'Bournemouth':'https://resources.premierleague.com/premierleague/badges/70/t91.png',
               'Arsenal':'https://resources.premierleague.com/premierleague/badges/70/t3.png',
               'Liverpool':'https://resources.premierleague.com/premierleague/badges/70/t14.png',
               'Manchester City':'https://resources.premierleague.com/premierleague/badges/70/t43.png',
               'Newcastle Utd':'https://resources.premierleague.com/premierleague/badges/70/t4.png',
               'Southampton':'https://resources.premierleague.com/premierleague/badges/70/t20.png',
               "Nott'ham Forest":'https://resources.premierleague.com/premierleague/badges/70/t17.png',
               }