import re
from string import Template
from urllib.request import urlopen

from ediblepickle import checkpoint

from gwjffl import constants


# noinspection PyUnusedLocal
# https://pypi.python.org/pypi/ediblepickle
# TODO: Update constants.edible_pickle_template to be less complex
@checkpoint(key=Template(constants.edible_pickle_template), work_dir=constants.edible_pickle_dir)
def get_html(url, url_type, week, league_label):
    html = urlopen(url).read()
    return html


def get_league_html(league, week, html_type):
    if html_type is constants.standings_label:
        return get_html(constants.standings_url_template % (league.id, constants.current_year),
                        constants.standings_label,
                        week,
                        league.name.replace(' ', ''))
    if html_type is constants.prev_week_label:
        return get_html(constants.schedule_url_template % (league.id, week - 1, constants.current_year),
                        constants.results_label,
                        week,
                        league.name.replace(' ', ''))
    if html_type is constants.cur_week_label:
        return get_html(constants.schedule_url_template % (league.id, week, constants.current_year),
                        constants.schedule_label,
                        week,
                        league.name.replace(' ', ''))
    if html_type is constants.consolation_label:
        return get_html(constants.consolation_bracket_url_template % (league.id, constants.current_year),
                        constants.consolation_label,
                        week,
                        league.name.replace(' ', ''))
    return None


def get_team_html(league, week, team, html_type):
    if html_type is constants.roster_label:
        return get_html(constants.roster_url_template %
                        (league.id, team.id, constants.current_year, max(16, constants.current_week)),
                        constants.roster_label,
                        week,
                        'Keeper_%s' % re.sub(r'[\W_]+', '', team.name))
    return None


def get_player_html(league, week, team, player, html_type):
    if html_type is constants.transactions_label:
        return get_html(constants.transactions_url_template % (league.id, player.id),
                        constants.transactions_label,
                        week,
                        'Keeper_%s_%s' % (re.sub(r'[\W_]+', '', team.name), re.sub(r'[\W_]+', '', player.name)))
    return None
