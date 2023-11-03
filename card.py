class Card:
    def __init__(self, suit: str, rank: str) -> None:
        self.suit: str = suit
        self.rank: str = rank
        self.value: int = self._assign_value()

    def _assign_value(self) -> int:
        if self.rank.isdigit():
            return int(self.rank)
        elif self.rank in ['10', 'Jack', 'Queen', 'King']:
            return 10
        elif self.rank == 'Ace':
            return 11

    def change_ace_value_to_one(self) -> None:
        if self.rank == 'Ace':
            self.value = 1

    def change_ace_value_to_eleven(self) -> None:
        if self.rank == 'Ace':
            self.value = 11

    def __str__(self) -> str:
        return f"{self.rank} of {self.suit}"

    def __repr__(self) -> str:
        return f"{self.rank} of {self.suit}"
