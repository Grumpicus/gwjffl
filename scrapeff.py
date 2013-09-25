__author__ = 'Grumpicus'

from jinja2 import Environment, FileSystemLoader
#import urllib2
#import jsonpickle

from mocks import week4
import classes
import parsers

env = Environment(loader=FileSystemLoader('templates'), trim_blocks=True, lstrip_blocks=True)

league_info_list = [(120356, 'Dynasty'),
                    (92221, 'Keeper'),
                    (131597, 'Pro'),
                    (34260, 'Division I'),
                    (33978, 'Division II')]
current_week = 4


def get_and_parse_league_data():
    league_data = {}

    for x in league_info_list:
        league_data[x[0]] = classes.League(x, current_week)
        #leagues[x[0]].html_standings = urllib2.urlopen(leagues[x[0]].url_standings).read()
        #leagues[x[0]].html_prev_week = urllib2.urlopen(leagues[x[0]].url_prev_week).read()
        #leagues[x[0]].html_cur_week = urllib2.urlopen(leagues[x[0]].url_cur_week).read()
        league_data[x[0]].html_standings = week4.standings_mock[x[0]]
        league_data[x[0]].html_prev_week = week4.prev_week_mock[x[0]]
        league_data[x[0]].html_cur_week = week4.cur_week_mock[x[0]]

    for x in league_data:
        league_data[x].teams = parsers.parse_standings(league_data[x].html_standings)
        league_data[x].results = parsers.parse_prev_week(league_data[x].html_prev_week)
        league_data[x].schedule = parsers.parse_cur_week(league_data[x].html_cur_week)

    return league_data


leagues = get_and_parse_league_data()
sorted_leagues = []

for l in league_info_list:
    sorted_leagues.append(leagues[l[0]])
#print jsonpickle.encode(sorted_leagues)

template = env.get_template('standings.template')

print template.render(sorted_leagues=sorted_leagues)