class League(object):
    def __init__(self, league_id, league_name):
        self.id = league_id
        self.name = league_name
        self.teams = None
        self.results = []
        self.schedule = []
        self.div_record = ''
        self.div_rank = 0


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


class Game(object):
    def __init__(self, team1, team2, link):
        self.team1_id = int(team1[0])
        self.team1_score = float(team1[1])
        self.team2_id = int(team2[0])
        self.team2_score = float(team2[1])
        self.highest_rank = 0
        self.box_link = link