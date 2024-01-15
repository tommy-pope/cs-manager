class PlayerContract:
    def __init__(self, team, salary: float, signed_date: list, expiration_date: list):
        self.team = team

        self.salary = salary
        self.signed_date = signed_date
        self.expiration_date = expiration_date  