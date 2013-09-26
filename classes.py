__author__ = 'Grumpicus'

import constants


class League(object):
    def __init__(self, league_info, current_week, sort_index=0):
        self.id = league_info[0]
        self.name = league_info[1]
        self.week = current_week
        self.url_standings = constants.standings_url % league_info[0]
        self.url_prev_week = constants.scores_url % (league_info[0], current_week - 1)
        self.url_cur_week = constants.scores_url % (league_info[0], current_week)
        self.html_standings = ''
        self.html_prev_week = ''
        self.html_cur_week = ''
        self.teams = None
        self.results = []
        self.schedule = []
        self.sort_key = sort_index


class Team(object):
    def __init__(self):
        self.id = 0
        self.name = ''
        self.url = ''
        self.username = ''
        self.wins = 0
        self.losses = 0
        self.points_for = 0
        self.points_against = 0
        self.streak = ''
        self.rank = 0
        self.icon = ''


class Game(object):
    def __init__(self, team1, team2):
        self.team1_id = int(team1[0])
        self.team1_score = float(team1[1])
        self.team2_id = int(team2[0])
        self.team2_score = float(team2[1])
        self.highest_rank = 0