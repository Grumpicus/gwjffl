__author__ = 'Grumpicus'

from bs4 import BeautifulSoup

import classes
import constants


def parse_standings(html):
    teams = []
    soup = BeautifulSoup(html)
    rows = soup.find_all('tr', class_='cell-row')
    #print(soup.title.string)
    for row in rows:
        teams.append(extract_team_info_from_row(row))
    teams.sort(key=lambda team: team.rank)
    return teams


def extract_team_info_from_row(row):
    #print(row.prettify())
    team = classes.Team()

    div_league_name = row.find('div', class_='league-name').find('a')
    team.name = div_league_name.text
    team.url = '%s%s' % (constants.fleaflicker_url, div_league_name['href'])
    start = team.url.find('teamId=') + len('teamId=')
    team.id = int(team.url[start:])

    a_user_name = row.find('a', class_='user-name')
    team.username = a_user_name.text

    second_td_horizontal_spacer = row.find_all('td', class_='horizontal-spacer')[1]
    td_wins = second_td_horizontal_spacer.next_sibling
    team.wins = int(td_wins.text)
    #print(team.wins)
    td_losses = td_wins.next_sibling
    team.losses = int(td_losses.text)
    #print(team.losses)

    third_td_horizontal_spacer = row.find_all('td', class_='horizontal-spacer')[2]
    td_streak = third_td_horizontal_spacer.previous_sibling
    team.streak = td_streak.text
    #print(team.streak)
    td_points_for = third_td_horizontal_spacer.next_sibling
    team.points_for = float(td_points_for.text)
    #print(team.points_for)
    td_points_against = td_points_for.next_sibling.next_sibling
    team.points_against = float(td_points_against.text)
    #print(team.points_against)

    fourth_td_horizontal_spacer = row.find_all('td', class_='horizontal-spacer')[3]
    td_rank = fourth_td_horizontal_spacer.next_sibling
    team.rank = int(td_rank.text)
    #print(team.rank)

    return team


def parse_prev_week(html):
    soup = BeautifulSoup(html)
    print(soup.title.string)
    return ''


def parse_cur_week(html):
    soup = BeautifulSoup(html)
    print(soup.title.string)
    return ''