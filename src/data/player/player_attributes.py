class PlayerAttributes:
    def __init__(
        self,
        rifle: float = 0.0,
        pistol: float = 0.0,
        awp: float = 0.0,
        positioning: float = 0.0,
        clutch: float = 0.0,
        consistency: float = 0.0,
        overall: float = 0.0,
        potential: float = 0.0,
        is_awper: bool = False,
    ) -> None:
        self.rifle = rifle
        self.pistol = pistol
        self.awp = awp
        self.positioning = positioning
        self.clutch = clutch
        self.consistency = consistency
        self.overall = overall
        self.potential = potential

        self.is_awper = is_awper
