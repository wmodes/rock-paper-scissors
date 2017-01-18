#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""rock_paper_scissors.py: The classic game with some extra features."""
__author__      = "Wes Modes (wmodes@gmail.com)"
__copyright__   = "2016, MIT"


import os
import sys
from time import time, sleep
import textwrap
import re
from random import choice

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
COUNT_WORDS = ["ONE", "TWO", "THREE", "GO!", ""]
#COUNT_WORDS = ["RO", "SHO", "BO!"]

# TODO: Use python module curses that allows easy painting text on the terminal
# ANSI Escape Codes - these work for MOST terminals, but not all
ANSI_ESC = '\033'
ANSI_CLEAR = ANSI_ESC+'[2J'
ANSI_ERASE_EOL = ANSI_ESC+'[K'
ANSI_DOWN1 = ANSI_ESC+'[1B'
ANSI_UP1 = ANSI_ESC+'[1A'
ANSI_HOME = ANSI_ESC+'[0;0H'
ANSI_BOTTOM = ANSI_ESC+'[999;0H'
ANSI_ERASELINE = ANSI_ESC+'[2K'

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
min_wins = 1
win_count = [0, 0]
game = 0
# how wide we want to display our text
text_width = 80
text_indent = 4
# What do we call the players
player1 = "Player 1"
player2 = "Player 2"
# record keeping
game_record = []

computer_strategy = "wsls"

#
# text bidness
#   we spend a bit of effort to make sure that things print nicely
#

def get_scr_size():
    """Get row and column size of currently running terminal and return as (row, col) tuple"""
    rows, cols = os.popen('stty size', 'r').read().split()
    # these come as strings so we cast them to int
    return (int(rows), int(cols))

def nicely(text, left_indent=0, right_indent=0, format="left"):
    """Return a paragraph of text, breaking it nicely at the margins. 
    With optional arguments, you can indent the left or right margins or center the text."""
    # get row and column size of currently running terminal
    max_rows, max_cols = get_scr_size()
    if (max_cols > text_width):
        left_margin = (max_cols - text_width) / 2
        right_margin = left_margin
    else:
        left_margin = 0
        right_margin = 0
    # here's a string of spaces to help indent our text
    indent_str = ' ' * (left_indent + left_margin)
    # now subtract left and right margins from text width
    cols = max_cols - left_margin - right_margin - left_indent - right_indent
    # Multiple whitespace will just mess stuff up.
    # Here we use the 're' module for regular expressions to substitute multiple
    # remove whitespace on first line and at end
    text =  text.strip() + " "
    # remove whitespace before and after each newline
    text =  re.sub('[ \t]*\n[ \t]*', '\n', text)
    # Now we use the 'textwrap' module which nicely wraps things at n columns
    text = textwrap.fill(text, cols)
    if (str(format).lower() == "center"):
        # create string for format() command to center: '{:^80}' = center in 80 cols
        fmt = '{:^'+str(cols)+'}'
        # this is some tricky shit that will center the text on each line
        text = '\n'.join(fmt.format(s) for s in text.split('\n'))
    elif (str(format).lower() == "right"):
        # create string for format() command to right justify: '{:>80}' = right justfy in 80 cols
        fmt = '{:>'+str(cols)+'}'
        # more tricky shit that will right justify the text on each line
        text = '\n'.join(fmt.format(s) for s in text.split('\n'))        
    # add spaces before first line
    text = re.sub('^', indent_str, text)
    # add spaces after each newline
    text = re.sub('\n', '\n' + indent_str, text)
    # if there are spaces at the end, remove them
    text = text.rstrip()
    return text

def indent(text):
    """ Indent string and print nicely()"""
    left_indent = text_indent
    right_indent = text_indent
    # pass all arguments (including left_indent & right_indent) to nicely() and return results
    return nicely(**locals())

def left(text, left_indent=0, right_indent=0):
    """Left justify string and print nicely()"""
    format = "left"
    # pass all arguments (including format) to nicely() and return results
    return nicely(**locals())

