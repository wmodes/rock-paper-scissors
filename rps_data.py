"""game_data.py: game data for Rock Paper Scissors"""
__author__      = "Wes Modes (wmodes@gmail.com)"
__copyright__   = "2016, MIT"

# Program Data
# We define all of our data up front rather than in the program logic

# we create a list for indexing into our elements
# useful since dictionaries don't have a fixed order
element_list = ["rock", "paper", "scissors", "lizard", "spock"]

# We create a dictionary of game elements 
ELEMENTS = {
    "rock": {
        "defeats": {
            "scissors": {"how": "crushes"},
            "lizard": {"how": "crushes"}
        },
        "synonyms": ["a rock", "a stone", "a pebble", "a boulder"]
    },
    "paper": {
        "defeats": {
            "rock": {"how": "covers"},
            "spock": {"how": "disproves"}
        },
        "synonyms": ["paper", "parchment"]
    },
    "scissors": {
        "defeats": {
            "paper": {"how": "cuts"},
            "lizard": {"how": "decapitates"}
        },
        "synonyms": ["the scissors", "the sheers", "the clippers"]
    },
    "lizard": {
        "defeats": {
            "paper": {"how": "eats"},
            "spock": {"how": "poisons"}
        },
        "synonyms": ["the lizard", "the tiny dragon"]
    },
    "spock": {
        "defeats": {
            "scissors": {"how": "smashes"},
            "rock": {"how": "vaporizes"}
        },
        "synonyms": ["Spock", "the Vulcan"]
    },
}