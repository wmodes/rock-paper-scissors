Rock-Paper-Scissors
===================

The classic game with some extra features, including heuristic computer player strategies. 

Features
--------

Up front the game gives the user some choices to spice things up a bit:

- Do you want to play the computer or another player?
- Do you want to play instant-death, the best 2-out-of-3, or indefinite?
- Do you want to play RPS or Rock-Paper-Scissors-Lizard-Spock?

Considerations
--------------

**When you have a game that relies on guessing against a computer, how to you make sure that the computer is not cheating?**

You can examine the source code, of course, and see that the computer is not looing at the user's response before making a choice.

As much as possible, we try to get the user's response and report the computer's choice at the same time. Just like RPS against another human, we have a countdown to the moment both players (computer and human) report their move.

**If your computer opponent is choosing randomly, is this game any fun?**

In other words, isn't half the fun of RPS trying to outsmart your opponent while they are trying to outsmart you? You find yourself choosing a throw because you suspect the other player is selecting a throw to counter what you think they think you are going to throw.

To that end, the computer player has strategy implemented, both to make it a more challenging opponent, but also so you can waste brain power trying to figure out what the computer thinks you are going to throw.

Design
------
With a program that runs in the terminal, usually we can just print stuff out as it happens. But since we need to accept user input while we are doing a countdown, we needed to use the capability of most terminals to turn off echoed key presses and buffered input. We were originally considering using ``ncurses`` but instead decided to use an ordinary scrolling terminal.

As much as possible, I tried to keep data about the game in a separate module for portability, translatability, and flexibility. 

Strategy
--------
I won't detail the strategy here, but I will say that there are several strategies that the computer uses, even attempting to guess the strategy the player may be using to counter it.

Installation
------------

Simple:

    git clone https://github.com/wmodes/rock-paper-scissors.git
    cd rock-paper-scissors
    python rpc.py

Dependencies
------------

In order to make it as portable as possible, we use only modules that are included with most python distributions:

- os and sys, for various terminal access
- time, for timing responses and the countdown
- textwrap, to print the text nicely
- re, for regular expression matching
- random, for making the text less predictable and for some computer strategy