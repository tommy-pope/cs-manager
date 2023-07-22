from .player_attributes import PlayerAttributes
from .player_information import PlayerInformation


class Player:
    def __init__(
        self, player_information: PlayerInformation, player_attributes: PlayerAttributes
    ) -> None:
        self.info = player_information
        self.attributes = player_attributes
