Rock-Paper-Scissors
===================

The classic game with some extra features. Terminal-based, but using ``ncurses`` to handle display and user keyboard input.


Features
--------

Up front the game gives the user some choices to spice things up a bit:

- Do you want to play the computer or another player?
- Do you want to play instant-death or the best 2-out-of-3?
- Do you want to play RPS or Rock-Paper-Scissors-Lizard-Spock?

Considerations
--------------

**When you have a game that relies on guessing against a computer, how to you make sure that the computer is not cheating?**

You can examine the source code, of course, and see that the computer is not looing at the user's response before making a choice.

As much as possible, we try to get the user's response and report the computer's choice at the same time. Just like RPS against another human, we have a countdown to the moment both players (computer and human) report their move.

Design
------
With a program that runs in the terminal, usually we can just print stuff out as it happens. But since we need to accept user input while we are doing a countdown and since we need a few separate screen regions to do different things, we need to use a module that makes this easier. The curses program  was originally written in the 1970s to allow us to do complicated things with screens that had very limited capabilities.

This makes our design a bit more challenging. We needed to decide at the beginning how we wanted the screen configured. 

- A key guide at the bottom near the keyboard,
- A window to accept typed responses to the user's configuration of the game,
- A window to display the countdown, and
- A window to display the results of each round

Installation
------------

Simple:

    git clone https://github.com/wmodes/rock-paper-scissors.git
    cd rock-paper-scissors
    python rpc.py

Dependencies
------------

In order to make it as portable as possible, we use only modules that are included with most python distributions:

- curses (the python wrapper for ncurses)
- time, for timing responses and the countdown


