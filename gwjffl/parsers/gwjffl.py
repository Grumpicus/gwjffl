from collections import OrderedDict
import json

from bs4 import BeautifulSoup

from gwjffl import constants
from gwjffl.classes import gwjffl
from gwjffl.io.jsonstore import pickle_json_to_file, unpickle_json_from_file
from gwjffl.io.web import get_league_html


def parse_standings(html):
    global tooltips
    teams = []
    soup = BeautifulSoup(html, 'html.parser')
    page_data = str(soup.find(id='page-data').contents[0])
    json_value = '{%s}' % (page_data.split('{', 1)[1].rsplit('}', 1)[0],)
    tooltips = json.loads(json_value)['tooltips']
    rows = soup.find_all('tr', id=constants.row_partial_id)
    for row in rows:
        teams.append(extract_team_info_from_row(row))

    sorted_teams = OrderedDict((team.id, team) for team in sorted(teams, key=lambda team: team.rank))

    return sorted_teams


def parse_bs4_result_set_into_team_html_notes(rs):
    for s in rs:
        css_classes = s['class']
        del s['class']
        del s['id']
        if constants.text_success_class in css_classes:
            s['style'] = '%s %s' % (constants.team_notes_style_default, constants.text_success_style)
            s['title'] = constants.team_notes[(constants.text_success_style, s.string)]
        if constants.text_eliminated_class in css_classes:
            s['style'] = '%s %s' % (constants.team_notes_style_default, constants.text_error_style)
            s['title'] = constants.team_notes[(constants.text_error_style, s.string)]
    return ''.join(str(s) for s in rs)


def extract_team_info_from_row(row):
    # print(row)
    team = gwjffl.Team()

    td_div_rank = row.contents[0]
    team.div_rank = int(td_div_rank.text)

    div_league_name = row.find('div', class_=constants.league_name_class)
    team.icon = '' if div_league_name.find('img') is None else '<img src="%s">' % div_league_name.find('img')['src']
    a_team_info = div_league_name.find('a')
    team.name = a_team_info.text
    team.url = '%s%s' % (constants.fleaflicker_url, a_team_info['href'])
    start = team.url.find(constants.team_id_param) + len(constants.team_id_param)
    end = team.url.find('?', start)
    team.id = int(team.url[start:None if end == -1 else end])
    team.html_notes = parse_bs4_result_set_into_team_html_notes(
        div_league_name.parent.find_all('span', class_=constants.tt_content_class))
    team.trophy = div_league_name.find(class_=constants.icon_trophy_class) is not None

    a_user_name = row.find('a', class_=constants.user_name_class)
    team.username = a_user_name.text
    team.inactive = constants.inactive_class in a_user_name['class']
    last_sign_in_tooltip = [item for item in tooltips if a_user_name['id'] in item["ids"]][0]['contents']
    team.last_sign_in = BeautifulSoup(last_sign_in_tooltip, 'html.parser').find('span', class_='relative-date').text

    second_td_horizontal_spacer = row.find_all('td', class_=constants.horizontal_spacer_class)[1]
    td_wins = second_td_horizontal_spacer.next_sibling
    team.wins = int(td_wins.text if td_wins.text != "" else 0)
    td_losses = td_wins.next_sibling
    team.losses = int(td_losses.text if td_losses.text != "" else 0)
    td_div_record = td_losses.next_sibling.next_sibling.next_sibling
    team.div_record = td_div_record.text

    third_td_horizontal_spacer = row.find_all('td', class_=constants.horizontal_spacer_class)[2]
    td_streak = third_td_horizontal_spacer.previous_sibling
    team.streak = td_streak.text
    td_points_for = third_td_horizontal_spacer.next_sibling
    team.points_for = float(td_points_for.text.replace(',', '') if td_points_for.text != "" else 0)
    td_points_against = td_points_for.next_sibling.next_sibling
    team.points_against = float(td_points_against.text.replace(',', '') if td_points_against.text != "" else 0)

    fourth_td_horizontal_spacer = row.find_all('td', class_=constants.horizontal_spacer_class)[3]
    td_rank = fourth_td_horizontal_spacer.next_sibling
    team.rank = int(td_rank.text if td_rank.text != "" else 0)

    return team


def parse_schedule(html):
    soup = BeautifulSoup(html, 'html.parser')
    games = []
    for i in range(1, 7):
        game = get_game_info(i, soup)
        if game is not None:
            games.append(game)
    return games


def parse_scores(html):
    soup = BeautifulSoup(html, 'html.parser')
    scores = []

    top_scores_description_list = soup.find(id='left-container').find('dl', class_='panel-body')

    top_scores = top_scores_description_list.children

    for dt, dd in zip(top_scores, top_scores):
        a = dt.find('a')
        team_id = int(extract_team_id(a))
        score = float(dd.string)
        scores.append(gwjffl.Result(team_id, score))

    return scores


