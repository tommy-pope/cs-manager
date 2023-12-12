from .team_information import TeamInformation


class Team:
    def __init__(self, team_information: TeamInformation) -> None:
        self.info = team_information
        
        self.events = []
        self.past_events = []
