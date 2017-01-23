"""game_data.py: game data for Rock Paper Scissors"""
__author__      = "Wes Modes (wmodes@gmail.com)"
__copyright__   = "2016, MIT"

# Program Data
# We put as much of our data in a separate file rather than in the program logic

# we create a list for indexing into our elements
# useful since dictionaries don't have a fixed order
element_list = ["rock", "paper", "scissors", "lizard", "spock"]

# We create a dictionary of game elements 
ELEMENTS = {
    "rock": {
        "defeats": {
            "scissors": "crushes",
            "lizard": "crushes"
        },
        "ties": "bangs futilely against",
        "synonyms": ["a rock", "a stone", "a pebble", "a boulder"]
    },
    "paper": {
        "defeats": {
            "rock": "covers",
            "spock": "disproves"
        },
        "ties": "flutters against",
        "synonyms": ["paper", "parchment"]
    },
    "scissors": {
        "defeats": {
            "paper": "cuts",
            "lizard": "decapitates"
        },
        "ties": "snip at",
        "synonyms": ["the scissors", "the sheers", "the clippers"]
    },
    "lizard": {
        "defeats": {
            "paper": "eats",
            "spock": "poisons"
        },
        "ties": "bites at",
        "synonyms": ["the lizard", "the tiny dragon"]
    },
    "spock": {
        "defeats": {
            "scissors": "smashes",
            "rock": "vaporizes"
        },
        "ties": "examines",
        "synonyms": ["Spock", "the Vulcan"]
    },
}

# Now we create a dictionary of keys
KEYS = {
    0: ["1", "2", "3", "4", "5"],
    1: ["6", "7", "8", "9", "0"],
}