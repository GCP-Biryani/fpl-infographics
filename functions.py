import requests
import pandas as pd
import time

# URL pattern to get the weekly summary data for a player by their element ID
element_summary_url = "https://fantasy.premierleague.com/api/element-summary/{}/"

def get_player_name(player_id):
    player_raw = pd.read_csv('data/players_raw.csv')
    name = player_raw.loc[player_raw['id'] == player_id]['web_name'].to_string(index=False)
    return name

def get_player_team(player_id):
    player_raw = pd.read_csv('data/players_raw.csv')
    team = player_raw.loc[player_raw['id'] == player_id]['team'].to_string(index=False)
    return team

def get_player_position(player_id):
    player_raw = pd.read_csv('data/players_raw.csv')
    position = player_raw.loc[player_raw['id'] == player_id]['element_type'].to_string(index=False)
    return position

# Function to get weekly data for a specific player by their element ID
def get_player_weekly_data(player_id):
    response = requests.get(element_summary_url.format(player_id))
    return response.json()

def extract_all_players_data(picks):
    all_player_history = []

    # Loop through each player
    for player in picks:
        player_id = player
        name = get_player_name(player)
        team = get_player_team(player)
        position = get_player_position(player)
        #print(f"Fetching data for player {name}")

        # Get player weekly data
        player_weekly_data = get_player_weekly_data(player_id)

        # Loop through each gameweek history and create separate rows
        for gameweek in player_weekly_data.get('history', []):
            player_data = {
                'id': player,
                'name': name,
                'team': team,
                'position': position,
                'total_points': gameweek['total_points'],
                'round': gameweek['round'],
                'minutes': gameweek['minutes'],
                'goals_scored': gameweek['goals_scored'],
                'assists': gameweek['assists'],
                'clean_sheets': gameweek['clean_sheets'],
                'goals_conceded': gameweek['goals_conceded'],
                'own_goals': gameweek['own_goals'],
                'penalties_saved': gameweek['penalties_saved'],
                'penalties_missed': gameweek['penalties_missed'],
                'yellow_cards': gameweek['yellow_cards'],
                'red_cards': gameweek['red_cards'],
                'saves': gameweek['saves'],
                'bonus': gameweek['bonus'],
                'bps': gameweek['bps'],
                'influence': gameweek['influence'],
                'creativity': gameweek['creativity'],
                'threat': gameweek['threat'],
                'ict_index': gameweek['ict_index'],
                'starts': gameweek['starts'],
                'expected_goals': gameweek['expected_goals'],
                'expected_assists': gameweek['expected_assists'],
                'expected_goal_involvements': gameweek['expected_goal_involvements'],
                'expected_goals_conceded': gameweek['expected_goals_conceded'],
                # 'value': gameweek['value'],
                # 'transfers_balance': gameweek['transfers_balance'],
                # 'selected': gameweek['selected'],
                # 'transfers_in': gameweek['transfers_in'],
                # 'transfers_out': gameweek['transfers_out']
            }
            all_player_history.append(player_data)

        # Pause between requests to avoid rate-limiting
        time.sleep(1)  # Adjust sleep time if necessary

    return all_player_history