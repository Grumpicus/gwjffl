import json
import re
from datetime import datetime

from bs4 import BeautifulSoup

from gwjffl import constants
from gwjffl.classes import gwjffl
from gwjffl.io.web import get_team_html, get_player_html


tooltips = {}  # global
transaction_tooltips = {}  # global


def get_keeper_prices(keeper_league):
    # Go to each team page get the roster
    i = 0
    for team_id in keeper_league.teams:
        i += 1
        print("%d. Getting Keeper prices for team_id: %s" % (i, team_id))
        team = keeper_league.teams[team_id]
        team_html = get_team_html(keeper_league, constants.current_week, team, constants.roster_label)
        roster = parse_roster_html(team_html)
        team.roster = roster
    # TODO: Figure out the optimal time and place to add transaction data
    print("Adding transaction data")
    keeper_league = add_transaction_data(keeper_league)
    print("Calculating player values")
    keeper_league = calculate_player_values(keeper_league)
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
        player_info = extract_player_info_from_row(row)
        if player_info:
            roster.append(extract_player_info_from_row(row))

    return roster


def extract_player_info_from_row(row):
    # print(row)
    player = gwjffl.Player()

    div_player_name = row.find('div', class_=constants.player_name_class)
    a_player_text = div_player_name.find('a')
    if not a_player_text:  # blank row; empty roster slot
        return None
    player.name = a_player_text.text
    player.url = '%s%s' % (constants.fleaflicker_url, a_player_text['href'])

    # last_sign_in_tooltip = [item for item in tooltips if a_user_name['id'] in item["ids"]][0]['contents']
    acquisition_tooltip = [item for item in tooltips if a_player_text['id'] in item["ids"]][0]['contents']
    span_acquisition_how = BeautifulSoup(acquisition_tooltip, 'html.parser').find('span')
    player.acquired_how = span_acquisition_how.text
    acquisition_when = span_acquisition_how.next_sibling[2:]
    player.acquired_when_year = int(acquisition_when[-4:])
    player.acquired_when_text = acquisition_when[:-5]
    acquisition = calculate_acquisition(player)
    player.keeper_status = acquisition if acquisition else 'ERROR'

    start = player.url.find(constants.player_id_param) + len(constants.player_id_param)
    end = player.url.find('?', start)
    player.SEO_id = player.url[start:None if end == -1 else end]
    player.id = player.SEO_id[player.SEO_id.rindex('-') + 1:]

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
        week_maybe = player.acquired_when_text[-2:].strip()
        acquired_when_week = int(week_maybe) if week_maybe.isnumeric() else 0
        if player.acquired_how == 'Imported':
            acquisition = 'Drafted'
        elif acquired_when_week > constants.max_keepers_week:
            acquisition = constants.ineligible_label
        else:
            acquisition = player.acquired_how
    return acquisition


def add_transaction_data(league):
    i = 0
    for team_id in league.teams:
        i += 1
        print("%d. Adding transaction data for team_id: %s" % (i, team_id))
        team = league.teams[team_id]

        for player in team.roster:
            print("%d. Adding transaction data for player: %s" % (i, player.name))
            # print(player.id, player.name)
            player_html = get_player_html(league, constants.current_week, team, player, constants.transactions_label)
            player.transactions = parse_transactions_html(player_html)

    return league


def parse_transactions_html(html):
    global transaction_tooltips

    transactions = []

    soup = BeautifulSoup(html, 'html.parser')
    page_data = str(soup.find(id='page-data').contents[0])
    json_value = '{%s}' % (page_data.split('{', 1)[1].rsplit('}', 1)[0],)
    transaction_tooltips = json.loads(json_value)['tooltips']

    rows = soup.find_all('div', class_=constants.list_group_item_text_class)
    for row in rows:
        transaction = extract_transaction_info_from_row(row)
        if transaction.datetime.year == constants.current_year and transaction.type in ['Added', 'Claimed']:
            transaction.amount = transaction.amount if transaction.amount else 0
            transactions.append(transaction)

    return transactions


def convert_timezone_to_offset(time_str):
    tz_map = {'EDT': '-0400', 'EST': '-0500'}  # These are the only ones the fleaflicker is known to use
    tz_str = time_str[time_str.rindex(' ') + 1:]
    return time_str.replace(tz_str, tz_map[tz_str])


def extract_transaction_info_from_row(row):
    # Should be strictly focused on getting the information from the HTML. Transformations go elsewhere.
    transaction = gwjffl.Transaction()

    transaction.type = row.find('div', class_="player").previous_sibling.strip()

    span_date = row.find('span', class_=constants.relative_date_class)
    transaction_tooltip = [item for item in transaction_tooltips if span_date['id'] in item["ids"]][0]['contents']
    datetime_str = BeautifulSoup(transaction_tooltip, 'html.parser').text
    converted_datetime_str = convert_timezone_to_offset(datetime_str)
    transaction.datetime = datetime.strptime(converted_datetime_str, '%a %m/%d/%y %I:%M %p %z')

    r = re.compile('\(\$\d+\)')
    t = row.find(string=r)
    transaction.amount = int(t.strip()[2:-1]) if t else None

    return transaction


def calculate_player_values(league):
    i = 0
    for team_id in league.teams:
        i += 1
        print("%d. Calculating player values for team_id: %s" % (i, team_id))
        team = league.teams[team_id]

        for player in team.roster:
            print("%d. Calculating value for player: %s (%d transactions)" % (i, player.name, len(player.transactions)))
            if player.keeper_status == constants.ineligible_label:
                player.peak_price = 999
                player.last_price = 999
            elif len(player.transactions) > 0:
                player.peak_price = calculate_peak_amount(player.transactions)
                # print(player.peak_price)
                player.last_price = calculate_last_amount(player.transactions)
                # print(player.last_price)

    return league


def calculate_last_amount(transactions):
    sorted_by_date = sorted(transactions, key=lambda k: k.datetime, reverse=True)
    for transaction in sorted_by_date:
        if transaction.amount is not None:
            return transaction.amount


def calculate_peak_amount(transactions):
    peak_amount = None
    for transaction in transactions:
        if transaction.amount is not None:
            if peak_amount is None or transaction.amount > peak_amount:
                peak_amount = transaction.amount
    return peak_amount
