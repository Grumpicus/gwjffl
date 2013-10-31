#python_version: 3.3.2

from urllib.request import urlopen
from collections import OrderedDict
from string import Template

from jinja2 import Environment, FileSystemLoader
from ediblepickle import checkpoint

import constants
from classes import League
from parsers import extract_pro_data, parse_standings, parse_scores
from jsonstore import pickle_json_to_file, unpickle_json_from_file



#noinspection PyUnusedLocal
@checkpoint(key=Template(constants.edible_pickle_template), work_dir=constants.edible_pickle_dir)
def get_html(url, url_type, week, league_label):
    html = urlopen(url).read()
    return html


def get_league_html(league, week, type):
    if type is constants.standings_label:
        return get_html(constants.standings_url_template % league.id,
                        constants.standings_label,
                        week,
                        league.name.replace(' ', ''))
    if type is constants.prev_week_label:
        return get_html(constants.scores_url_template % (league.id, week - 1),
                        constants.results_label,
                        week,
                        league.name.replace(' ', ''))
    if type is constants.cur_week_label:
        return get_html(constants.scores_url_template % (league.id, week),
                        constants.schedule_label,
                        week,
                        league.name.replace(' ', ''))
    return None


def parse_league_html(league, week):
    league.teams = parse_standings(get_league_html(league, week, constants.standings_label))
    league = add_prev_week_rankings(league, week)
    league.schedule = parse_scores(get_league_html(league, week, constants.cur_week_label))

    for game in league.schedule:
        game.highest_rank = min(league.teams[game.team1_id].rank, league.teams[game.team2_id].rank)
    league.schedule.sort(key=lambda g: g.highest_rank)

    league.results = parse_scores(get_league_html(league, week, constants.prev_week_label))
    for game in league.results:
        game.highest_rank = min(league.teams[game.team1_id].prev_rank, league.teams[game.team2_id].prev_rank)
    league.results.sort(key=lambda g: g.highest_rank)

    return league


def write_output(leagues_data, week, pro_data):
    env = Environment(loader=FileSystemLoader(constants.templates_dir), trim_blocks=True)

    start_week_template = env.get_template(constants.main_template)
    start_week_output = start_week_template.render(leagues=leagues_data, current_week=week, pro_data=pro_data)
    f1 = open(constants.start_week_file_path % week, 'w+')
    f1.write(start_week_output)

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


def main():
    leagues = OrderedDict()
    for x in constants.league_definitions:
        leagues[x[0]] = League(x[0], x[1])
        leagues[x[0]] = parse_league_html(leagues[x[0]], constants.current_week)
        pickle_json_to_file(constants.league_week_storage_path_template % (constants.current_week, x[0]), leagues[x[0]])

    pro_league_data = extract_pro_data(leagues[constants.pro_league_id], constants.current_week)

    write_output(leagues, constants.current_week, pro_league_data)


if __name__ == "__main__":
    main()