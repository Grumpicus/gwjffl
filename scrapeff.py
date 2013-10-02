__author__ = 'Grumpicus'

from collections import OrderedDict
import urllib2
import string

from jinja2 import Environment, FileSystemLoader
from ediblepickle import checkpoint

import classes
import parsers
import constants


env = Environment(loader=FileSystemLoader('templates'), trim_blocks=True)

current_week = 5


@checkpoint(key=string.Template('{1}_week{3}_{2}.html'), work_dir='pickles')
def get_html(url, league_name, url_type, week):
    html = urllib2.urlopen(url).read()
    return html


def get_and_parse_league_data():
    league_data = OrderedDict()

    #get data
    for i, x in enumerate(constants.league_info_list):
        league_data[x[0]] = classes.League(x, current_week, i)
        league_data[x[0]].html_standings = get_html(league_data[x[0]].url_standings,
                                                    league_data[x[0]].name.replace(' ', ''), constants.standings,
                                                    current_week)
        league_data[x[0]].html_cur_week = get_html(league_data[x[0]].url_cur_week,
                                                   league_data[x[0]].name.replace(' ', ''), constants.cur_week,
                                                   current_week)
        league_data[x[0]].html_prev_week = get_html(league_data[x[0]].url_prev_week,
                                                    league_data[x[0]].name.replace(' ', ''), constants.prev_week,
                                                    current_week)

    #parse data
    for x in league_data:
        league_data[x].teams = parsers.parse_standings(league_data[x].html_standings)

        league_data[x].schedule = parsers.parse_scores(league_data[x].html_cur_week)
        for game in league_data[x].schedule:
            game.highest_rank = min(league_data[x].teams[game.team1_id].rank, league_data[x].teams[game.team2_id].rank)
        league_data[x].schedule.sort(key=lambda game: game.highest_rank)

        league_data[x].results = parsers.parse_scores(league_data[x].html_prev_week)
        for game in league_data[x].results:
            game.highest_rank = min(league_data[x].teams[game.team1_id].rank, league_data[x].teams[game.team2_id].rank)
        league_data[x].results.sort(key=lambda game: game.highest_rank)

    return league_data


leagues = get_and_parse_league_data()

start_week_template = env.get_template('main.template')
start_week_output = start_week_template.render(leagues=leagues)
f1 = open('output/start_week%s.html' % current_week, 'w+')
f1.write(start_week_output)

end_week_template = env.get_template('scores.template')
end_week_output = end_week_template.render(leagues=leagues)
f1 = open('output/end_week%s.html' % current_week, 'w+')
f1.write(end_week_output)
