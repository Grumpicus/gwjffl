from collections import OrderedDict

from bs4 import BeautifulSoup

import classes
import constants
from jsonstore import read_json_from_file, write_json_to_file


def parse_standings(html):
    teams = []
    soup = BeautifulSoup(html)
    page_data = soup.find(id='page-data')  # unused for now
    rows = soup.find_all('tr', class_=constants.cell_row_class)
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
        if constants.text_error_class in css_classes:
            s['style'] = '%s %s' % (constants.team_notes_style_default, constants.text_error_style)
            s['title'] = constants.team_notes[(constants.text_error_style, s.string)]
    return ''.join(str(s) for s in rs)


def extract_team_info_from_row(row):
    #print(row)
    team = classes.Team()

    td_div_rank = row.contents[0]
    team.div_rank = int(td_div_rank.text)

    div_league_name = row.find('div', class_=constants.league_name_class)
    team.icon = '' if div_league_name.find('img') is None else '<img src="%s">' % div_league_name.find('img')['src']
    a_team_info = div_league_name.find('a')
    team.name = a_team_info.text
    team.url = '%s%s' % (constants.fleaflicker_url, a_team_info['href'])
    start = team.url.find(constants.team_id_param) + len(constants.team_id_param)
    team.id = int(team.url[start:])
    team.html_notes = parse_bs4_result_set_into_team_html_notes(
        div_league_name.parent.find_all('span', class_=constants.tt_content_class))
    team.trophy = div_league_name.find(class_=constants.icon_trophy_class) is not None

    a_user_name = row.find('a', class_=constants.user_name_class)
    team.username = a_user_name.text
    team.inactive = constants.inactive_class in a_user_name['class']

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


def parse_scores(html):
    soup = BeautifulSoup(html)
    scores = []
    for i in range(1, 7):
        score = get_game_info(i, soup)
        if score is not None:
            scores.append(score)
    return scores


def get_game_info(game_number, soup):
    team1_row = soup.find(id=constants.scoreboard_ids['game%d_team1_id' % game_number])
    team2_row = soup.find(id=constants.scoreboard_ids['game%d_team2_id' % game_number])
    game_link_row = soup.find(id=constants.scoreboard_ids['game%d_box_link_id' % game_number])
    if team1_row and team2_row and game_link_row:
        return classes.Game(get_team_info(team1_row), get_team_info(team2_row), get_game_link(game_link_row))
    else:
        return None


def get_team_info(row):
    #print(row)
    team_info = row.find('a')
    start = team_info['href'].find(constants.team_id_param) + len(constants.team_id_param)
    end = team_info['href'].find('&', start)
    team_id = int(team_info['href'][start:None if end == -1 else end])
    score = float(row.find('td', class_='right').text)
    return team_id, score


def get_game_link(row):
    return '%s%s' % (constants.fleaflicker_url, row.find('a')['href'])


def extract_pro_data(pro_league, current_week):
    pro_data = read_json_from_file(constants.pro_data_storage_path)
    pro_data = pro_data if pro_data is not None else {}
    #print(pro_data)
    i = 0
    max_pf = -1
    for x in pro_league.teams:
        if current_week <= 14:
            if pro_league.teams[x].div_rank == 1:
                i += 1
                division_ref = 'div%s' % i
                pro_data[division_ref] = pro_league.teams[x].name
            if pro_league.teams[x].rank == 1:
                pro_data['number_one'] = pro_league.teams[x].name
            if pro_league.teams[x].points_for > max_pf:
                max_pf = pro_league.teams[x].points_for
                if 'regular_season_most_points' not in pro_data:
                    pro_data['regular_season_most_points'] = {}
                pro_data['regular_season_most_points']['team'] = pro_league.teams[x].name
                pro_data['regular_season_most_points']['points'] = pro_league.teams[x].points_for
        elif current_week == 17:
            if pro_league.teams[x].rank == 1:
                pro_data['first'] = pro_league.teams[x].name
            if pro_league.teams[x].rank == 2:
                pro_data['second'] = pro_league.teams[x].name
            if pro_league.teams[x].rank == 3:
                pro_data['third'] = pro_league.teams[x].name
            pro_data['consolation_champ'] = 'Leap\'s Peeps'  # TODO: Parse the playoff bracket

    if current_week <= 14:
        highest_score = 'regular_season_highest_score'
    else:
        highest_score = 'postseason_highest_score'
    if pro_data.get(highest_score, None) is None:
        pro_data[highest_score] = {'points': 0, 'team': None, 'week': None}
    for x in pro_league.results:
        if x.team1_score > pro_data[highest_score]['points']:
            pro_data[highest_score]['points'] = x.team1_score
            pro_data[highest_score]['team'] = pro_league.teams[x.team1_id].name
            pro_data[highest_score]['week'] = current_week - 1
        if x.team2_score > pro_data[highest_score]['points']:
            pro_data[highest_score]['points'] = x.team2_score
            pro_data[highest_score]['team'] = pro_league.teams[x.team2_id].name
            pro_data[highest_score]['week'] = current_week - 1

    write_json_to_file(constants.pro_data_storage_path, pro_data)
    return pro_data


def parse_nfl_html(html):
    soup = BeautifulSoup(html)
    #print(soup)
    schedule_data = soup.find('div', class_=constants.nfl_schedules_div_class)
    #print(schedule_data.prettify())

    nfl_data = classes.NFL_Week(constants.current_week)
    nfl_data.source = constants.nfl_schedule_url_template % (constants.current_year, constants.current_week)

    byes = schedule_data.find('span', class_=constants.nfl_schedules_header_byes_span_class)
    bye_teams = byes.find('span', class_=constants.nfl_bye_team_span_class)
    nfl_data.byes = 'None' if bye_teams is None else bye_teams.get_text("", strip=True)
    nfl_data.dates = schedule_data.find('div', class_=constants.nfl_schedules_list_date_div_class).contents[0]

    gotw = schedule_data.find('div', id=constants.nfl_schedules_centerpiece_div_id)
    nfl_data.gotw['label'] = gotw.find('h5').text
    nfl_data.gotw['title'] = gotw.find('h2').text
    nfl_data.gotw['text'] = gotw.find('p').text

    schedules_table = schedule_data.find('ul', class_=constants.nfl_schedules_table_ul_class)
    first_li = schedules_table.find('li')
    nfl_data.first_date = first_li.find('span')
    for sibling in first_li.find_next_siblings('li'):
        # print(sibling)
        if 'schedules-list-date' in sibling['class']:
            break
        else:
            matchup = classes.NFL_Game()
            matchup.time = sibling.find('div', class_='list-matchup-row-time').get_text(" ", strip=True)
            matchup.teams = sibling.find('div', class_='list-matchup-row-team').get_text(" ", strip=True)
            nfl_data.matchups.append(matchup)

    return nfl_data
