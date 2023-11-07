from Models.card import Card
import random

# implemented as a queue ADT
class Deck:
    def __init__(self) -> None:
        self.numCards = 52 * 8
        self.cards = self.newDeck()
        self.shuffleDeck()

    def newDeck(self) -> list:
        faces = ["ace"] + list(range(2, 10)) + ["jack", "queen", "king"]
        suits = ["spades", "hearts", "clubs", "diamonds"]

        deck = []
        for face in faces:
            for suit in suits:
                if face in ["jack", "queen", "king"]:
                    value = 10
                elif face == "ace":
                    value = 11
                else:
                    value = face
                deck.append(Card(str(face), suit, value))
        deck = deck * 8

        return deck

    def shuffleDeck(self) -> None:
        random.shuffle(self.cards)

    def drawCard(self) -> Card:
        self.numCards -= 1
        return self.cards.pop(0)