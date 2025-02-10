# %%
import requests
import pandas as pd
import numpy as np
from functools import reduce
from functions import *
import soccerdata as sd
from fbref_functions import *
pd.options.mode.chained_assignment = None
# %%
players_epl_unused_columns = ['chance_of_playing_next_round','chance_of_playing_this_round','code','cost_change_event','cost_change_event_fall','cost_change_start','cost_change_start_fall','in_dreamteam','special','squad_number','transfers_in','transfers_in_event','transfers_out','transfers_out_event','region','influence_rank_type','creativity_rank_type','threat_rank_type','ict_index_rank_type','corners_and_indirect_freekicks_text','direct_freekicks_text','penalties_text','now_cost_rank','now_cost_rank_type','form_rank','form_rank_type','points_per_game_rank','points_per_game_rank_type','selected_rank','selected_rank_type','dreamteam_count','first_name','second_name']
players_understat_unused_columns = ['team_id', 'position','matches','minutes','goals','assists','yellow_cards','red_cards']
# %%
##########################
# Bootstrap data
##########################
url = 'https://fantasy.premierleague.com/api/bootstrap-static/'
r = requests.get(url)
json1 = r.json()
#
# %%
##########################
# Fixtures data
##########################
fixtures_url = 'https://fantasy.premierleague.com/api/fixtures/'
fixtures_json = requests.get(fixtures_url).json()
#
# %%
##########################
# Pandas Dataframes
##########################
all_fixtures_df = pd.json_normalize(fixtures_json)
player_types_df = pd.DataFrame(json1['element_types'])
players_df_epl = pd.DataFrame(json1['elements'])
teams_df = pd.DataFrame(json1['teams'])
events_df = pd.DataFrame(json1['events'])
#
# %%
# Save events to get the current gameweek without session
events_df.to_csv('events.csv', index=False)
CURR_GW = events_df.loc[events_df['is_current'] == True]['id'].iloc[-1]
# %%
##########################
# TEAM form
##########################
all_fixtures_form_df = all_fixtures_df[all_fixtures_df.finished == True]
all_fixtures_form_df = all_fixtures_form_df.astype({"team_h_score": int, "team_a_score": int})

id_to_name = teams_df['id'].to_list()
    
appended_data = []
for id in id_to_name:
    fixtures_form_df = all_fixtures_form_df[((all_fixtures_form_df.team_h == id) | (all_fixtures_form_df.team_a == id))]
    fixtures_form_df['is_home_team'] = np.where(fixtures_form_df.team_h == id, True, False)
    fixtures_form_df['team_goals'] = np.where(fixtures_form_df.is_home_team == True,fixtures_form_df.team_h_score , fixtures_form_df.team_a_score)
    fixtures_form_df['opp_goals'] = np.where(fixtures_form_df.is_home_team == False,fixtures_form_df.team_h_score , fixtures_form_df.team_a_score)
    fixtures_form_df['clean_sheets'] = np.where(fixtures_form_df.opp_goals == 0, 1, 0)
    fixtures_form_df['did_team_score'] = np.where(fixtures_form_df.team_goals > 0, 1, 0)
    fixtures_form_df['points'] = np.where(fixtures_form_df.team_goals > fixtures_form_df.opp_goals, 3, np.where(fixtures_form_df.team_goals == fixtures_form_df.opp_goals, 1, 0))
    fixtures_form_df['difficulty'] = np.where(fixtures_form_df.is_home_team == True,fixtures_form_df.team_h_difficulty, fixtures_form_df.team_a_difficulty)
    fixtures_form_df.sort_values(by=['event'])
    PPG5 = round(fixtures_form_df.tail(5).points.mean(),2)
    GPG5 = round(fixtures_form_df.tail(5).team_goals.mean(), 2)
    PPG = round(fixtures_form_df.points.mean(), 2)
    CS = fixtures_form_df.clean_sheets.sum()
    SCORED = fixtures_form_df.did_team_score.sum()

    appended_data.append({'Team': id,'Points Per Game(Last5)':PPG5, 'Goals Per Game(Last5)':GPG5, 'Points Per Game(Season)':PPG,'Clean Sheets':CS, 'GAMES SCORED IN':SCORED})
    
