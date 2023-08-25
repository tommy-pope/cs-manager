class Continent:
    def __init__(self, continent_name: str, short_name: str, continent_rep: float) -> None:
        self.name = continent_name
        self.sname = short_name
        self.rep = continent_rep
        self.nations = []
        self.rankings = {}