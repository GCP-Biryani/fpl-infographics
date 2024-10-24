# %%
import requests
import pandas as pd
import numpy as np
from functions import *
import soccerdata as sd
pd.options.mode.chained_assignment = None

# %%
players_epl_unused_columns = ['chance_of_playing_next_round','chance_of_playing_this_round','code','cost_change_event','cost_change_event_fall','cost_change_start','cost_change_start_fall','in_dreamteam','special','squad_number','transfers_in','transfers_in_event','transfers_out','transfers_out_event','region','influence_rank_type','creativity_rank_type','threat_rank_type','ict_index_rank_type','corners_and_indirect_freekicks_text','direct_freekicks_text','penalties_text','now_cost_rank','now_cost_rank_type','form_rank','form_rank_type','points_per_game_rank','points_per_game_rank_type','selected_rank','selected_rank_type','dreamteam_count','first_name','second_name']
players_understat_unused_columns = ['team_id', 'position','matches','minutes','goals','assists','yellow_cards','red_cards']
# %%
url = 'https://fantasy.premierleague.com/api/bootstrap-static/'
r = requests.get(url)
json1 = r.json()

# %%
# Set data frames
player_types_df = pd.DataFrame(json1['element_types'])
players_df_epl = pd.DataFrame(json1['elements'])
teams_df = pd.DataFrame(json1['teams'])
events_df = pd.DataFrame(json1['events'])
CURR_GW = events_df.loc[events_df['is_current'] == True]['id'].iloc[-1]

# %%
##########################
# TEAM form
##########################
fixtures_url = 'https://fantasy.premierleague.com/api/fixtures/'
fixtures_json = requests.get(fixtures_url).json()
all_fixtures_df = pd.json_normalize(fixtures_json)
all_fixtures_df = all_fixtures_df[all_fixtures_df.finished == True]
all_fixtures_df = all_fixtures_df.astype({"team_h_score": int, "team_a_score": int})

id_to_name = teams_df['id'].to_list()
    
appended_data = []
for id in id_to_name:
    fixtures_df = all_fixtures_df[((all_fixtures_df.team_h == id) | (all_fixtures_df.team_a == id))]
    fixtures_df['is_home_team'] = np.where(fixtures_df.team_h == id, True, False)
    fixtures_df['team_goals'] = np.where(fixtures_df.is_home_team == True,fixtures_df.team_h_score , fixtures_df.team_a_score)
    fixtures_df['opp_goals'] = np.where(fixtures_df.is_home_team == False,fixtures_df.team_h_score , fixtures_df.team_a_score)
    fixtures_df['clean_sheets'] = np.where(fixtures_df.opp_goals == 0, 1, 0)
    fixtures_df['did_team_score'] = np.where(fixtures_df.team_goals > 0, 1, 0)
    fixtures_df['points'] = np.where(fixtures_df.team_goals > fixtures_df.opp_goals, 3, np.where(fixtures_df.team_goals == fixtures_df.opp_goals, 1, 0))
    fixtures_df['difficulty'] = np.where(fixtures_df.is_home_team == True,fixtures_df.team_h_difficulty, fixtures_df.team_a_difficulty)
    fixtures_df.sort_values(by=['event'])
    PPG5 = round(fixtures_df.tail(5).points.mean(),2)
    GPG5 = round(fixtures_df.tail(5).team_goals.mean(), 2)
    PPG = round(fixtures_df.points.mean(), 2)
    CS = fixtures_df.clean_sheets.sum()
    SCORED = fixtures_df.did_team_score.sum()

    appended_data.append({'Team': id,'Points Per Game(Last5)':PPG5, 'Goals Per Game(Last5)':GPG5, 'Points Per Game(Season)':PPG,'Clean Sheets':CS, 'GAMES SCORED IN':SCORED})
    
TEAM_FORM_DF = pd.DataFrame(appended_data)
TEAM_FORM_DF['Team'] = TEAM_FORM_DF.Team.map(teams_df.set_index('id').name)
TEAM_FORM_DF.to_csv('team_form.csv', index=False)
#
# %%
##########################
# TEAM FDR
##########################
fixtures_url = 'https://fantasy.premierleague.com/api/fixtures/'
fixtures_json = requests.get(fixtures_url).json()
all_fixtures_df = pd.json_normalize(fixtures_json)

