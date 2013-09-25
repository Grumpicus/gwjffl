__author__ = 'Grumpicus'

import constants


class League(object):
    def __init__(self, league_info, current_week):
        self.id = league_info[0]
        self.name = league_info[1]
        self.url_standings = constants.standings_url % league_info[0]
        self.url_prev_week = constants.scores_url % (league_info[0], current_week - 1)
        self.url_cur_week = constants.scores_url % (league_info[0], current_week)
        self.html_standings = None
        self.html_prev_week = None
        self.html_cur_week = None
        self.teams = []
        self.results = []
        self.schedule = []


class Team(object):
    def __init__(self):
        self.id = None
        self.name = None
        self.url = None
        self.username = None
        self.wins = 0
        self.losses = 0
        self.points_for = 0
        self.points_against = 0
        self.streak = None
        self.rank = 0
