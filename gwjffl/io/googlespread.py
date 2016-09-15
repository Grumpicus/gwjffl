import gspread
from oauth2client.service_account import ServiceAccountCredentials

from gwjffl import constants


SCOPE = ['https://spreadsheets.google.com/feeds']
CLIENT_SECRET_FILE = '../config/gwjffl-secret.json'


def get_credentials():
    return ServiceAccountCredentials.from_json_keyfile_name(CLIENT_SECRET_FILE, SCOPE)


def get_col_num_from_letter(worksheet, letter):
    return worksheet.get_int_addr(letter + '1')[1]


def convert_position_to_sort_index(position):
    pos_map = {'QB': 1, 'RB': 2, 'WR': 3, 'TE': 4, 'K': 5, 'D/ST': 6}
    return pos_map[position]


def write_keeper_to_spreadsheet(keeper_league):
    credentials = get_credentials()
    gc = gspread.authorize(credentials)
    # https://docs.google.com/spreadsheets/d/102Qc780UZqG7cfpgOJ2KuElOe3dnD0DaSa0oaKGEFA0/edit#gid=1643976956
    worksheet = gc.open_by_key(constants.keeper_spreadsheet_id).worksheet(constants.keeper_worksheet_id)

    teams = keeper_league.teams

    name_col = get_col_num_from_letter(worksheet, 'A')
    acquired_col = get_col_num_from_letter(worksheet, 'C')
    peak_col = get_col_num_from_letter(worksheet, 'D')
    final_col = get_col_num_from_letter(worksheet, 'E')
    season_total_col = get_col_num_from_letter(worksheet, 'T')
    season_avg_col = get_col_num_from_letter(worksheet, 'V')
    player_url_col = get_col_num_from_letter(worksheet, 'AI')

    default_peak_value_template = '=if(' \
                                  'and(' \
                                  'A{0}<>"",A{1}<>"",' \
                                  'C{0}<>"Keeper",C{0}<>"Drafted",C{0}<>"Cut",C{0}<>"Traded For"' \
                                  '),' \
                                  '-1,"")'

    team_limit = 23

    row_num = 1
    for team_id in teams:
        team = teams[team_id]
        row_num += 1
        team_count = 1

        print(row_num, team.name)
        worksheet.update_cell(row_num, 1, team.name)

        sorted_roster = sorted(team.roster, key=lambda k: (convert_position_to_sort_index(k.position), k.name))
        # print(sorted_roster)

        for player in sorted_roster:
            row_num += 1
            team_count += 1
            cell_list = []

            cell = worksheet.cell(row_num, name_col)
            cell.value = player.name
            cell_list.append(cell)

            cell = worksheet.cell(row_num, acquired_col)
            cell.value = player.keeper_status
            cell_list.append(cell)

            cell = worksheet.cell(row_num, peak_col)
            if player.peak_price is not None and player.peak_price != player.last_price:
                cell.value = player.peak_price
            else:
                cell.value = ''
            cell_list.append(cell)

            default_peak_value = default_peak_value_template.format(row_num, row_num - 1)

            cell = worksheet.cell(row_num, final_col)
            if player.last_price is not None:
                cell.value = player.last_price
            else:
                cell.value = default_peak_value
            cell_list.append(cell)

            cell = worksheet.cell(row_num, season_total_col)
            cell.value = player.season_total
            cell_list.append(cell)

            cell = worksheet.cell(row_num, season_avg_col)
            cell.value = player.season_avg
            cell_list.append(cell)

            cell = worksheet.cell(row_num, player_url_col)
            cell.value = player.url
            cell_list.append(cell)

            print(row_num, player.name, player.keeper_status, player.peak_price, player.last_price, player.url)
            worksheet.update_cells(cell_list)

        while team_count % team_limit > 0:
            row_num += 1
            print(row_num)
            worksheet.update_cell(row_num, name_col, "")
            worksheet.update_cell(row_num, acquired_col, "")
            worksheet.update_cell(row_num, final_col, default_peak_value_template.format(row_num, row_num - 1))
            team_count += 1