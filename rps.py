#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""rock_paper_scissors.py: The classic game with some extra features."""
__author__      = "Wes Modes (wmodes@gmail.com)"
__copyright__   = "2016, MIT"


import os
import sys
from time import time
import textwrap
import re

# get data from external file
from rps_data import *
#from termcolor import colored, cprint

# these are all used just to get keyboard events. Thanks Python docs:
# https://docs.python.org/2/faq/library.html#how-do-i-get-a-single-keypress-at-a-time
import termios, fcntl, sys, os


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
# the number of players
players = 1
# the number of elements in the game
elements = 3
# the max number of hands we play to determine a winner
hands = 1
# how wide we want to display our text
max_width = 80
tab = 4

#
# text bidness
#   we spend a bit of effort to make sure that things print nicely
#

def nicely(text, left_indent=0, right_indent=0):
    """Return a paragaph of text, breaking it nicely at the margins. With 
    optional arguments, you can indent the left or right margins."""
    # get row and column size of currently running terminal
    term_rows, term_cols = os.popen('stty size', 'r').read().split()
    # these come as strings so we cast them to int
    term_rows = int(term_rows)
    term_cols = int(term_cols)
    if (term_cols > max_width):
        left_margin = (term_cols - max_width) / 2
        right_margin = left_margin
    else:
        left_margin = 0
        right_margin = 0
    # here's a string of spaces to help indent our text
    indent_str = ' ' * (left_indent + left_margin)
    # now subtract left and right margins from text width
    cols = term_cols - left_margin - right_margin - left_indent - right_indent
    # Multiple whitespace will just mess stuff up.
    # Here we use the 're' module for regular expressions to substitute multiple
    # remove whitespace on first line and at end
    text =  text.strip()
    # remove whitespace before and after each newline
    text =  re.sub('[ \t]*\n[ \t]*', '\n', text)
    # Now we use the 'textwrap' module which nicely wraps things at n columns
    text = textwrap.fill(text, cols)
    # add spaces before first line
    text = re.sub('^', indent_str, text)
    # add spaces after each newline
    text = re.sub('\n', '\n' + indent_str, text)
    # if there are spaces at the end, remove them
    text = text.rstrip()
    return text

#
# screen manipulations
#

def supports_ansi():
    """Returns True if the running system's terminal supports color, and False
    otherwise."""
    plat = sys.platform
    supported_platform = plat != 'Pocket PC' and (plat != 'win32' or
                                                  'ANSICON' in os.environ)
    # isatty is not always implemented, #6223.
    is_a_tty = hasattr(sys.stdout, 'isatty') and sys.stdout.isatty()
    if not supported_platform or not is_a_tty:
        print "Nope, doesn't support ANSI"
        return False
    print "Yup, supports ANSI"
    return True

def clear():
    if supports_ansi():
        print ANSI_CLEAR

#
# instructions
#   and other text-based things specific to this game
#

def user_config_game():
    """Get answers to important configuration questions for the game: Select one player or two?
    Select instant-death or two-out-of-three? Traditional RPS or RPSLS? """
    # declaring these variables as global allows us to change them from within the local scope
    global players, elements, hands
    print ""
    # ask how many players - repeat until we get an answer
    while 1:
        # the comma at the end here makes it not issue a newline, 
        # so the question will be on one line
        print nicely("Play against the computer or another human (or help)?"),
        input = raw_input("").lower();
        if (input == "help"):
            print nicely("""Whether you play against another person or against the computer, you
                will both select your hand at the same time using the number keys.""", tab)
        elif ('c' in input):
            print nicely("Play against the computer. Okay.", tab)
            players = 1
            break
        elif ('h' in input or 'p' in input):
            print nicely("Play against another person. Okay.", tab)
            players = 2
            break
        else:
            print nicely("Not sure what you said there.", tab)
    print ""
    # ask how many elements - repeat until we get an answer
    while 1:
        # the comma at the end here makes it not issue a newline, 
        # so the question will be on one line
        print nicely("""Traditional Rock-Paper-Scissors (RPS) or 
            Rock-Paper-Scissors-Lizard-Spock (RPSLS) (or help)?"""),
        input = raw_input("").lower();
        if (input == "help"):
            print nicely("RPSLS is like traditional RPS but adds two new elements:", tab)
            print nicely("""Spock smashes scissors and vaporizes rock; he is poisoned 
                by lizard and disproven by paper. Lizard poisons Spock and eats paper; 
                it is crushed by rock and decapitated by scissors.""", tab)
        elif ('l' in input or 'spock' in input):
            print nicely("Rock-Paper-Scissors-Lizard-Spock. Okay!", tab)
            elements = 5
            break
        elif ('rps' in input):
            print nicely("Traditional Rock-Paper-Scissors", tab)
            elements = 3
            break
        else:
            print nicely("Not sure what you said there.", tab)
    print ""
    # ask how many hands - repeat until we get an answer
    while 1:
        print nicely("Instant-death or 2-out-of-3 (or help)?"),
        input = raw_input("").lower();
        if (input == "help"):
            print nicely("""With instant-death, you will play one hand to determine the winner. 
                With 2 out of 3, you have to win at least two hands to win the round.""", tab)
        # we'll just look for the first letters of instant or death to simplify things
        elif ('i' in input or 'd' in input):
            print nicely("Instant-death!", tab)
            hands = 1
            break
        # we'll just look for the numbers
        elif ('2' in input or '3' in input):
            print nicely("Two-out-of-three. Alright.", tab)
            hands = 3
            break
        else:
            print nicely("Not sure what you said there.", tab)

