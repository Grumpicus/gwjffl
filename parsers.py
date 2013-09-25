__author__ = 'Grumpicus'

from bs4 import BeautifulSoup

import classes
import constants


def parse_standings(html):
    teams = []
    soup = BeautifulSoup(html)
    rows = soup.find_all('tr', class_=constants.cell_row_class)
    for row in rows:
        teams.append(extract_team_info_from_row(row))
    teams.sort(key=lambda team: team.rank)
    return teams


def extract_team_info_from_row(row):
    #print(row.prettify())
    team = classes.Team()

    a_team_info = row.find('div', class_=constants.league_name_class).find('a')
    team.name = a_team_info.text
    team.url = '%s%s' % (constants.fleaflicker_url, a_team_info['href'])
    start = team.url.find(constants.team_id_param) + len(constants.team_id_param)
    team.id = int(team.url[start:])

    a_user_name = row.find('a', class_=constants.user_name_class)
    team.username = a_user_name.text

    second_td_horizontal_spacer = row.find_all('td', class_=constants.horizontal_spacer_class)[1]
    td_wins = second_td_horizontal_spacer.next_sibling
    team.wins = int(td_wins.text)
    td_losses = td_wins.next_sibling
    team.losses = int(td_losses.text)

    third_td_horizontal_spacer = row.find_all('td', class_=constants.horizontal_spacer_class)[2]
    td_streak = third_td_horizontal_spacer.previous_sibling
    team.streak = td_streak.text
    td_points_for = third_td_horizontal_spacer.next_sibling
    team.points_for = float(td_points_for.text)
    td_points_against = td_points_for.next_sibling.next_sibling
    team.points_against = float(td_points_against.text)

    fourth_td_horizontal_spacer = row.find_all('td', class_=constants.horizontal_spacer_class)[3]
    td_rank = fourth_td_horizontal_spacer.next_sibling
    team.rank = int(td_rank.text)

    return team


def parse_prev_week(html):
    results = []
    #soup = BeautifulSoup(html)
    return results


def parse_cur_week(html):
    schedule = []
    soup = BeautifulSoup(html)

    schedule.append(get_game_info(1, soup))
    schedule.append(get_game_info(2, soup))
    schedule.append(get_game_info(3, soup))
    schedule.append(get_game_info(4, soup))
    schedule.append(get_game_info(5, soup))
    schedule.append(get_game_info(6, soup))

    return schedule


def get_game_info(game_number, soup):
    team1_row = soup.find(id=constants.game_team_ids['game%s_team1_id' % game_number])
    team2_row = soup.find(id=constants.game_team_ids['game%s_team2_id' % game_number])
    return classes.Game(get_team_info(team1_row), get_team_info(team2_row))


def get_team_info(row):
    team_info = row.find('a')
    start = team_info['href'].find(constants.team_id_param) + len(constants.team_id_param)
    team_id = int(team_info['href'][start:])
    team_projected = float(row.find('span', class_=constants.projected_class).text)
    return (team_id, team_projected)