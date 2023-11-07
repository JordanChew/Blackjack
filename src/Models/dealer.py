class Dealer():
    def __init__(self) -> None:
        self.hand = None

    def displayHandHidden(self) -> None:
        lastCard = self.hand.cards[-1]
        self.hand.cards[-1] = "?"
        print("\nDealer: " + str(self.hand))
        self.hand.cards[-1] = lastCard

    def displayHandFull(self) -> None:
        print("\nDealer: " + str(self.hand) + " = " + str(self.hand.total))