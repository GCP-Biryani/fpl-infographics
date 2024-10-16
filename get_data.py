# %%
import requests
import pandas as pd
import numpy as np
from functions import *
pd.options.mode.chained_assignment = None

# %%
players_unused_columns = ['chance_of_playing_next_round','chance_of_playing_this_round','code','cost_change_event','cost_change_event_fall','cost_change_start','cost_change_start_fall','in_dreamteam','special','squad_number','transfers_in','transfers_in_event','transfers_out','transfers_out_event','region','influence_rank_type','creativity_rank_type','threat_rank_type','ict_index_rank_type','corners_and_indirect_freekicks_text','direct_freekicks_text','penalties_text','now_cost_rank','now_cost_rank_type','form_rank','form_rank_type','points_per_game_rank','points_per_game_rank_type','selected_rank','selected_rank_type','dreamteam_count','photo','first_name','second_name']

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
FWD_DF_history = FWD_DF_history.sort_values('total_points',ascending=False).head(20)
FWD_DF_history = FWD_DF_history['id'].to_list()
FWD_DF_history = extract_all_players_data(FWD_DF_history)
FWD_DF_history = pd.DataFrame(FWD_DF_history)
FWD_DF_history.to_csv('FWD_history.csv',index=False)