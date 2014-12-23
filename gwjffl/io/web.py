from string import Template
from urllib.request import urlopen

from ediblepickle import checkpoint

from gwjffl import constants



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
        return get_html(constants.schedule_url_template % (league.id, week - 1),
                        constants.results_label,
                        week,
                        league.name.replace(' ', ''))
    if html_type is constants.cur_week_label:
        return get_html(constants.schedule_url_template % (league.id, week),
                        constants.schedule_label,
                        week,
                        league.name.replace(' ', ''))
    if html_type is constants.consolation_label:
        return get_html(constants.consolation_bracket_url_template % league.id,
                        constants.consolation_label,
                        week,
                        league.name.replace(' ', ''))
    return None