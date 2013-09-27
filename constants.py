__author__ = 'Grumpicus'

league_info_list = [(120356, 'Dynasty'),
                    (92221, 'Keeper'),
                    (131597, 'Pro'),
                    (34260, 'Division I'),
                    (33978, 'Division II')]

fleaflicker_url = 'http://www.fleaflicker.com'
standings_url = 'http://www.fleaflicker.com/nfl/league?leagueId=%s'
scores_url = 'http://www.fleaflicker.com/nfl/league-schedule?leagueId=%s&week=%s'

standings = 'standings'
cur_week = 'schedule'
prev_week = 'results'

user_name_class = 'user-name'
league_name_class = 'league-name'
team_id_param = 'teamId='
horizontal_spacer_class = 'horizontal-spacer'
vertical_spacer_class = 'vertical-spacer'
cell_row_class = 'cell-row'
scoreboard_class = 'scoreboard'
projected_class = 'projected'

#scoreboard/schedule
game_team_ids = {
    'game1_team1_id': 'row_0_0_0',
    'game1_team2_id': 'row_0_0_1',

    'game2_team1_id': 'row_0_1_0',
    'game2_team2_id': 'row_0_1_1',

    'game3_team1_id': 'row_0_2_0',
    'game3_team2_id': 'row_0_2_1',

    'game4_team1_id': 'row_1_0_0',
    'game4_team2_id': 'row_1_0_1',

    'game5_team1_id': 'row_1_1_0',
    'game5_team2_id': 'row_1_1_1',

    'game6_team1_id': 'row_1_2_0',
    'game6_team2_id': 'row_1_2_1'
}

