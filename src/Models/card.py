class Card:
    def __init__(self, face: str, suit: str, value: int) -> None:
        self.face = face
        self.suit = suit
        self.value = value

    def __str__(self) -> str:
        return self.face

    def changeAceValue(self) -> None:
        if self.face == "ace" and self.value == 11:
            self.value = 1