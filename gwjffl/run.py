# python_version: 3.4.3

from collections import OrderedDict
import os
import errno

from jinja2 import Environment, FileSystemLoader

from gwjffl import constants
from gwjffl.classes.gwjffl import League
from gwjffl.io.web import get_html, get_league_html
from gwjffl.parsers.gwjffl import extract_pro_data, parse_standings, parse_schedule, parse_scores
from gwjffl.parsers.nfl import parse_nfl_html
from gwjffl.io.jsonstore import pickle_json_to_file, unpickle_json_from_file


def get_nfl_html(week):
    return get_html(constants.nfl_schedule_url_template % (constants.current_year, week),
                    constants.schedule_label,
                    week,
                    'NFL')


def parse_league_html(league, week):
    league.teams = parse_standings(get_league_html(league, week, constants.standings_label))
    # if constants.current_week > 1:
    league = add_prev_week_rankings(league, week)

    if constants.current_week > 1:
        league.results = parse_schedule(get_league_html(league, week, constants.prev_week_label))
        for game in league.results:
            game.highest_rank = min(league.teams[game.team1_result.team_id].prev_rank,
                                    league.teams[game.team2_result.team_id].prev_rank)
        league.results.sort(key=lambda g: g.highest_rank)

        league.scores = parse_scores(get_league_html(league, week, constants.prev_week_label))

    if constants.current_week < 17:
        league.schedule = parse_schedule(get_league_html(league, week, constants.cur_week_label))
        for game in league.schedule:
            game.highest_rank = min(league.teams[game.team1_result.team_id].rank,
                                    league.teams[game.team2_result.team_id].rank)
        league.schedule.sort(key=lambda g: g.highest_rank)

    return league


def write_output(leagues_data, week, pro_data, nfl_data):
    env = Environment(loader=FileSystemLoader(constants.templates_dir), trim_blocks=True)
    env.add_extension('jinja2.ext.do')

    start_week_template = env.get_template(constants.main_template)
    start_week_output = start_week_template.render(leagues=leagues_data, current_week=week, pro_data=pro_data,
                                                   legend=constants.team_notes, nfl_data=nfl_data)
    f1 = open(constants.start_week_file_path % week, 'w+')
    f1.write(start_week_output)

    if constants.current_week > 1:
        end_week_template = env.get_template(constants.week_end_scores_template)
        end_week_output = end_week_template.render(leagues=leagues_data)
        f1 = open(constants.end_week_file_path % (week - 1), 'w+')
        f1.write(end_week_output)


def add_prev_week_rankings(league, current_week):
    file = constants.league_week_storage_path_template % (current_week - 1, league.id)
    prev_league = unpickle_json_from_file(file)

    if prev_league is not None:
        for team_id in league.teams:
            league.teams[team_id].prev_rank = prev_league.teams[team_id].rank

    return league


def make_sure_path_exists(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise


def init():
    os.makedirs(constants.data_store_dir, exist_ok=True)
    os.makedirs(constants.edible_pickle_dir, exist_ok=True)
    os.makedirs(constants.output_dir, exist_ok=True)


def main():
    if constants.current_week < 0 or constants.current_week > 17:
        print('ERROR: Invalid current week: %d' % constants.current_week)
        return

    init()

    leagues = OrderedDict()
    for x in constants.league_definitions:
        leagues[x[0]] = League(x[0], x[1])
        leagues[x[0]] = parse_league_html(leagues[x[0]], constants.current_week)
        pickle_json_to_file(constants.league_week_storage_path_template % (constants.current_week, x[0]), leagues[x[0]])

    pro_league_data = extract_pro_data(leagues[constants.pro_league_id], constants.current_week)

    if 0 < constants.current_week < 17:
        nfl_week_data = parse_nfl_html(get_nfl_html(constants.current_week))
    else:
        nfl_week_data = {}

    write_output(leagues, constants.current_week, pro_league_data, nfl_week_data)


if __name__ == "__main__":
    main()