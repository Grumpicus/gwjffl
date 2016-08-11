import json

from bs4 import BeautifulSoup

from gwjffl import constants
from gwjffl.classes import gwjffl
from gwjffl.io.web import get_team_html


def get_keeper_prices(keeper_league):
    # Go to each team page get the roster
    for team_id in keeper_league.teams:
        # print(team_id)
        team = keeper_league.teams[team_id]
        team_html = get_team_html(keeper_league, constants.current_week, team, constants.roster_label)
        roster = parse_roster_html(team_html)
        team.roster = roster
    return keeper_league


def parse_roster_html(html):
    global tooltips
    roster = []
    soup = BeautifulSoup(html, 'html.parser')
    page_data = str(soup.find(id='page-data').contents[0])
    json_value = '{%s}' % (page_data.split('{', 1)[1].rsplit('}', 1)[0],)
    tooltips = json.loads(json_value)['tooltips']
    rows = soup.find_all('tr', id=constants.row_partial_id)
    for row in rows:
        roster.append(extract_player_info_from_row(row))

    return roster


def extract_player_info_from_row(row):
    # print(row)
    player = gwjffl.Player()

    div_player_name = row.find('div', class_=constants.player_name_class)
    a_player_text = div_player_name.find('a')
    player.name = a_player_text.text
    player.url = '%s%s' % (constants.fleaflicker_url, a_player_text['href'])

    # last_sign_in_tooltip = [item for item in tooltips if a_user_name['id'] in item["ids"]][0]['contents']
    acquisition_tooltip = [item for item in tooltips if a_player_text['id'] in item["ids"]][0]['contents']
    span_acquisition_how = BeautifulSoup(acquisition_tooltip, 'html.parser').find('span')
    player.acquired_how = span_acquisition_how.text
    acquisition_when = span_acquisition_how.next_sibling[2:]
    player.acquired_when_year = int(acquisition_when[-4:])
    player.acquired_when_text = acquisition_when[:-5]
    player.acquired = calculate_acquisition(player)

    start = player.url.find(constants.player_id_param) + len(constants.player_id_param)
    end = player.url.find('?', start)
    player.id = player.url[start:None if end == -1 else end]

    div_player_info = row.find('div', class_=constants.player_info_class)
    player.position = div_player_info.find('span', class_=constants.player_position_class).text
    player.team = div_player_info.find('span', class_=constants.player_team_class).text

    div_fp_total = row.find('div', class_=constants.player_fptotal_class)
    if div_fp_total:
        player.season_avg = float(div_fp_total.previous_sibling.text)
        fp_total = div_fp_total.find('span', class_=constants.player_fp_class)
        player.season_total = float(fp_total.text)

    return player


def calculate_acquisition(player):
    if player.acquired_when_year < constants.current_year:
        acquisition = 'Keeper'
    else:
        if player.acquired_how == 'Imported':
            acquisition = 'Drafted'
        else:
            acquisition = player.acquired_how
    return acquisition
