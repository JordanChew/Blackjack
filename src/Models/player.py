from Models.hand import Hand
from Models.deck import Deck

class Player():
    def __init__(self) -> None:
        self.hands = []
        self.numHands = 0
        self.balance = 100
        self.bets = []

    def clearHands(self) -> None:
        self.hands = []

    def split(self, deck: Deck, handIndex: int) -> None:
        self.hands.append(Hand())
        self.hands[-1].cards.append(self.hands[handIndex].cards.pop())
        self.hands[handIndex].total = int(self.hands[handIndex].total / 2)
        self.hands[-1].total = int(self.hands[handIndex].total)

        self.hands[handIndex].hit(deck)
        self.hands[-1].hit(deck)

        self.bets.append(self.bets[handIndex])

    def displayHands(self) -> None:
        print()
        for handIndex, hand in enumerate(self.hands):
            print("Hand " + str(handIndex + 1) + ": " + str(hand) + " = " + str(hand.total))