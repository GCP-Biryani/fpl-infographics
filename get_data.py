# %%
import requests
import pandas as pd
import numpy as np
from scripts.functions import *
pd.options.mode.chained_assignment = None

# %%
#
players_unused_columns = ['chance_of_playing_next_round','chance_of_playing_this_round','code','cost_change_event','cost_change_event_fall','cost_change_start','cost_change_start_fall','in_dreamteam','special','squad_number','transfers_in','transfers_in_event','transfers_out','transfers_out_event','region','influence_rank_type','creativity_rank_type','threat_rank_type','ict_index_rank_type','corners_and_indirect_freekicks_order','corners_and_indirect_freekicks_text','direct_freekicks_order','direct_freekicks_text','penalties_order','penalties_text','now_cost_rank','now_cost_rank_type','form_rank','form_rank_type','points_per_game_rank','points_per_game_rank_type','selected_rank','selected_rank_type','dreamteam_count','news','news_added','photo','first_name','second_name']

# %%
url = 'https://fantasy.premierleague.com/api/bootstrap-static/'
r = requests.get(url)
json1 = r.json()

# %%
# Set data frames
player_types_df = pd.DataFrame(json1['element_types'])
players_df = pd.DataFrame(json1['elements'])
teams_df = pd.DataFrame(json1['teams'])
events_df = pd.DataFrame(json1['events'])
CURR_GW = events_df.loc[events_df['is_current'] == True]['id'].iloc[-1]

# %%
# DROP unavailable & Injured
players_df.drop(players_df[players_df['status'] == 'u'].index, inplace=True)
players_df.drop(players_df[players_df['status'] == 'i'].index, inplace=True)
# players_df = players_df.drop(players_df[players_df['minutes'] == 0].index)
# SAVE
players_df.to_csv('players_raw.csv')

# Drop unused columns
players_df = players_df.drop(columns = players_unused_columns)

# Replace position ID with name
players_df['position'] = players_df.element_type.map(player_types_df.set_index('id').singular_name)

# Replace team ID with name
players_df['team'] = players_df.team.map(teams_df.set_index('id').name)

# Create new stats
players_df['element_type'] = players_df['element_type'].replace([1,2,3,4],['GKP','DEF','MID','FWD'])
players_df['now_cost'] = players_df['now_cost']/10
players_df['goal_involvements'] = players_df['goals_scored'] + players_df['assists']
players_df['money_value'] = players_df['total_points'] / players_df['now_cost']
players_df = players_df.astype({"form": float, "total_points": int, "expected_goal_involvements": float,"money_value":float ,"goal_involvements": float})
players_df['performance'] = players_df['goal_involvements'] - players_df['expected_goal_involvements']
# SAVE
players_df.to_csv('players_data.csv', index=False)
FWD_DF = players_df.loc[players_df['element_type'] == 'FWD']
FWD_DF.to_csv('FWD_data.csv', index=False)
MID_DF = players_df.loc[players_df['element_type'] == 'MID']
MID_DF.to_csv('MID_data.csv', index=False)
DEF_DF = players_df.loc[players_df['element_type'] == 'DEF']
DEF_DF.to_csv('DEF_data.csv', index=False)
GKP_DF = players_df.loc[players_df['element_type'] == 'GKP']
GKP_DF.to_csv('GKP_data.csv', index=False)

# %%
#GKP
GKP_DF_history = players_df.loc[players_df['element_type'] == 'GKP']
GKP_DF_history = GKP_DF_history.sort_values('total_points',ascending=False).head(15)
GKP_DF_history = GKP_DF_history['id'].to_list()
GKP_DF_history = extract_all_players_data(GKP_DF_history)
GKP_DF_history = pd.DataFrame(GKP_DF_history)
GKP_DF_history.to_csv('GKP_history.csv',index=False)

# %%
#DEF
DEF_DF_history = players_df.loc[players_df['element_type'] == 'DEF']
DEF_DF_history = DEF_DF_history.sort_values('total_points',ascending=False).head(25)
DEF_DF_history = DEF_DF_history['id'].to_list()
DEF_DF_history = extract_all_players_data(DEF_DF_history)
DEF_DF_history = pd.DataFrame(DEF_DF_history)
DEF_DF_history.to_csv('DEF_history.csv',index=False)

# %%
#MID
MID_DF_history = players_df.loc[players_df['element_type'] == 'MID']
MID_DF_history = MID_DF_history.sort_values('total_points',ascending=False).head(25)
MID_DF_history = MID_DF_history['id'].to_list()
MID_DF_history = extract_all_players_data(MID_DF_history)
MID_DF_history = pd.DataFrame(MID_DF_history)
MID_DF_history.to_csv('MID_history.csv',index=False)

# %%
#FWD
FWD_DF_history = players_df.loc[players_df['element_type'] == 'FWD']
FWD_DF_history = FWD_DF_history.sort_values('total_points',ascending=False).head(15)
FWD_DF_history = FWD_DF_history['id'].to_list()
FWD_DF_history = extract_all_players_data(FWD_DF_history)
FWD_DF_history = pd.DataFrame(FWD_DF_history)
FWD_DF_history.to_csv('FWD_history.csv',index=False)