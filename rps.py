#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""rock_paper_scissors.py: The classic game with some extra features."""
__author__      = "Wes Modes (wmodes@gmail.com)"
__copyright__   = "2016, MIT"


import os
import sys
from time import time

# get data from external file
from rps_data import *
#from termcolor import colored, cprint

#
# Constants
#   (Convention: These are capitalized)
#
GRACE_TIME = 1000   # time in ms before we suspect the user is cheating

# TODO: Use python module curses that allows easy painting text on the terminal
# ANSI Escape Codes - these work for MOST terminals, but not all
ANSI_CLEAR = '\033[2J'
ANSI_ERASE_EOL = '\033[K'
ANSI_DOWN1 = '\033[1B'
ANSI_UP1 = '\033[1A'

#
# Global variables
#   (it is good style to minimize globals)
#
user_past_choices = []
players = 1
elements = 3
hands = 1

def supports_ansi():
    """
    Returns True if the running system's terminal supports color, and False
    otherwise.
    """
    plat = sys.platform
    supported_platform = plat != 'Pocket PC' and (plat != 'win32' or
                                                  'ANSICON' in os.environ)
    # isatty is not always implemented, #6223.
    is_a_tty = hasattr(sys.stdout, 'isatty') and sys.stdout.isatty()
    if not supported_platform or not is_a_tty:
        return False
    return True

# print the rules
def print_rules():
    pass

# print brief instructions
def print_brief():
    if (players == 1):
        player_text = "you and the computer"
    else:
        player_text = "both players"
    print 'Traditionally, in each round, players usually count aloud to 3, or say the name of the'
    print 'game ("rock paper scissors," "Ro Sham Bo," "Jan Ken Po", and so on) raising one'
    print 'hand in a fist and swinging it down on the count. They then \"throw\" by extending their'
    print 'chosen "hand," either rock, paper, or scissors, towards their opponent. These shapes are '
    print '"rock" (a simple fist), "paper" (a flat hand), and "scissors" (a fist with the '
    print 'index and middle fingers together forming a V).'
    print ''
    print 'In this game, you will get a 1-2-3 count, whereupon', player_text, 'will'
    print 'simultaneously choose a "hand" (in this case, a chosen key).'
    print ''
    print 'Here are the rules around which hand wins:'
    if (elements == 3):
        print 'Scissors cuts paper. Paper covers rock. Rock crushes scissors.'
    else:
        print 'Scissors cuts paper and decapitates lizard. Paper covers rock and disproves Spock.'
        print 'Rock crushes scissors and lizard. Lizard eats paper and poisons Spock. Spock'
        print 'smashes scissors and vaporizes rock.'
    print ''

# center text in fixed string width (without cutting front off)
def center_tab(string, width):
    string = str(string)    # in case someone passes us a number
    length = len(string)
    if (length >= width):
        return string[0:width]
    else:
        left_margin = (width - length)/2
        right_margin = width - left_margin - length
        return (left_margin * " ") + string + (right_margin * " ")

# print the key guide
def print_key_guide():
    #print "players:", players, "elements", elements, "hands", hands
    tab1 = 2
    tab2 = 2
    #print "-"*(37)
    print ""
    if (players == 1):
        print "Player Keys"
        print "-----------"
        print "1 =", element_list[0]
        print "2 =", element_list[1]
        print "3 =", element_list[2]
        if (elements == 5):
            print "4 =", element_list[3]
            print "5 =", element_list[4]
    else:
        print "Player 1 Keys", "\t"*tab1, "Player 2 Keys"
        print "-------------", "\t"*tab1, "-------------"
        print "1 =", element_list[0], "\t"*tab2, "6 =", element_list[0]
        print "2 =", element_list[1], "\t"*tab2, "7 =", element_list[1]
        print "3 =", element_list[2], "\t"*tab2, "8 =", element_list[2]
        if (elements == 5):
            print "4 =", element_list[3], "\t"*tab2, "9 =", element_list[3]
            print "5 =", element_list[4], "\t"*tab2, "0 =", element_list[4]
    print ""
    

# select one player or two?
# select instant-death or two-out-of-three
# traditional RPS or RPSLS
def user_config_game():
    global players, elements, hands
    print ""
    # ask how many players - repeat until we get an answer
    while 1:
        input = raw_input("Play against the computer or another human (or help)? ").lower();
        if (input == "help"):
            print "  Whether you play against another person or against the computer, you"
            print "  will both select your hand at the same time using the number keys."
        elif ('c' in input):
            print "  Play against the computer. Okay."
            players = 1
            break
        elif ('h' in input or 'p' in input):
            print "  Play against another person. Okay."
            players = 2
            break
        else:
            print "  Not sure what you said there."
    print ""
    # ask how many elements - repeat until we get an answer
    while 1:
        print "Traditional Rock-Paper-Scissors (RPS) or"
        input = raw_input("Rock-Paper-Scissors-Lizard-Spock (RPSLS) (or help)? ").lower();
        if (input == "help"):
            print "  RPSLS is like traditional RPS but adds two new elements:"
            print "  Spock smashes scissors and vaporizes rock; he is poisoned "
            print "  by lizard and disproven by paper. Lizard poisons Spock and "
            print "  eats paper; it is crushed by rock and decapitated by scissors."
        elif ('l' in input or 'spock' in input):
            print "  Rock-Paper-Scissors-Lizard-Spock. Okay!"
            elements = 5
            break
        elif ('rps' in input):
            print "  Traditional RPS"
            elements = 3
            break
        else:
            print "  Not sure what you said there."
    print "\nFinally,",
    # ask how many hands - repeat until we get an answer
    while 1:
        input = raw_input("Instant-death or 2-out-of-3 (or help)? ").lower();
        if (input == "help"):
            print "  With instant-death, you will play one hand to determine the"
            print "  winner. With 2 out of 3, you have to win at least two hands"
            print "  to win the round."
        # we'll just look for the first letters of instant or death to simplify things
        elif ('i' in input or 'd' in input):
            print "  Instant-death!"
            hands = 1
            break
        # we'll just look for the numbers
        elif ('2' in input or '3' in input):
            print "  Two-out-of-three. Alright."
            hands = 3
            break
        else:
            print "  Not sure what you said there."


# computer player chooses
def get_system_choice():
    pass

# get user keypress
def get_user_choice():
    pass

# countdown and choices
def countdown_choices():
    pass

# determine winner of round
def determine_winner():
    pass

# our main loop
#
# note that most of the work is done by functions above
def main():
    if supports_ansi():
        print ANSI_CLEAR
    user_config_game()
    print_brief()
    print_key_guide()

# 
if __name__=='__main__':
        # Enter the main loop
        main() 