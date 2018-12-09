class Week(object):
    def __init__(self, week):
        self.week = week
        self.byes = ''
        self.dates = ''
        self.gotw = {}
        self.early = []
        self.later = []
        self.first_date = ''
        self.source = ''


class Matchup(object):
    def __init__(self):
        self.date = ''
        self.time = ''
        self.teams = ''
        self.tv = ''