id_to_name = teams_df['id'].to_list()

appended_data = []
for id in id_to_name:
    fixtures_df = all_fixtures_df[((all_fixtures_df.team_h == id) | (all_fixtures_df.team_a == id)) & (all_fixtures_df.finished == False)]
    fixtures_df['is_home_team'] = np.where(fixtures_df.team_h == id, True, False)
    fixtures_df['difficulty'] = np.where(fixtures_df.is_home_team == True,fixtures_df.team_h_difficulty, fixtures_df.team_a_difficulty)
    fixtures_df.sort_values(by=['event'])
    FDR3 = round(fixtures_df.head(3).difficulty.mean(), 2)
    FDR5 = round(fixtures_df.head(5).difficulty.mean(), 2)
    FDR10 = round(fixtures_df.head(10).difficulty.mean(), 2)
    FDR_ALL = round(fixtures_df.difficulty.mean(), 2)
    appended_data.append({'Team': id,'Avg FDR(Next 3)':FDR3, 'Avg FDR5(Next 5)':FDR5, 'Avg FDR(Next 10)':FDR10, 'Avg FDR(Remaining Season)':FDR_ALL})
    
TEAM_FDR_DF = pd.DataFrame(appended_data)
TEAM_FDR_DF['Team'] = TEAM_FDR_DF.Team.map(teams_df.set_index('id').name)
TEAM_FDR_DF.to_csv('team_fdr.csv', index=False)
# %%
##########################
# Add FPL data
##########################
# DROP unavailable & Injured
players_df_epl.drop(players_df_epl[players_df_epl['status'] == 'u'].index, inplace=True)
players_df_epl.drop(players_df_epl[players_df_epl['status'] == 'i'].index, inplace=True)
# players_df_epl = players_df_epl.drop(players_df_epl[players_df_epl['minutes'] == 0].index)
# SAVE
players_df_epl.to_csv('players_raw.csv')
# Drop unused columns
players_df_epl = players_df_epl.drop(columns = players_epl_unused_columns)
# Replace position ID with name
players_df_epl['position'] = players_df_epl.element_type.map(player_types_df.set_index('id').singular_name)
# Replace team ID with name
players_df_epl['team'] = players_df_epl.team.map(teams_df.set_index('id').name)
# Create new stats
players_df_epl['element_type'] = players_df_epl['element_type'].replace([1,2,3,4],['GKP','DEF','MID','FWD'])
players_df_epl['now_cost'] = players_df_epl['now_cost']/10
players_df_epl['goal_involvements'] = players_df_epl['goals_scored'] + players_df_epl['assists']
players_df_epl['money_value'] = players_df_epl['total_points'] / players_df_epl['now_cost']
players_df_epl = players_df_epl.astype({"form": float, "total_points": int, "expected_goal_involvements": float,"money_value":float ,"goal_involvements": float})
players_df_epl['performance'] = players_df_epl['goal_involvements'] - players_df_epl['expected_goal_involvements']
# %%
##########################
# FPL, UNDERSTAT, FBREF ID_MAP
##########################
ID_MAP_DF = pd.read_csv('https://raw.githubusercontent.com/ChrisMusson/FPL-ID-Map/refs/heads/main/Master.csv')
map_unused_columns = ['code','first_name', 'second_name','web_name', '16-17', '17-18',
       '18-19', '19-20', '20-21', '21-22', '22-23', '23-24']