def center(text, left_indent=0, right_indent=0):
    """Center string and print nicely()"""
    format = "center"
    # pass all arguments (including format) to nicely() and return results
    return nicely(**locals())

def right(text, left_indent=0, right_indent=0):
    """Right justify string and print nicely()"""
    format = "right"
    # pass all arguments (including format) to nicely() and return results
    return nicely(**locals())


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
        return False
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
    global players, elements, hands, player1, player2, min_wins
    print ""
    # ask how many players - repeat until we get an answer
    while 1:
        # the comma at the end here makes it not issue a newline, 
        # so the question will be on one line
        print nicely("Play against the computer or another human (or help)?"),
        input = raw_input("").lower();
        if (input == "help"):
            print indent("""Whether you play against another person or against the computer, you
                will both select your hand at the same time using the number keys.""")
        elif ('c' in input):
            print indent("Play against the computer. Okay.")
            players = 1
            # what do we call them - this will help us later, preventing lots of conditionals
            player1 = "Player"
            player2 = "Computer"
            break
        elif ('h' in input or 'p' in input):
            print indent("Play against another person. Okay.")
            players = 2
            # what do we call them - this will help us later, preventing lots of conditionals
            player1 = "Player 1"
            player2 = "Player 2"
            break
        else:
            print indent("Not sure what you said there.")
    print ""
    # ask how many elements - repeat until we get an answer
    while 1:
        # the comma at the end here makes it not issue a newline, 
        # so the question will be on one line
        print nicely("""Traditional Rock-Paper-Scissors (RPS) or 
            Rock-Paper-Scissors-Lizard-Spock (RPSLS) (or help)?"""),
        input = raw_input("").lower();
        if (input == "help"):
            print indent("RPSLS is like traditional RPS but adds two new elements:")
            print indent("""Spock smashes scissors and vaporizes rock; he is poisoned 
                by lizard and disproven by paper. Lizard poisons Spock and eats paper; 
                it is crushed by rock and decapitated by scissors.""")
        elif any(s in input for s in ['rpsls', 'spock', 'li']):
            print indent("Rock-Paper-Scissors-Lizard-Spock. Okay!")
            elements = 5
            break
        elif any(s in input for s in ['rps', 'tra', 'old']):
            print indent("Traditional Rock-Paper-Scissors")
            elements = 3
            break
        else:
            print indent("Not sure what you said there.")
    print ""
    # ask how many wins are needed - repeat until we get an answer
    while 1:
        print nicely("Instant-death, 2-out-of-3, or indefinite (or help)?"),
        input = raw_input("").lower();
        if (input == "help"):
            print indent("""With instant-death, you will play one throw to determine the winner. 
                With 2 out of 3, you have to win at least two throws to win the game.
                With indefinite, you play forever or until you decide you are done.""")
        # we'll just look for a few unique key letters in the input
        elif any(s in input for s in ['1', 'ins', 'dea']):
            print indent("Instant-death!")
            min_wins = 1
            break
        # we'll just look for a few unique key letters in the input
        elif any(s in input for s in ['ind', 'def', 'for', 'infi']):
            print indent("Indefinite!")
            min_wins = 1000
            break
        # we'll just look for the numbers
        elif any(s in input for s in ['2', '3', 'out']):
            print indent("Two-out-of-three. Alright.")
            min_wins = 2
            break
        else:
            print indent("Not sure what you said there.")

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

# print the key guide
def print_key_guide():
    if (players == 1):
        print nicely("""Here are the keys to press for your throw:""")
    else:
        print nicely("""Here are the keys for both player's throws:""")  
    tab1_text = "\t" * 2
    tab2_text = "\t" * 2
    #print "-"*(37)
    print ""
    if (players == 1):
        print indent("Player Keys")
        print indent("-----------")
    else:    
        print indent("Player 1 Keys" + tab1_text + "Player 2 Keys")
        print indent("-------------" + tab1_text + "-------------")
    for e in range(elements):
        string = KEYS[0][e] + " = " + element_list[e]
        if (players == 2):
            string += tab2_text
            string += KEYS[1][e] + " = " + element_list[e]
        print indent(string)
    print ""
    print nicely("""Wait for the count followed by "Go!" """)