TEAM_FORM_DF = pd.DataFrame(appended_data)
TEAM_FORM_DF['Team'] = TEAM_FORM_DF.Team.map(teams_df.set_index('id').name)
TEAM_FORM_DF.to_csv('team_form.csv', index=False)
#
# %%
##########################
# TEAM FDR
##########################
# fixtures_url = 'https://fantasy.premierleague.com/api/fixtures/'
# fixtures_json = requests.get(fixtures_url).json()
# all_fixtures_df = pd.json_normalize(fixtures_json)
id_to_name = teams_df['id'].to_list()

appended_data = []
for id in id_to_name:
    fixtures_fdr_df = all_fixtures_df[((all_fixtures_df.team_h == id) | (all_fixtures_df.team_a == id)) & (all_fixtures_df.finished == False)]
    fixtures_fdr_df['is_home_team'] = np.where(fixtures_fdr_df.team_h == id, True, False)
    fixtures_fdr_df['difficulty'] = np.where(fixtures_fdr_df.is_home_team == True,fixtures_fdr_df.team_h_difficulty, fixtures_fdr_df.team_a_difficulty)
    fixtures_fdr_df.sort_values(by=['event'])
    FDR3 = round(fixtures_fdr_df.head(3).difficulty.mean(), 2)
    FDR5 = round(fixtures_fdr_df.head(5).difficulty.mean(), 2)
    FDR10 = round(fixtures_fdr_df.head(10).difficulty.mean(), 2)
    FDR_ALL = round(fixtures_fdr_df.difficulty.mean(), 2)
    appended_data.append({'Team': id,'Avg FDR(Next 3)':FDR3, 'Avg FDR5(Next 5)':FDR5, 'Avg FDR(Next 10)':FDR10, 'Avg FDR(Remaining Season)':FDR_ALL})
    
TEAM_FDR_DF = pd.DataFrame(appended_data)
TEAM_FDR_DF['Team'] = TEAM_FDR_DF.Team.map(teams_df.set_index('id').name)
TEAM_FDR_DF.to_csv('team_fdr.csv', index=False)
#
# %%
##########################
# Fixtures
##########################
fixtures_df = all_fixtures_df
fixtures_unused_columns = ['id', 'code', 'finished', 'finished_provisional', 'minutes', 'provisional_start_time', 'started', 'stats', 'pulse_id']
fixtures_df.drop(fixtures_unused_columns, axis=1, inplace=True)
fixtures_df.rename(columns={'event': 'Gameweek'}, inplace=True)
# fixtures_df.head()

# format kick off times
fixtures_df = fixtures_df[~fixtures_df['kickoff_time'].isnull()]
fixtures_df['kickoff_date'] = fixtures_df['kickoff_time'].apply(lambda x: x.split('T')[0])
fixtures_df['kickoff_time'] = fixtures_df['kickoff_time'].apply(lambda x: x.split('T')[1].replace('Z', ''))
fixtures_df = fixtures_df[['Gameweek', 'kickoff_date', 'kickoff_time', 'team_a', 'team_a_score', 'team_h', 'team_h_score', 'team_h_difficulty', 'team_a_difficulty']]

# set team names instead of IDs
fixtures_df['team_a'] = fixtures_df['team_a'].map(teams_df.set_index('id').name)
fixtures_df['team_h'] = fixtures_df['team_h'].map(teams_df.set_index('id').name)
fixtures_df.to_csv('fixtures.csv',index=False)
#
#
def fixtures_by_team(fixtures, team, gameweek):
    away = fixtures.loc[fixtures['team_a'] == team]
    away.drop(['team_h_difficulty'], axis=1, inplace=True)
    away.rename(columns={'team_a': 'selected_team', 'team_h': 'opponent', 'team_a_difficulty': 'FDR', 'team_a_score': 'selected_team_score', 'team_h_score': 'opponent_score'}, inplace=True)
    away['h_or_a'] = 'Away'
    home = fixtures.loc[fixtures['team_h'] == team]
    home.drop(['team_a_difficulty'], axis=1, inplace=True)
    home.rename(columns={'team_h': 'selected_team', 'team_a': 'opponent', 'team_h_difficulty': 'FDR', 'team_h_score': 'selected_team_score',  'team_a_score': 'opponent_score'}, inplace=True)
    home['h_or_a'] = 'Home'
    combined = pd.concat([away, home])
    return combined.loc[combined['Gameweek'] <= gameweek].sort_values(by='Gameweek')

