import json
import constants


def extract_pro_data(pro_league, current_week):
    pro_data = read_json_from_file(constants.json_storage_path)
    i = 0
    max_pf = 0
    for x in pro_league.teams:
        if pro_league.teams[x].div_rank == 1:
            i += 1
            ref = 'div%s' % i
            pro_data[ref] = pro_league.teams[x].name
        if pro_league.teams[x].rank == 1:
            pro_data['number_one'] = pro_league.teams[x].name
        if pro_league.teams[x].points_for > max_pf:
            max_pf = pro_league.teams[x].points_for
            pro_data['regular_season_most_points']['team'] = pro_league.teams[x].name
            pro_data['regular_season_most_points']['points'] = pro_league.teams[x].points_for

    for x in pro_league.results:
        if x.team1_score > pro_data['regular_season_highest_score']['points']:
            pro_data['regular_season_highest_score']['points'] = x.team1_score
            pro_data['regular_season_highest_score']['team'] = pro_league.teams[x.team1_id]
            pro_data['regular_season_highest_score']['week'] = current_week
        if x.team2_score > pro_data['regular_season_highest_score']['points']:
            pro_data['regular_season_highest_score']['points'] = x.team2_score
            pro_data['regular_season_highest_score']['team'] = pro_league.teams[x.team2_id]
            pro_data['regular_season_highest_score']['week'] = current_week

    write_json_to_file(constants.json_storage_path, pro_data)
    return pro_data


def read_json_from_file(filename):
    json_data = open(filename).read()
    data = None
    if json_data:
        data = json.loads(json_data)
    return data


def write_json_to_file(filename, data):
    with open(filename, 'w') as outfile:
        json.dump(data, outfile)
    return