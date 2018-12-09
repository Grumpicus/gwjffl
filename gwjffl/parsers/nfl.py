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

    schedules_table = schedule_data.find_all('ul', class_=constants.nfl_schedules_table_ul_class)[
        1]  # Second one on the page. Fragile!
    first_li = schedules_table.find('li')
    # nfl_data.first_date = first_li.find('span')
    current_date = first_li.find('span')
    schedule_target = nfl_data.early
    for sibling in first_li.find_next_siblings('li'):
        if constants.nfl_schedules_list_date_div_class in sibling['class']:
            current_date = sibling.find('span')
            schedule_target = nfl_data.later
        else:
            matchup = nfl.Matchup()
            matchup.date = current_date
            matchup.time = sibling.find('div', class_=constants.nfl_list_matchup_row_time_div_class).get_text(" ",
                                                                                                              strip=True)
            nflicon = sibling.find('div', class_=constants.nfl_list_matchup_row_tv_div_class).find('span',
                                                                                                   class_='nflicon')
            matchup.tv = nflicon.get('title') if nflicon else None
            matchup.teams = sibling.find('div', class_=constants.nfl_list_matchup_row_team_div_class).get_text(" ",
                                                                                                               strip=True)
            schedule_target.append(matchup)

    return nfl_data
