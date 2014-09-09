# python_version: 3.3.2

from urllib.request import urlopen
from collections import OrderedDict
from string import Template

from jinja2 import Environment, FileSystemLoader
from ediblepickle import checkpoint

from gwjffl import constants
from gwjffl.classes.gwjffl import League
from gwjffl.parsers.gwjffl import extract_pro_data, parse_standings, parse_scores
from gwjffl.parsers.nfl import parse_nfl_html
from gwjffl.io.jsonstore import pickle_json_to_file, unpickle_json_from_file



# noinspection PyUnusedLocal
@checkpoint(key=Template(constants.edible_pickle_template), work_dir=constants.edible_pickle_dir)
def get_html(url, url_type, week, league_label):
    html = urlopen(url).read()
    return html


def get_league_html(league, week, html_type):
    if html_type is constants.standings_label:
        return get_html(constants.standings_url_template % league.id,
                        constants.standings_label,
                        week,
                        league.name.replace(' ', ''))
    if html_type is constants.prev_week_label:
        return get_html(constants.scores_url_template % (league.id, week - 1),
                        constants.results_label,
                        week,
                        league.name.replace(' ', ''))
    if html_type is constants.cur_week_label:
        return get_html(constants.scores_url_template % (league.id, week),
                        constants.schedule_label,
                        week,
                        league.name.replace(' ', ''))
    return None


def get_nfl_html(week):
    return get_html(constants.nfl_schedule_url_template % (constants.current_year, week),
                    constants.schedule_label,
                    week,
                    'NFL')


def parse_league_html(league, week):
    league.teams = parse_standings(get_league_html(league, week, constants.standings_label))
    league = add_prev_week_rankings(league, week)

    if constants.current_week > 1:
        league.results = parse_scores(get_league_html(league, week, constants.prev_week_label))
        for game in league.results:
            game.highest_rank = min(league.teams[game.team1_id].prev_rank, league.teams[game.team2_id].prev_rank)
        league.results.sort(key=lambda g: g.highest_rank)

    if constants.current_week < 17:
        league.schedule = parse_scores(get_league_html(league, week, constants.cur_week_label))
        for game in league.schedule:
            game.highest_rank = min(league.teams[game.team1_id].rank, league.teams[game.team2_id].rank)
        league.schedule.sort(key=lambda g: g.highest_rank)

    return league


def write_output(leagues_data, week, pro_data, nfl_data):
    env = Environment(loader=FileSystemLoader(constants.templates_dir), trim_blocks=True)

    start_week_template = env.get_template(constants.main_template)
    start_week_output = start_week_template.render(leagues=leagues_data, current_week=week, pro_data=pro_data,
                                                   legend=constants.team_notes, nfl_data=nfl_data)
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
    if constants.current_week < 0 or constants.current_week > 17:
        print('ERROR: Invalid current week: %d' % constants.current_week)
        return

    leagues = OrderedDict()
    for x in constants.league_definitions:
        leagues[x[0]] = League(x[0], x[1])
        leagues[x[0]] = parse_league_html(leagues[x[0]], constants.current_week)
        pickle_json_to_file(constants.league_week_storage_path_template % (constants.current_week, x[0]), leagues[x[0]])

    pro_league_data = extract_pro_data(leagues[constants.pro_league_id], constants.current_week)

    nfl_week_data = parse_nfl_html(get_nfl_html(constants.current_week))

    write_output(leagues, constants.current_week, pro_league_data, nfl_week_data)


if __name__ == "__main__":
    main()