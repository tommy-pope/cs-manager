from ..player.player import Player


class TeamInformation:
    def __init__(
        self, id: int, name: str, reputation: float, players: list, continent, owner_financial_type: str, budget: float
    ) -> None:
        self.id = id
        self.name = name
        self.reputation = reputation
        self.players = players
        self.elo = round(self.reputation * 10)
        self.world_rank = 0
        self.continent = continent

        self.owner_financial_type = owner_financial_type
        self.transfer_split = .2
        self.salary_split = .8

        self.budget = budget
        self.transfer_budget = 0
        self.salary_budget = 0

        self.more_transfer_budget = True

        self.leftover_transfer_budget = 0
        self.leftover_salary_budget = 0