# %%
##########################
# Add FPL data
##########################
# DROP unavailable & Injured & 0 min players
# players_df_epl.drop(players_df_epl[players_df_epl['status'] == 'u'].index, inplace=True)
# players_df_epl.drop(players_df_epl[players_df_epl['status'] == 'i'].index, inplace=True)
players_df_epl.drop(players_df_epl[players_df_epl['minutes'] == 0].index, inplace=True)
# SAVE
players_df_epl.to_csv('players_raw.csv')
# Drop unused columns
players_df_epl = players_df_epl.drop(columns = players_epl_unused_columns)
# Replace position ID with name
players_df_epl['position'] = players_df_epl.element_type.map(player_types_df.set_index('id').singular_name)
# Replace team ID with name
players_df_epl['team'] = players_df_epl.team.map(teams_df.set_index('id').name)
# Add photos
players_df_epl['photo'] = 'https://resources.premierleague.com/premierleague/photos/players/250x250/p' + players_df_epl['photo'].astype(str)
players_df_epl['photo'] = players_df_epl['photo'].str.replace('jpg','png')
# Create new stats
players_df_epl['element_type'] = players_df_epl['element_type'].replace([1,2,3,4],['GKP','DEF','MID','FWD'])
players_df_epl['now_cost'] = players_df_epl['now_cost']/10
players_df_epl['goal_involvements'] = players_df_epl['goals_scored'] + players_df_epl['assists']
players_df_epl['money_value'] = players_df_epl['total_points'] / players_df_epl['now_cost']
players_df_epl = players_df_epl.astype({"form": float, "total_points": int, "expected_goal_involvements": float,"money_value":float ,"goal_involvements": float})
players_df_epl['performance'] = players_df_epl['goal_involvements'] - players_df_epl['expected_goal_involvements']
# Add fixture details
fixtures_going_forward = fixtures_df.loc[fixtures_df['Gameweek'] > CURR_GW]
#
players_df_epl['next_match'] = players_df_epl['team'].apply(lambda x: list(fixtures_by_team(fixtures_df, x, CURR_GW+1)[['opponent', 'h_or_a']].iloc[-1]))
#
players_df_epl['next_3_FDRs'] = players_df_epl['team'].apply(lambda x: list(fixtures_by_team(fixtures_going_forward, x, CURR_GW+3)['FDR']))
players_df_epl['next_3_avg_FDRs'] = players_df_epl['next_3_FDRs'].apply(lambda x: np.round(np.mean(x), 2))
players_df_epl['next_3'] = players_df_epl['team'].apply(lambda x: list(fixtures_by_team(fixtures_going_forward, x, CURR_GW+3)['opponent']))
#
players_df_epl['next_5_FDRs'] = players_df_epl['team'].apply(lambda x: list(fixtures_by_team(fixtures_going_forward, x, CURR_GW+5)['FDR']))
players_df_epl['next_5_avg_FDRs'] = players_df_epl['next_5_FDRs'].apply(lambda x: np.round(np.mean(x), 2))
players_df_epl['next_5'] = players_df_epl['team'].apply(lambda x: list(fixtures_by_team(fixtures_going_forward, x, CURR_GW+5)['opponent']))
#
players_df_epl = players_df_epl.astype({"next_3": str, "next_5": str, "next_3_avg_FDRs": float, "next_5_avg_FDRs": float})
#

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

# %%
##########################
# FBref team data
##########################
fbref = sd.FBref(leagues="ENG-Premier League", seasons=2425, no_cache=True, no_store=True)
teams = ["Arsenal","Aston Villa","Bournemouth","Brentford","Brighton","Chelsea","Crystal Palace","Everton","Fulham","Ipswich Town","Leicester City","Liverpool","Manchester City","Manchester Utd","Newcastle Utd","Southampton","Tottenham","West Ham","Wolves"]
for team in teams:
    DF = fbref.read_team_match_stats(stat_type="schedule", team=team)
    DF = DF[~DF["result"].isna()]
    DF['fixture'] = DF['opponent'] + "[" + DF['venue']  + "]"
    DF.to_csv("fbref-"+team+".csv")
