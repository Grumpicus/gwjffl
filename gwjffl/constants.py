import re
from collections import OrderedDict

current_year = 2016
current_week = 2

# leagues # TODO: Convert to OrderedDict?
league_definitions = [(131597, 'Pro'),
                      (34260, 'Division I'),
                      (33978, 'Division II'),
                      (92221, 'Keeper'),
                      (120356, 'Dynasty')]

pro_league_id = 131597

# keepers
max_keepers_week = 13
ineligible_label = 'Ineligible'
keeper_spreadsheet_id = '1BYucUOA4g661z8izWGXD9Z5gA3n1otdcR_Q1uarBElA'
keeper_worksheet_id = 'Rosters'

sub_dir_year_week = '/%d/%d' % (current_year, current_week)
sub_dir_year = '/%d' % current_year


# edible_pickle
edible_pickle_dir = '../pickles' + sub_dir_year_week
edible_pickle_template = 'week{2}_{1}_{3}.html'

# templates
templates_dir = '../templates'
main_template = 'main.template'
week_end_scores_template = 'week_end_scores.template'
keeper_template = 'keeper.jinja'

# output
output_dir = '../output' + sub_dir_year_week
start_week_file_path = output_dir + '/start_week%d.html'
end_week_file_path = output_dir + '/end_week%d.html'
keepers_file_path = output_dir + '/keepers.html'

# data_store
data_store_dir = '../data_store' + sub_dir_year
pro_data_storage_path = data_store_dir + '/pro_data.json'
league_week_storage_path_template = data_store_dir + '/week%d_league%d.json'

# misc
standings_label = 'standings'
schedule_label = 'schedule'
results_label = 'results'
cur_week_label = 'cur_week'
prev_week_label = 'prev_week'
consolation_label = 'consolation'
roster_label = 'roster'
transactions_label = 'transactions'

# fleaflicker
fleaflicker_url = 'http://www.fleaflicker.com'
standings_url_template = 'http://www.fleaflicker.com/nfl/leagues/%s?season=%s'
schedule_url_template = 'http://www.fleaflicker.com/nfl/leagues/%s/scores?week=%s&season=%s'
# playoffs_bracket_url_template = 'http://www.fleaflicker.com/nfl/leagues/%s/playoffs'
consolation_bracket_url_template = 'http://www.fleaflicker.com/nfl/leagues/%s/playoffs?bracketIndex=1&season=%s'
roster_url_template = 'http://www.fleaflicker.com/nfl/leagues/%s/teams/%s?season=%d&week=%d'  # http://www.fleaflicker.com/nfl/leagues/92221/teams/648518?season=2015&week=14
transactions_url_template = 'http://www.fleaflicker.com/nfl/leagues/%s/transactions?playerId=%s'

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

player_name_class = 'player-name'
player_id_param = '/players/'
player_info_class = 'player-info'
player_position_class = 'position'
player_team_class = 'player-team'
player_fptotal_class = 'fp-total'
player_fp_class = 'fp'

# transactions
player_inline_class = 'player-inline'
list_group_item_text_class = 'list-group-item-text'
relative_date_class = 'relative-date'

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