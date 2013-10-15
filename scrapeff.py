from urllib.request import urlopen

from collections import OrderedDict
import string

from jinja2 import Environment, FileSystemLoader
from ediblepickle import checkpoint

import classes
import parsers
import constants
import pro_parsers


#noinspection PyUnusedLocal
@checkpoint(key=string.Template(constants.edible_pickle_template), work_dir=constants.edible_pickle_dir)
def get_html(url, url_type, week, league_label):
    html = urlopen(url).read()
    return html


def get_league_html(league, week):
    league.html_standings = get_html(constants.standings_url_template % league.id,
                                     constants.standings_label,
                                     week,
                                     league.name.replace(' ', ''))
    league.html_prev_week = get_html(constants.scores_url_template % (league.id, week - 1),
                                     constants.results_label,
                                     week,
                                     league.name.replace(' ', ''))
    league.html_cur_week = get_html(constants.scores_url_template % (league.id, week),
                                    constants.schedule_label,
                                    week,
                                    league.name.replace(' ', ''))
    return league


def parse_league_html(league):
    league.teams = parsers.parse_standings(league.html_standings)
    league.schedule = parsers.parse_scores(league.html_cur_week)

    for game in league.schedule:
        game.highest_rank = min(league.teams[game.team1_id].rank, league.teams[game.team2_id].rank)
    league.schedule.sort(key=lambda g: g.highest_rank)

    league.results = parsers.parse_scores(league.html_prev_week)
    for game in league.results:
        game.highest_rank = min(league.teams[game.team1_id].rank, league.teams[game.team2_id].rank)
    league.results.sort(key=lambda g: g.highest_rank)

    return league


def write_output(leagues_data, week, pro_data):
    env = Environment(loader=FileSystemLoader(constants.templates_dir), trim_blocks=True)

    start_week_template = env.get_template(constants.main_template)
    start_week_output = start_week_template.render(leagues=leagues_data, current_week=week, pro_data=pro_data)
    f1 = open(constants.start_week_file_path % week, 'w+')
    f1.write(start_week_output)

    end_week_template = env.get_template(constants.scores_template)
    end_week_output = end_week_template.render(leagues=leagues_data)
    f1 = open(constants.end_week_file_path % (week - 1), 'w+')
    f1.write(end_week_output)


current_week = 6

leagues = OrderedDict()
for x in constants.league_definitions:
    leagues[x[0]] = classes.League(x[0], x[1])
    leagues[x[0]] = get_league_html(leagues[x[0]], current_week)
    leagues[x[0]] = parse_league_html(leagues[x[0]])

pro_league_data = pro_parsers.extract_pro_data(leagues[constants.pro_league_id], current_week)

write_output(leagues, current_week, pro_league_data)