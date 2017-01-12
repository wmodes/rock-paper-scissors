"""rock_paper_scissors.py: The classic game with some extra features."""
__author__      = "Wes Modes (wmodes@gmail.com)"
__copyright__   = "2016, MIT"


import os
import sys
from time import time

# get data from external file
from rps_data import *
from termcolor import colored, cprint



#
# Constants
#   (Convention: These are capitalized)
#
GRACE_TIME = 1000   # time in ms before we suspect the user is cheating

#
# Global variables
#   (it is good style to minimize globals)
#
user_past_choices = []
players = 1
elements = 3
hands = 1

# print the rules
def print_rules():
    pass

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
    # get the width of the console
    # thanks, stackoverflow: http://stackoverflow.com/questions/566746/
    rows, columns = os.popen('stty size', 'r').read().split()
    keys = 10
    width = int(columns)/keys   # width of each key
    # we'll construct a list of which keys represent which choices
    #   (zero = blank, and 1 = first element in list)
    num_list = [1,2,3]
    if (elements == 5):
        num_list.extend([4,5])
    else:
        num_list.extend([0,0])
    if (players == 2):
        num_list.extend([1,2,3])
        if (elements == 5):
            num_list.extend([4,5])
        else:
            num_list.extend([0,0])
    else:
        num_list.extend([0,0,0,0,0])
    # now we should have a list of 10 numbers that represents which keys
    #   correspond to which choice
    # We can now create a list of words for each key, looking each one
    #   in our elements list
    word_list = []
    for num in num_list:
        if (not num):
            word_list.append("")
        else:
            word_list.append(element_list[num-1])
    # Line 1 of key guide - Players
    if (players == 1):
        if (elements == 3):
            text = colored(center_tab("Player", width*3 - 1) + "|", attrs=['reverse'])
        else:
            text = colored(center_tab("Player", width*5 - 1) + "|", attrs=['reverse'])
    else:
        if (elements == 3):
            text = colored(center_tab("Player 1", width*3 - 1) + "|", attrs=['reverse'])
            text += ((width*2 - 1) * " ") + "|"
            text += colored(center_tab("Player 2", width*3 - 1) + "|", attrs=['reverse'])
        else:
            text = colored(center_tab("Player 1", width*5 - 1) + "|", attrs=['reverse'])
            text += colored(center_tab("Player 2", width*5 - 1) + "|", attrs=['reverse'])            
    print text
    # Line 2 of key guide - Words
    for word in word_list:
        if (word):
            sys.stdout.write(colored(center_tab(word, width-1)+"|", attrs=['reverse']))
        else:
            sys.stdout.write(center_tab("", width-1)+"|")
    print ""
    # Line 3 of key guide - Numbers
    for key in range(len(word_list)):
        # we only want to print numbers for keys we are using
        if (word_list[key]):
            sys.stdout.write(colored(center_tab(key+1, width-1)+"|", attrs=['reverse']))
        else:
            sys.stdout.write(center_tab("", width-1)+"|")
    print ""
    

# select one player or two?
# select instant-death or two-out-of-three
# traditional RPS or RPSLS
def user_config_game():
    global players, elements, rounds
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
        elif ('rps' in input):
            print "  Traditional RPS"
            elements = 3
            break
        elif ('l' in input or '3' in input):
            print "  Rock-Paper-Scissors-Lizard-Spock. Okay!"
            elements = 5
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
    #user_config_game()
    global players, elements, rounds
    players = 1
    elements = 3
    print_key_guide()


if __name__=='__main__':
    try:
        # Initialize curses
        screen = curses.initscr()
        # Turn off echoing of keys, and enter cbreak mode,
        # where no buffering is performed on keyboard input
        curses.noecho()
        curses.cbreak()

        # In keypad mode, escape sequences for special keys
        # (like the cursor keys) will be interpreted and
        # a special value like curses.KEY_LEFT will be returned
        screen.keypad(1)

        # Enter the main loop
        main()                    
        # Set everything back to normal
        screen.keypad(0)
        curses.echo()
        curses.nocbreak()
        # Terminate curses
        curses.endwin()                 
    except:
        # In event of error, restore terminal to sane state.
        screen.keypad(0)
        curses.echo()
        curses.nocbreak()
        curses.endwin()
        traceback.print_exc()           # Print the exception
