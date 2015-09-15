from collections import OrderedDict
import re

current_year = 2015
current_week = 2

# leagues
league_definitions = [(131597, 'Pro'),
                      (34260, 'Division I'),
                      (33978, 'Division II'),
                      (92221, 'Keeper'),
                      (120356, 'Dynasty')]

pro_league_id = 131597

# edible_pickle
edible_pickle_dir = '../pickles'
edible_pickle_template = 'week{2}_{1}_{3}.html'

# templates
templates_dir = '../templates'
main_template = 'main.template'
week_end_scores_template = 'week_end_scores.template'

# output
output_dir = '../output'
start_week_file_path = output_dir + '/start_week%d.html'
end_week_file_path = output_dir + '/end_week%d.html'

#misc
standings_label = 'standings'
schedule_label = 'schedule'
results_label = 'results'
cur_week_label = 'cur_week'
prev_week_label = 'prev_week'
consolation_label = 'consolation'

#data_store
data_store_dir = '../data_store'
pro_data_storage_path = data_store_dir + '/pro_data.json'
league_week_storage_path_template = data_store_dir + '/week%d_league%d.json'

#fleaflicker
fleaflicker_url = 'http://www.fleaflicker.com'
standings_url_template = 'http://www.fleaflicker.com/nfl/league?leagueId=%s'
schedule_url_template = 'http://www.fleaflicker.com/nfl/league-schedule?leagueId=%s&week=%s'
# playoffs_bracket_url_template = 'http://www.fleaflicker.com/nfl/showBracket.do?leagueId=%s&bracketIndex=0'
consolation_bracket_url_template = 'http://www.fleaflicker.com/nfl/showBracket.do?leagueId=%s&bracketIndex=1'

user_name_class = 'user-name'
league_name_class = 'league-name'
tt_content_class = 'tt-content'
team_id_param = '/teams/'
horizontal_spacer_class = 'horizontal-spacer'
vertical_spacer_class = 'vertical-spacer'
# cell_row_class = 'cell-row'
row_partial_id = re.compile("^row_")
scoreboard_class = 'scoreboard'
projected_class = 'projected'
text_success_class = 'text-success'
text_success_style = 'color:#009900;'
text_error_class = 'text-error'
text_eliminated_class = 'eliminated'
text_error_style = 'color:#990000; text-decoration:line-through;'
icon_trophy_class = 'fa-trophy'
inactive_class = 'inactive'

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

team_notes_style_default = 'font-size:8pt; cursor:help; border-bottom:1px dashed;'
#OrderedDict for printing in main.template
team_notes = OrderedDict((x[0], x[1]) for x in [
    ((text_success_style, '*'), 'Would make playoffs if season ended now'),
    ((text_success_style, 'y'), 'Clinched division'),
    ((text_success_style, 'z'), 'Clinched round 1 bye'),
    ((text_success_style, 'x'), 'Clinched wildcard'),
    ((text_error_style, 'y'), 'Eliminated from division contention'),
    ((text_error_style, 'z'), 'Eliminated from round 1 bye contention'),
    ((text_error_style, 'o'), 'Eliminated from wildcard contention')
])

#nfl
nfl_schedule_url_template = 'http://www.nfl.com/schedules/%d/REG%d'

nfl_schedules_div_class = 'schedules'
nfl_schedules_header_byes_span_class = 'schedules-header-byes'
nfl_bye_team_span_class = 'bye-team'
nfl_schedules_list_date_div_class = 'schedules-list-date'
nfl_schedules_centerpiece_div_id = 'schedules-centerpiece'
nfl_schedules_table_ul_class = 'schedules-table'
nfl_schedules_list_matchup_li_class = 'schedules-list-matchup'