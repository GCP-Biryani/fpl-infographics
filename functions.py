import requests
import pandas as pd
import time
import plotly.express as px

# URL pattern to get the weekly summary data for a player by their element ID
element_summary_url = "https://fantasy.premierleague.com/api/element-summary/{}/"

def get_player_name(player_id):
    player_raw = pd.read_csv('players_raw.csv')
    name = player_raw.loc[player_raw['id'] == player_id]['web_name'].to_string(index=False)
    return name

def get_player_team(player_id):
    player_raw = pd.read_csv('players_raw.csv')
    team = player_raw.loc[player_raw['id'] == player_id]['team'].to_string(index=False)
    return team

def get_player_position(player_id):
    player_raw = pd.read_csv('players_raw.csv')
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
### Mini-league functions
import plotly.express as px

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