#
#"Nott'ham Forest"
DF_NFO = fbref.read_team_match_stats(stat_type="schedule", team="Nott'ham Forest")
DF_NFO = DF_NFO[~DF_NFO["result"].isna()]
DF_NFO['fixture'] = DF_NFO['opponent'] + "[" + DF_NFO['venue']  + "]"
DF_NFO.to_csv('fbref-NFO.csv')
# %%
##########################
# FBref player data
##########################
standard_stats_columns = ['player','Performance_Gls','Performance_Ast','Performance_G+A','Performance_G-PK','Performance_PK','Expected_xG','Expected_npxG','Expected_xAG','Expected_npxG+xAG','Per90Minutes_Gls','Per90Minutes_Ast','Per90Minutes_G+A','Per90Minutes_G-PK', 'Per90Minutes_G+A-PK', 'Per90Minutes_xG','Per90Minutes_xAG', 'Per90Minutes_xG+xAG', 'Per90Minutes_npxG','Per90Minutes_npxG+xAG']
shooting_stats_columns = ['player','Standard_Sh','Standard_SoT','Standard_SoT%','Standard_Sh/90','Standard_SoT/90','Standard_G/Sh','Standard_G/SoT',]
goalshot_stats_columns = ['player','SCA_SCA','SCA_SCA90','GCA_GCA','GCA_GCA90']
passing_stats_columns = ['player','Total_Cmp','Total_Att','Total_Cmp%','KP_','1/3_','PPA_','CrsPA_',]
possition_stats_columns = ['player','Touches_Att3rd','Touches_AttPen','Take-Ons_Att','Take-Ons_Succ',]
defense_stats_columns = ['player','Tackles_Tkl','Tackles_TklW','Int_','Tkl+Int_','Blocks_Sh','Clr_','Err_']
##
fbref = sd.FBref(leagues="ENG-Premier League", seasons='2425', no_cache=True, no_store=True)
#
standard_stats = rename_cols(fbref.read_player_season_stats(stat_type='standard')).fillna(0.0)
standard_stats = combine_duplicates(standard_stats[standard_stats_columns])
#
shooting_stats = rename_cols(fbref.read_player_season_stats(stat_type='shooting')).fillna(0.0)
shooting_stats = combine_duplicates(shooting_stats[shooting_stats_columns])
#
goalshot_stats = rename_cols(fbref.read_player_season_stats(stat_type='goal_shot_creation')).fillna(0.0)
goalshot_stats = combine_duplicates(goalshot_stats[goalshot_stats_columns])
#
passing_stats = rename_cols(fbref.read_player_season_stats(stat_type='passing')).fillna(0.0)
passing_stats = combine_duplicates(passing_stats[passing_stats_columns])
#
possition_stats = rename_cols(fbref.read_player_season_stats(stat_type='possession')).fillna(0.0)
possition_stats = combine_duplicates(possition_stats[possition_stats_columns])
#
defense_stats = rename_cols(fbref.read_player_season_stats(stat_type='defense')).fillna(0.0)
defense_stats = combine_duplicates(defense_stats[defense_stats_columns])
#
data_frames = [standard_stats,shooting_stats,goalshot_stats,possition_stats,passing_stats,defense_stats]
players_data = reduce(lambda  left,right: pd.merge(left,right,on=['player'],how='outer'), data_frames).fillna(0.0).round(2)
players_data = players_data.drop_duplicates()
players_data.to_csv('fbref_players_data.csv')
#
# %%
##########################
# FBref schedule data
##########################
epl_schedule = fbref.read_schedule()
epl_schedule_df = epl_schedule.reset_index(inplace=True)
epl_schedule_df = epl_schedule[['date','time','week','home_team', 'home_xg', 'score','away_xg', 'away_team']]
epl_schedule_df['home_team'] = epl_schedule_df['home_team'].map(team_crest)
epl_schedule_df['away_team'] = epl_schedule_df['away_team'].map(team_crest)
epl_schedule_df.to_csv('fbref_schedule.csv',index=False)