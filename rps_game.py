"""rock_paper_scissors.py: The classic game with some extra features."""
__author__      = "Wes Modes (wmodes@gmail.com)"
__copyright__   = "2016, MIT"

class rpsGame():

    def __init__(self, players=1, elements=3, hands=1):
        self.players = players
        self.elements = elements
        self.hands = hands

    def __print__(self):
        print "Players:", self.players
        print "Elements:", self.elements
        print "Hands:", self.hands