def print_score():
    print ""
    tab_text = "\t" * 2
    print nicely("Throw %i - Current score:" % game)
    print nicely("------------------------")
    print indent("%s:  %i%s%s:  %i" % (player1, win_count[0], tab_text,
        player2, win_count[1]))

def ready(text = "Any key to start."):
    print nicely(text),
    c = waitforkey()
    if supports_ansi():
        print ANSI_ERASELINE
    return c

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
            c = str(sys.stdin.read(1))
        except IOError: 
            pass
    keynormalmode()
    #print "keypressmode turned off"
    return c

def checkforkey():
    c = ""
    try:
        #sys.stdin.read(1)
        c = str(sys.stdin.read(1))
        #print "Got character", c
    except IOError: 
        pass
    return c

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

def legal_key(c):
    """Check to see if keypress is in KEY database and return which player and throw it corresponds to"""
    for e in range(elements):
        for p in range(players):
            if (c == KEYS[p][e]):
                # if we find it in KEYS, we return player and element
                return (p, e)

def defeats(element1, element2):
    """ Does element1 defeat element2?"""
    return element2 in ELEMENTS[element1]["defeats"]

def what_defeats(element):
    """Look up what defeats a given element"""
    choices = []
    for lookup in element_list[0:elements]:
        if defeats(lookup, element):
            choices.append(lookup)
    return choice(choices)

def get_system_choice():
    """Choose computer's throw. """
    """We will exploit the win-stay, lose-shift strategy:
            1. If our opponent wins, statistically they tend to stick with their winning move. 
                So if we lose, we shift to a throw that will win against our opponent's previous throw.
            2. If we won, we mirror what our opponent played.
    """
    """TODO: We have to keep track of:
        - which strategy we are currently using
        - our win-lose record over the last few games
        - the last two throws of us and our opponent
        - possibly a record of the strategies it appears our opponent is using, to shift to
            a win against that strategy
        """
    # STRATEGY 1: win-stay, lose-shift
    #   * Assume A is opponent's throw, and A' defeats opponent's throw.
    #   * If we win, next we play A
    #   * If we lose, next we play A'
    #   * If we are losing playing this strategy, shift to another strategy
    #       TODO: Implement this
    if (computer_strategy == "wsls"):
        if (not game_record):
            # if we have no data yet, choose scissors
            computer_throw = "scissors"
        else:
            their_last = game_record[-1]["p1"]
            our_last = game_record[-1]["p2"]
            # get results
            results = who_won(their_last, our_last)
            # did we tie? - if so, choose randomly
            if (not results):
                computer_throw = element_list[choice(range(elements))]
            # did they win? - if so, choose a throw to defeat their last one
            elif (results == 1):
                computer_throw = what_defeats(their_last)
            # did we win? - if so, choose their last throw
            elif (results == 2):
                computer_throw = their_last
    # STRATEGY 2: random
    else:
        computer_throw = element_list[choice(range(elements))]
    return computer_throw

