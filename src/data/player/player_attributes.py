class PlayerAttributes:
    def __init__(
        self,
        rifle: float = 0.0,
        pistol: float = 0.0,
        awp: float = 0.0,
        positioning: float = 0.0,
        clutch: float = 0.0,
        consistency: float = 0.0,
        is_awper: bool = False,
    ) -> None:
        self.rifle = rifle
        self.pistol = pistol
        self.awp = awp
        self.positioning = positioning
        self.clutch = clutch
        self.consistency = consistency
        self.overall = round((self.rifle + self.pistol + self.awp + self.positioning + self.clutch + self.consistency) / 6, 2)

        self.is_awper = is_awper
