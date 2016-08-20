class League(object):
    def __init__(self, league_id, league_name):
        self.id = league_id
        self.name = league_name
        self.teams = None
        self.results = []
        self.schedule = []
        self.div_record = ''
        self.div_rank = 0
        self.scores = []


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
        self.prev_rank = 0
        self.html_notes = ''
        self.trophy = False
        self.inactive = False
        self.last_sign_in = ''
        self.roster = []


class Game(object):
    def __init__(self, team1_result, team2_result, link):
        self.team1_result = team1_result
        self.team2_result = team2_result
        self.highest_rank = 0
        self.box_link = link


class Result(object):
    def __init__(self, team_id, score):
        self.team_id = team_id
        self.score = score


class Award(object):
    def __init__(self, award_desc):
        self.desc = award_desc
        self.value = 0
        self.team = None
        self.week = None
        self.points = 0


class Player(object):
    def __init__(self):
        self.id = ''
        self.name = ''
        self.position = ''  # unused
        self.team = ''  # unused
        self.season_avg = 0
        self.season_total = 0
        self.acquired_how = ''
        self.acquired_when_year = 0
        self.acquired_when_text = ''
        self.acquired = ''
        self.SEO_id = ''
        self.transactions = []
        self.peak_price = None
        self.last_price = None
        self.url = ''


class Transaction(object):
    def __init__(self):
        self.team = ''
        self.datetime = None
        self.amount = None
        self.type = None
