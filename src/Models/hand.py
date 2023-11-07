from Models.deck import Deck
from Models.card import Card

class Hand:
    def __init__(self) -> None:
        self.cards = []
        self.total = 0
        self.hasElevin = False
        self.blackjack = False
        self.twentyone = False
        self.bust = False

    def __str__(self) -> str:
        lstCards = [str(card) for card in self.cards]
        return " ".join(lstCards)

    def hit(self, deck: Deck) -> None:
        card = deck.drawCard()
        self.cards.append(card)
        
        if card.face == "ace":
            self.checkElevin(card)

        self.total += int(card.value)

        self.updateStatus()
        
    def checkElevin(self, card: Card) -> None:
        if self.total > 10:
            card.changeAceValue()
        else:
            self.hasElevin = True

    def updateStatus(self) -> None:
        if self.total == 21:
            if len(self.cards) == 2:
                self.blackjack = True
            else:
                self.twentyone = True
        elif self.total > 21:
            self.bust = True

    def isSplitable(self) -> bool:
        if self.cards[0].value == self.cards[1].value:
            return True
        return False