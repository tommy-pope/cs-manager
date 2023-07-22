class PlayerAttributes:
    def __init__(
        self,
        rifle: float = 0.0,
        pistol: float = 0.0,
        awp: float = 0.0,
        positioning: float = 0.0,
        clutch: float = 0.0,
        consistency: float = 0.0,
    ) -> None:
        self.rifle = rifle
        self.pistol = pistol
        self.awp = awp
        self.positioning = positioning
        self.clutch = clutch
        self.consistency = consistency

        self.is_awper = False
