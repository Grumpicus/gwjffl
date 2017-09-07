from bs4 import BeautifulSoup

from gwjffl import constants
from gwjffl.classes import nfl


def parse_nfl_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    schedule_data = soup.find('div', class_=constants.nfl_schedules_div_class)

    nfl_data = nfl.Week(constants.current_week)
    nfl_data.source = constants.nfl_schedule_url_template % (constants.current_year, constants.current_week)

    byes = schedule_data.find('span', class_=constants.nfl_schedules_header_byes_span_class)
    bye_teams = byes.find('span', class_=constants.nfl_bye_team_span_class)
    nfl_data.byes = 'None' if bye_teams is None else bye_teams.get_text("", strip=True).replace(",", ", ")
    # nfl_data.dates = schedule_data.find('div', class_=constants.nfl_schedules_list_date_div_class).contents[0]

    schedules_table = schedule_data.find_all('ul', class_=constants.nfl_schedules_table_ul_class)[0]  # Fragile!
    first_li = schedules_table.find('li')
    nfl_data.first_date = first_li.find('span')
    for sibling in first_li.find_next_siblings('li'):
        if 'schedules-list-date' in sibling['class']:
            break
        else:
            matchup = nfl.Matchup()
            matchup.time = sibling.find('div', class_='list-matchup-row-time').get_text(" ", strip=True)
            matchup.teams = sibling.find('div', class_='list-matchup-row-team').get_text(" ", strip=True)
            nfl_data.matchups.append(matchup)

    return nfl_data