from .team_information import TeamInformation


class Team:
    def __init__(self, team_information: TeamInformation) -> None:
        self.info = team_information
        
        self.events = []
        self.past_events = []

    def update_finance_weights(self):
        test_salary_budget = round((self.info.budget * self.info.salary_split) / 12)

        for player in self.info.players:
            test_salary_budget -= player.contract.salary

        if test_salary_budget < 0:
            if self.info.salary_split < 1:
                self.info.salary_split += .1
                self.info.transfer_split -= .1

                self.update_finance_weights()

    def update_budget(self):
        self.update_finance_weights()

        self.info.transfer_budget = round(self.info.budget * self.info.transfer_split)
        self.info.salary_budget = round((self.info.budget * self.info.salary_split) / 12)
        self.info.leftover_salary_budget = self.info.salary_budget

        if self.info.more_transfer_budget:
            self.info.leftover_transfer_budget = self.info.transfer_budget
            self.info.more_transfer_budget = False

        # calculate leftover salary budget
        for player in self.info.players:
            self.info.leftover_salary_budget -= player.contract.salary