# countdown and choices
def countdown_choices():
    print ""
    # we'll need to make sure players don't go twice
    played = [False, False] 
    # just in case a player doesn't go at all we need some default values
    p1_element = ""; p2_element = ""
    p1_time = 0; p2_time = 0
    keypressmode()
    for count in COUNT_WORDS:
        print center(count)
        # here we mark the current time in seconds
        count_time = time()
        if ("go" in count.lower()):
            zero_time = time()
            # get computer's choice
            p2_element = get_system_choice()
            print right(player2 + ": " + p2_element)
            p2_time = time()
        # we will loop through this until ONE second has gone by
        while(time() < count_time + 1):
            c = checkforkey()
            if (c):
                # check to see if key is legal key
                key_result = legal_key(c)
                # if we got results we do stuff
                if key_result:
                    # legal_key() returned a tuple which we break into parts
                    (p, e) = key_result
                    #print "p:",p,"e:",e
                    # if player has not already gone
                    if (not played[p]):
                        # now we make sure they can't play again
                        played[p] = True
                        if (p == 0):
                            p1_element = element_list[e]
                            # record time player one threw (to see if they are cheating)
                            p1_time = time()
                            print left(player1 + ": " + p1_element)
                        else:
                            p2_element = element_list[e]
                            # record time player two threw
                            p2_time = time()
                            print right(player2 + ": " + p2_element)
    keynormalmode()
    # calculate how long after "Go!" p1 threw, this could be negative if they went early
    if (p1_time):
        p1_wait = p1_time - zero_time
    # but if the player didn't go their delay is 0
    else:
        p1_wait = 0
    # calculate how long after "Go!" p2 threw, this could be negative if they went early
    if (p2_time):
        p2_wait = p2_time - zero_time
    # but if the player didn't go their delay is 0
    else:
        p2_wait = 0
    return (p1_element, p1_wait, p2_element, p2_wait)

def who_won(p1_element, p2_element):
    # who does each player defeat? - get dictionary of defeats
    p1_defeats_dict = ELEMENTS[p1_element]["defeats"]
    p2_defeats_dict = ELEMENTS[p2_element]["defeats"]
    # is it a tie?
    if (p1_element == p2_element):
        return 0
    # did p1 win?
    elif (p2_element in p1_defeats_dict):
        return 1
    # p2 won
    elif (p1_element in p2_defeats_dict):
        return 2
    else:
        return 100
 
def report_winner(p1_element, p2_element):
    """ determine winner of throw"""
    # declaring these variables as global allows us to change them from within the local scope
    global win_count
    print ""
    # who does each player defeat? - get dictionary of defeats
    p1_defeats_dict = ELEMENTS[p1_element]["defeats"]
    p2_defeats_dict = ELEMENTS[p2_element]["defeats"]
    # first we check if one or both of the players didn't throw
    didnt_go = []
    if (not p1_element):
        didnt_go.append(player1)
    if (not p2_element):
        didnt_go.append(player2)
    if (not p1_element or not p2_element):
        text1 = " and ".join(didnt_go) + " didn't throw!"
        text2 = "After the count, press the key to indicate your throw."
    else:
        # for color we choose a random synonym from list
        p1_text = choice(ELEMENTS[p1_element]["synonyms"])
        p2_text = choice(ELEMENTS[p2_element]["synonyms"])
        # get results of contest
        results = who_won(p1_element, p2_element)
        # first we check for a tie
        if (results == 0):
            text1 = p1_text + " " + ELEMENTS[p1_element]["ties"] + " " + p2_text
            text2 = "It's a tie!"
        elif (results == 1):
            text1 = p1_text + " " + p1_defeats_dict[p2_element] + " " + p2_text
            text2 = player1 + " wins!"
            win_count[0] += 1
        elif (results == 2):
            text1 = p2_text + " " + p2_defeats_dict[p1_element] + " " + p1_text
            text2 = player2 + " wins!"
            win_count[1] += 1
        else:
            text1 = "Uh, something weird happened."
            text2 = "p1_element:"+p1_element+" p2_element:"+p2_element
    print center(text1)
    print center(text2)

def cheaters(p1_delay, p2_delay):
    """Look at delays and see if anyone is cheating"""
    print ""
    early = []
    late = []
    if (p1_delay < -0.5):
        early.append(player1)
    if  (p2_delay < -0.5):
        early.append(player2)
    early_birds = " and ".join(early)
    if (p1_delay > 0.5):
        late.append(player1)
    if  (p2_delay > 0.5):
        late.append(player2)
    late_bees = " and ".join(late)
    if (early_birds):
        print center("""Reminder: Wait until "GO!" Talking to you, %s""" % early_birds)
    if (late_bees):
        print center("""If you throw too long after "GO!" some might say you are cheating.""")
        print center("""Ahem, %s""" % late_bees)

