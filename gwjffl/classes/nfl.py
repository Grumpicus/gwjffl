class Week(object):
    def __init__(self, week):
        self.week = week
        self.byes = ''
        self.dates = ''
        self.gotw = {}
        self.matchups = []
        self.first_date = ''
        self.source = ''


class Matchup(object):
    def __init__(self):
        self.time = None
        self.teams = ''