import pandas as pd
from nba_api.stats.static import teams
from nba_api.stats.endpoints import leaguegamefinder
from nba_api.live.nba.endpoints import boxscore
import string

all_teams = teams.get_teams()

#get Nugggets 
def get_team(team_name: str):
    for team in all_teams:
        if team_name.lower().capitalize() in team['full_name']:
            return team
    return None    


nuggets = get_team('denver')
nuggets_id = nuggets['id']

#all Nuggets games
get_games = leaguegamefinder.LeagueGameFinder(team_id_nullable=nuggets_id)
games = get_games.get_data_frames()[0]

all_games = pd.DataFrame(games)

#2025-26 Nuggets games
this_season = all_games[all_games['SEASON_ID'] == '22025']
print(len(this_season))
#Last Nuggets game
print(this_season.iloc[0]['MIN'])

print(type(this_season.iloc[0]['GAME_ID']))
#player usage calculator
def usage_calc(fga, fta, to, mp, team_minutes, team_fga, team_fta, team_to):
    numerator = (fga + 0.44*fta + to) * (team_minutes / 5)
    denominator = mp * (team_fga + 0.44*team_fta + team_to)
    return round(100*(numerator / denominator), 2)


def clean_minutes(minutes: str)->int:
    clean = ''
    for char in minutes:
        if char not in string.ascii_letters:
            clean += char
    return int(clean)


dataFrame = []

#iterate throug all games this season chronologically 
for i in range(len(this_season) - 1, -1, -1):
    matchup = this_season.iloc[i]['MATCHUP']
    game_id = this_season.iloc[i]['GAME_ID']
    score = boxscore.BoxScore(game_id)

    team_minutes = this_season.iloc[i]['MIN']
    team_fga = this_season.iloc[i]['FGA']
    team_fta = this_season.iloc[i]['FTA']
    team_to = this_season.iloc[i]['TOV']

    jokic_playing = False
    active_players = 0

    sign = '@'

    is_away = '@' in matchup

    stats = score.away_team_player_stats.get_dict() if is_away else score.home_team_player_stats.get_dict()

    for player in stats:
        if player['status'] != 'ACTIVE':
            continue

        #Jokic ID
        if player['personId'] == 203999:
            jokic_playing = True

        minutes = player['statistics']['minutesCalculated']
        minutes_clean = clean_minutes(minutes)

        if minutes_clean < 15:
            continue
            
        usage = usage_calc(player['statistics']['fieldGoalsAttempted'], 
                                player['statistics']['freeThrowsAttempted'],
                                player['statistics']['turnovers'],
                                int(minutes_clean),
                                team_minutes,
                                team_fga,
                                team_fta,
                                team_to)
                                   
        row = {'game_id': game_id,'matchup':matchup,'date':this_season.iloc[i]['GAME_DATE'],'name':player['name'], 'usage %': usage, 'minutes':int(minutes_clean), 'jokic_playing':None}
        dataFrame.append(row)
        active_players += 1

    for r in dataFrame[-active_players:]:
        r['jokic_playing'] = jokic_playing


df2 = pd.DataFrame(dataFrame)
df2.sort_values('usage %',ascending=False).to_csv('denver_usage.csv', index=False)
print(df2.shape)
print(df2.sort_values(by='usage %', ascending=False)[:30])
    


    




    