def get_game_info(game_number, soup):
    team1_row = soup.find(id=constants.scoreboard_ids['game%d_team1_id' % game_number])
    team2_row = soup.find(id=constants.scoreboard_ids['game%d_team2_id' % game_number])
    game_link_row = soup.find(id=constants.scoreboard_ids['game%d_box_link_id' % game_number])
    if team1_row and team2_row and game_link_row:
        return gwjffl.Game(get_result(team1_row), get_result(team2_row), get_game_link(game_link_row))
    else:
        return None


def extract_team_id(a):
    start = a['href'].find(constants.team_id_param) + len(constants.team_id_param)
    end = a['href'].find('?', start)
    team_id = int(a['href'][start:None if end == -1 else end])
    return team_id


def get_result(row):
    a = row.find('a')
    team_id = extract_team_id(a)
    score = float(row.find('td', class_='right').text)
    return gwjffl.Result(team_id, score)


def get_game_link(row):
    return '%s%s' % (constants.fleaflicker_url, row.find('a')['href'])


def get_consolation_winner(league, week):
    html = get_league_html(league, week, constants.consolation_label)
    soup = BeautifulSoup(html, 'html.parser')
    bracket_table = soup.find('table', class_='playoff-bracket')
    winner = bracket_table.find_all('tr')[8]
    a = winner.find('a')
    team_id = extract_team_id(a)
    return league.teams[team_id]


def extract_pro_data(pro_league, current_week):
    pro_data = unpickle_json_from_file(constants.pro_data_storage_path)
    pro_data = pro_data if pro_data is not None else {}
    # print(pro_data)
    i = 0
    max_pf = -1
    for team_id in pro_league.teams:
        if current_week <= 14:
            if pro_league.teams[team_id].div_rank == 1:
                i += 1
                division_ref = 'div%s' % i
                award = gwjffl.Award('Division Winner')  # TODO: constant
                award.value = 15  # TODO: externalize
                award.team = pro_league.teams[team_id]
                pro_data[division_ref] = award
            if pro_league.teams[team_id].rank == 1:
                award = gwjffl.Award('#1 Overall')  # TODO: constant
                award.value = 10  # TODO: externalize
                award.team = pro_league.teams[team_id]
                pro_data['number_one'] = award
            if pro_league.teams[team_id].points_for > max_pf:
                max_pf = pro_league.teams[team_id].points_for
                if 'regular_season_most_points' not in pro_data:
                    pro_data['regular_season_most_points'] = {}
                award = gwjffl.Award('Most total points')  # TODO: constant
                award.value = 25  # TODO: externalize
                award.team = pro_league.teams[team_id]
                award.points = pro_league.teams[team_id].points_for
                pro_data['regular_season_most_points'] = award
        elif current_week == 17:
            if pro_league.teams[team_id].rank == 1:
                award = gwjffl.Award('1st place')  # TODO: constant
                award.value = 100  # TODO: externalize
                award.team = pro_league.teams[team_id]
                pro_data['first'] = award
            if pro_league.teams[team_id].rank == 2:
                award = gwjffl.Award('2nd place')  # TODO: constant
                award.value = 50  # TODO: externalize
                award.team = pro_league.teams[team_id]
                pro_data['second'] = award
            if pro_league.teams[team_id].rank == 3:
                award = gwjffl.Award('3rd place')  # TODO: constant
                award.value = 25  # TODO: externalize
                award.team = pro_league.teams[team_id]
                pro_data['third'] = award

    if current_week == 17:
        award = gwjffl.Award('Consolation Champ')  # TODO: constant
        award.value = 15  # TODO: externalize
        award.team = get_consolation_winner(pro_league, current_week)
        pro_data['consolation_champ'] = award

    award = gwjffl.Award('Highest single-week team total')
    if current_week <= 14:
        highest_score = 'regular_season_highest_score'  # TODO: constant
        award.value = 10  # TODO: externalize
    else:
        highest_score = 'postseason_highest_score'  # TODO: constant
        award.value = 5  # TODO: externalize
    if pro_data.get(highest_score, None) is None:
        pro_data[highest_score] = award
    for result in pro_league.scores:
        if result.score > pro_data[highest_score].points:
            pro_data[highest_score].points = result.score
            pro_data[highest_score].team = pro_league.teams[result.team_id]
            pro_data[highest_score].week = current_week - 1

    pickle_json_to_file(constants.pro_data_storage_path, pro_data)
    return pro_data