def what_strategy(old1, old2, winner, new1, new2):
    """Try to guess the apparent strategy player is using, based on the previous moves, the current moves, 
    and who won the last game."""
    # if the previous game was a tie, we can't infer anything about it
    if (winner == 0):
        return("unknown")
    # Strategy 1: Win Stay, Loss Shift
    # if they won, and stayed, or
    elif (((winner == 1) and (new1 == old1)) or
            # if they lost, and shifted to what would have won
            ((winner == 2) and defeats(new1, old2))):
        return("wsls")
    # Strategy 2: Contrarian strategy - a defence/offense against WSLS
    # if they won, and then shifted to what would have lost to that throw
    elif (((winner == 1) and defeats(new1, old1)) or
            # if they lost, and then chose their opponent's old hand
            ((winner == 2) and (new1 == old2))):
        return("contrarian")
    else:
        return("unknown")

def keep_record(p1_element, p2_element):
    """We record each players' throw for possible analysis and strategy"""
    global game_record
    if (not game_record):
        p1_strategy = "unknown"
        p2_strategy = "unknown"
    else:
        last_game = game_record[-1]
        p1_strategy = what_strategy(last_game["p1"], last_game["p2"], last_game["winner"], 
            p1_element, p2_element)
        p2_strategy = what_strategy(last_game["p2"], last_game["p1"], last_game["winner"], 
            p2_element, p1_element)
    # Lists are lists of python objects, and these objects can be dictionaries
    game_record.append({
            "p1": p1_element,
            "p2": p2_element,
            "winner": who_won(p1_element, p2_element),
            "strategy1": p1_strategy,
            "strategy2": p2_strategy
        })

def print_record():
    """Print the game record"""
    print ""
    tab = "    "
    print nicely(player1 + " vs. " + player2)
    print nicely("----------------------")
    print nicely("%8s%s%8s%s%8s%s%8s%s%10s%s%10s" % 
            ("Throw", tab, "P1", tab, "P2", tab, "Winner", tab, "Strategy 1", tab, "Strategy 2"))
    for n in range(len(game_record)):
        throw = game_record[n]
        print nicely("%8s%s%8s%s%8s%s%8s%s%10s%s%10s" % 
            (str(n), tab, throw["p1"], tab, throw["p2"], tab, str(throw["winner"]), 
                tab, throw["strategy1"], tab, throw["strategy2"]))

#
# our main loop
#

# note that most of the work is done by functions above
def main():
    global game
    keysetup()
    clear()
    user_config_game()
    print_brief()
    ready("Hit any key.")
    c = ""
    # let's repeat until either the player wants to quit or someone has won enough throws
    while ((c != 'q') and (min_wins not in win_count)):
        print_key_guide()
        print ""
        ready("Press any key to start")
        print ""
        print center("Okay, here goes!")
        sleep(1)
        game += 1
        (p1_hand, p1_delay, p2_hand, p2_delay) = countdown_choices()
        report_winner(p1_hand, p2_hand)
        cheaters(p1_delay, p2_delay)
        keep_record(p1_hand, p2_hand)
        print_score()
        print ""
        if (min_wins not in win_count):
            c = ready("New throw? (q to quit)")
    #print "c",c,"min_wins",min_wins,"win_count",win_count,"min_wins not in
    #   win_count",min_wins not in win_count
    keynormalmode()
    print_record()

# 
if __name__=='__main__':
    # try:     
        # Enter the main loop
    main()
    # except Exception as e: 
    #     print ""
    #     print str(e)
    #     keynormalmode()
    # except:
    #     print ""
    #     print "Exiting."
    #     keynormalmode()