ID_MAP_DF = ID_MAP_DF.drop(columns = map_unused_columns)
ID_MAP_DF = ID_MAP_DF.dropna()
ID_MAP_DF = ID_MAP_DF.sort_values('24-25')
ID_MAP_DF = ID_MAP_DF.rename(columns={'24-25':'FPL_ID','understat':'Understat_ID','fbref':'fbref_id'})
ID_MAP_DF['FPL_ID'] = ID_MAP_DF['FPL_ID'].astype(int)
ID_MAP_DF['Understat_ID'] = ID_MAP_DF['Understat_ID'].astype(int)
ID_MAP_DF['fbref_id'] = ID_MAP_DF['fbref_id'].astype(str)
ID_MAP_DF.to_csv('id_map.csv', index=False)
# %%
##########################
# Add understat IDs
##########################
players_df_understat = pd.read_csv('id_map.csv')
players_merge_df = pd.merge(players_df_epl, players_df_understat, left_on = "id", right_on = "FPL_ID")
# %%
##########################
# Add UNDERSTAT data
##########################
understat = sd.Understat(leagues="ENG-Premier League", seasons="2024/2025")
understat_data_df = understat.read_player_season_stats()
understat_data_df[understat_data_df.columns.dropna()]
understat_data_df=understat_data_df.drop(columns = players_understat_unused_columns)
#
understat_data_df['player_id'] = understat_data_df['player_id'].astype(int)
understat_data_df['xg'] = understat_data_df['xg'].astype(float)
understat_data_df['xa'] = understat_data_df['xa'].astype(float)
understat_data_df['np_xg'] = understat_data_df['np_xg'].astype(float)
understat_data_df['xg_chain'] = understat_data_df['xg_chain'].astype(float)
understat_data_df['xg_buildup'] = understat_data_df['xg_buildup'].astype(float)
understat_data_df['shots'] = understat_data_df['shots'].astype(int)
understat_data_df['key_passes'] = understat_data_df['key_passes'].astype(int)
understat_data_df['np_goals'] = understat_data_df['np_goals'].astype(int)
# understat_data_df.to_csv('understat_data_df.csv', index=False)
# %%
##########################
### Merge FPL and UNDERSTAT data
##########################
players_data_df= pd.merge(players_merge_df, understat_data_df, left_on = "Understat_ID", right_on = "player_id")
players_data_df = players_data_df.round(2)
# SAVE
players_data_df.to_csv('players_data.csv', index=False)
# %%
##########################
# Position DFs
##########################
FWD_DF = players_data_df.loc[players_data_df['element_type'] == 'FWD']
FWD_DF.to_csv('FWD_data.csv', index=False)
MID_DF = players_data_df.loc[players_data_df['element_type'] == 'MID']
MID_DF.to_csv('MID_data.csv', index=False)
DEF_DF = players_data_df.loc[players_data_df['element_type'] == 'DEF']
DEF_DF.to_csv('DEF_data.csv', index=False)
GKP_DF = players_data_df.loc[players_data_df['element_type'] == 'GKP']
GKP_DF.to_csv('GKP_data.csv', index=False)

# %%
##########################
# GKP - Top15
##########################
GKP_DF_history = players_data_df.loc[players_data_df['element_type'] == 'GKP']
GKP_DF_history = GKP_DF_history.sort_values('total_points',ascending=False).head(15)
GKP_DF_history = GKP_DF_history['id'].to_list()
GKP_DF_history = extract_all_players_data(GKP_DF_history)
GKP_DF_history = pd.DataFrame(GKP_DF_history)
GKP_DF_history.to_csv('GKP_history.csv',index=False)

# %%
##########################
# DEF - Top25
##########################
DEF_DF_history = players_data_df.loc[players_data_df['element_type'] == 'DEF']
DEF_DF_history = DEF_DF_history.sort_values('total_points',ascending=False).head(25)
DEF_DF_history = DEF_DF_history['id'].to_list()
DEF_DF_history = extract_all_players_data(DEF_DF_history)
DEF_DF_history = pd.DataFrame(DEF_DF_history)
DEF_DF_history.to_csv('DEF_history.csv',index=False)

# %%
##########################
# MID - Top25
##########################
MID_DF_history = players_data_df.loc[players_data_df['element_type'] == 'MID']
MID_DF_history = MID_DF_history.sort_values('total_points',ascending=False).head(25)
MID_DF_history = MID_DF_history['id'].to_list()
MID_DF_history = extract_all_players_data(MID_DF_history)
MID_DF_history = pd.DataFrame(MID_DF_history)
MID_DF_history.to_csv('MID_history.csv',index=False)

# %%
##########################
# FWD - Top20
##########################
FWD_DF_history = players_data_df.loc[players_data_df['element_type'] == 'FWD']
FWD_DF_history = FWD_DF_history.sort_values('total_points',ascending=False).head(20)
FWD_DF_history = FWD_DF_history['id'].to_list()
FWD_DF_history = extract_all_players_data(FWD_DF_history)
FWD_DF_history = pd.DataFrame(FWD_DF_history)
FWD_DF_history.to_csv('FWD_history.csv',index=False)