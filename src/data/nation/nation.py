class Nation:
    def __init__(self, nation_name: str, short_name: str, nation_rep: float, nation_continent: str) -> None:
        self.name = nation_name
        self.sname = short_name
        self.rep = nation_rep
        self.continent = nation_continent
        self.rankings = {}
        