def print_brief():
    """Print brief instructions for the game"""
    print ""
    if (players == 1):
        player_text = "you and the computer"
    else:
        player_text = "both players"
    print nicely("""Traditionally, in each round, players usually count aloud to 3, or say 
        the name of the game ("rock paper scissors," "Ro Sham Bo," "Jan Ken Po", and so on) 
        raising one hand in a fist and swinging it down on the count. They then \"throw\" 
        by extending their chosen "hand," either rock, paper, or scissors, towards their 
        opponent. These shapes are "rock" (a simple fist), "paper" (a flat hand), and 
        "scissors" (a fist with the index and middle fingers together forming a V).""")
    print ''
    # here we do string interpolation to substitute %s with player_text form above
    print nicely("""In this game, you will get a 1-2-3 count, whereupon %s will
        simultaneously choose a "hand" (in this case, a chosen key).""" % (player_text))
    print ''
    print nicely("""Here are the rules around which hand wins:""")
    if (elements == 3):
        print nicely("""Scissors cuts paper. Paper covers rock. Rock crushes scissors.""")
    else:
        print nicely("""Scissors cuts paper and decapitates lizard. Paper covers rock and 
            disproves Spock. Rock crushes scissors and lizard. Lizard eats paper and poisons 
            Spock. Spock smashes scissors and vaporizes rock.""")
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
        print nicely("Player Keys", tab)
        print nicely("-----------", tab)
        print nicely("1 = " + element_list[0], tab)
        print nicely("2 = " + element_list[1], tab)
        print nicely("3 = " + element_list[2], tab)
        if (elements == 5):
            print nicely("4 = " + element_list[3], tab)
            print nicely("5 = " + element_list[4], tab)
    else:
        print nicely("Player 1 Keys" + "\t"*tab1 + "Player 2 Keys", tab)
        print nicely("-------------" + "\t"*tab1 + "-------------", tab)
        print nicely("1 = " + element_list[0] + "\t"*tab2 + "6 = " + element_list[0], tab)
        print nicely("2 = " + element_list[1] + "\t"*tab2 + "7 = " + element_list[1], tab)
        print nicely("3 = " + element_list[2] + "\t"*tab2 + "8 = " + element_list[2], tab)
        if (elements == 5):
            print nicely("4 = " + element_list[3] + "\t"*tab2 + "9 = " + element_list[3], tab)
            print nicely("5 = " + element_list[4] + "\t"*tab2 + "0 = " + element_list[4], tab)
    print ""

def ready(text = "Ready? "):
    print nicely(text),
    waitforkey()
    print ""

#
# keypress stuff
# 

def waitforkey():
    keypressmode()
    #print "keypressmode set"
    c = ""
    while not c:
        try:
            #sys.stdin.read(1)
            c = repr(sys.stdin.read(1))
            #print "Got character", c
        except IOError: 
            pass
    keynormalmode()
    #print "keypressmode turned off"

def keysetup():
    # all of this sets up our terminal for keypress events
    global fd, oldterm, newattr, oldflags
    fd = sys.stdin.fileno()
    oldterm = termios.tcgetattr(fd)
    newattr = termios.tcgetattr(fd)
    oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)

def keypressmode():
    # we modify the terminal so that if accepts keys one at a time rather than in lines
    newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
    termios.tcsetattr(fd, termios.TCSANOW, newattr)
    oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)
    fcntl.fcntl(fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)

def keynormalmode():
    # now put everything back
    termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
    fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)

#
# "throws"
#   computer and users choose "hand"
#

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

#
# our main loop
#

# note that most of the work is done by functions above
def main():
    clear()
    user_config_game()
    print_brief()
    ready("Hit any key.")
    print_key_guide()

# 
if __name__=='__main__':
    try:
        keysetup()
        # Enter the main loop
        main()
        keynormalmode()
    except Exception as e: 
        print ""
        print str(e)
        keynormalmode()
    except:
        print ""
        print "Exiting."
        keynormalmode()