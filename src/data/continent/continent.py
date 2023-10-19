class Continent:
    def __init__(self, continent_name: str, short_name: str, continent_rep: float) -> None:
        self.name = continent_name
        self.sname = short_name
        self.rep = continent_rep
        self.nations = {}
        self.teams = []

        self.nation_distribution = {}
    
    def calculate_nation_distribution(self) -> None:
        # normalize, calculate percentage using power function, normalize weights, convert weights to percentages
        nations = [nation for nation in self.nations.values()]

        normalized_reps = [value.rep / 100 for value in nations]
        weights = [value**3 for value in normalized_reps]
        normalized_weights = [weight / sum(weights) for weight in weights]
        percentages = [weight * 100 for weight in normalized_weights]

        for idx in range(len(percentages)):
            self.nation_distribution[nations[idx].sname] = percentages[idx]
    
    def calculate_team_rankings(self) -> None:
        self.teams.sort(key=lambda x: x.info.elo, reverse=True)
