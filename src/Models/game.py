from Models.player import Player
from Models.dealer import Dealer
from Models.hand import Hand
from Models.deck import Deck

class Game:
    def __init__(self) -> None:
        playAgain = True
        self.deck = Deck()
        self.dealer = Dealer()
        self.player = Player()

        while playAgain:
            self.displayIntro()

            self.player.clearHands()
            self.player.numHands = self.getNumHands()
            self.player.bets = self.getBets()

            self.initHands()
            self.deal()

            self.displayTable()
            self.playHands()
            self.simDealer()

            self.outcomes = self.calculateOutcome()
            self.payout = self.calculatePayout()
            self.displayOutcome()
            self.makePayout()

            playAgain = self.askPlayAgain()


    def displayIntro(self) -> None:
        print("\nWelcome To Blackjack!")
        print("Dealer draws to 16, stands on 17")
        print("\nAccount Balance: " + str(self.player.balance))

    def getNumHands(self) -> int:
        try:
            numHands = int(input("\nEnter Number Of Hands: "))
        except ValueError:
            print("\nThat Is Not A Number")
            exit()
        
        if numHands > self.player.balance:
            print("\nCannot Have More Hands Than Remaining Balance")
            exit()
                
        return numHands

    def getBets(self) -> list[int]:
        bets = []
        numBets = 0
        try:
            while numBets < self.player.numHands:
                bets.append(input("Enter Bet Amount For Hand " + str(numBets + 1) + ": "))
                numBets += 1
            bets = [int(bet) for bet in bets]
        except ValueError:
            print("\nA Bet Entered Is Not A Number")
            exit()

        if sum(bets) > self.player.balance:
            print("\nInsuffient Account Funds")
            exit()

        return bets

    def initHands(self) -> None:
        self.dealer.hand = Hand()
        numHands = 0
        while numHands < self.player.numHands:
            self.player.hands.append(Hand())
            numHands += 1

    def deal(self) -> None:
        numCards = 0
        while numCards < 2:
            for hand in self.player.hands:
                hand.hit(self.deck)
            self.dealer.hand.hit(self.deck)
            numCards += 1

    def displayTable(self) -> None:
        print("\n-----------------------------------")
        self.dealer.displayHandHidden()
        self.player.displayHands()

    def playHands(self) -> None:
        for handID, hand in enumerate(self.player.hands):
            if hand.isSplitable() and self.player.balance >= self.player.bets[handID]:
                split = input("\nHand " + str(handID + 1) + "Split (y/n): ")
                if split.lower() == "y":
                    self.player.split(self.deck, handID)
                    self.displayTable()
            choice = "h"
            while not (hand.blackjack or hand.twentyone or hand.bust) and choice != "s":
                choice = input("\nHand " + str(handID + 1) + " Hit Or Stand (h/s): ")
                if choice.lower() == "h":
                    hand.hit(self.deck)
                self.displayTable()

    def simDealer(self) -> None:
        while self.dealer.hand.total < 17:
            self.dealer.hand.hit(self.deck)

    def calculateOutcome(self) -> list[str]:
        outcomes = []
        for hand in self.player.hands:
            if hand.bust or (hand.total < self.dealer.hand.total and not self.dealer.hand.bust):
                outcomes.append("Loss")
            elif hand.total > self.dealer.hand.total or self.dealer.hand.bust:
                if hand.blackjack:
                    outcomes.append("Blackjack")
                else:
                    outcomes.append("Win")
            else:
                outcomes.append("Push")

        return outcomes
    
    def displayOutcome(self) -> None:
        print("\n-----------------------------------")
        self.dealer.displayHandFull()
        self.player.displayHands()
        print()
        if self.dealer.hand.bust:
            print("Dealer Busts")
            print()
        for handID, outcome in enumerate(self.outcomes):
            if outcome == "Blackjack":
                msg = "Player Wins Hand " + str(handID + 1) + " Via Blackjack"
            elif outcome == "Win":
                msg = "Player Wins Hand " + str(handID + 1)
            elif outcome == "Push":
                msg = "Push On Hand " + str(handID + 1)
            else:
                msg = "Player Loss on Hand " + str(handID + 1)

            msg += " {0:{1}}".format(self.payout[handID], '+' if self.payout[handID] else '')
            print(msg)

        print("\nWinnings/Losses: {0:{1}}".format(sum(self.payout), '+' if sum(self.payout) else ''))

    def calculatePayout(self) -> list[float]:
        payout = []
        for handID, outcome in enumerate(self.outcomes):
            if outcome == "Blackjack":
                payout.append(self.player.bets[handID] * 1.5)
            elif outcome == "Win":
                payout.append(self.player.bets[handID])
            elif outcome == "Push":
                payout.append(0)
            else:
                payout.append(-self.player.bets[handID])

        return payout

    def makePayout(self) -> None:
        self.player.balance += sum(self.payout)

    def askPlayAgain(self) -> bool:
        if self.player.balance > 0:
            while True:
                playAgain = input("\nPlay again (y/n): ")
                if playAgain.lower() == "y":
                    return True
                elif playAgain.lower() == "n":
                    return False
        else:
            print("Account Balance Empty")
            return False