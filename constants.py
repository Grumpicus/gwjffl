current_week = 7

#leagues
league_definitions = [(131597, 'Pro'),
                      (34260, 'Division I'),
                      (33978, 'Division II'),
                      (92221, 'Keeper'),
                      (120356, 'Dynasty')]

pro_league_id = 131597

#edible_pickle
edible_pickle_dir = 'pickles'
edible_pickle_template = 'week{2}_{1}_{3}.html'

#templates
templates_dir = 'templates'
main_template = 'main.template'
week_end_scores_template = 'week_end_scores.template'

#output
start_week_file_path = 'output/start_week%d.html'
end_week_file_path = 'output/end_week%d.html'

standings_label = 'standings'
schedule_label = 'schedule'
results_label = 'results'

#data_store
json_storage_path = 'data_store/data.json'

#fleaflicker
fleaflicker_url = 'http://www.fleaflicker.com'
standings_url_template = 'http://www.fleaflicker.com/nfl/league?leagueId=%s'
scores_url_template = 'http://www.fleaflicker.com/nfl/league-schedule?leagueId=%s&week=%s'

user_name_class = 'user-name'
league_name_class = 'league-name'
team_id_param = 'teamId='
horizontal_spacer_class = 'horizontal-spacer'
vertical_spacer_class = 'vertical-spacer'
cell_row_class = 'cell-row'
scoreboard_class = 'scoreboard'
projected_class = 'projected'

scoreboard_ids = {
    'game1_team1_id': 'row_0_0_0',
    'game1_team2_id': 'row_0_0_1',
    'game1_box_link_id': 'row_0_0_2',

    'game2_team1_id': 'row_0_1_0',
    'game2_team2_id': 'row_0_1_1',
    'game2_box_link_id': 'row_0_1_2',

    'game3_team1_id': 'row_0_2_0',
    'game3_team2_id': 'row_0_2_1',
    'game3_box_link_id': 'row_0_2_2',

    'game4_team1_id': 'row_1_0_0',
    'game4_team2_id': 'row_1_0_1',
    'game4_box_link_id': 'row_1_0_2',

    'game5_team1_id': 'row_1_1_0',
    'game5_team2_id': 'row_1_1_1',
    'game5_box_link_id': 'row_1_1_2',

    'game6_team1_id': 'row_1_2_0',
    'game6_team2_id': 'row_1_2_1',
    'game6_box_link_id': 'row_1_2_2'
}
