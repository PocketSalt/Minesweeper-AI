import json

# difficulty enum
DIFFICULTIES = {
    "BEGINNER" : {"grid_size": 8, "bombs": 10},
    "INTERMEDIATE" : {"grid_size": 16, "bombs": 40},
    "EXPERT" : {"grid_size": 24, "bombs": 99},
}

# player enum
PLAYER = {
    "HUMAN": 0,
    "AI": 1
}

# game state
STATE = {
    "PLAYING": 0,
    "WIN": 1,
    "LOSE": 2
}

# display settings
WIDTH = HEIGHT = 1280
FPS = 1000
MARGIN = 2

#################################################
#####       adjust stuff here manually      #####
#difficulty = "HARD"
#player = 1
#AISpeed = 0.0
#################################################

# read from json instead
with open("config.json") as f:
    cfg = json.load(f)

difficulty = cfg["difficulty"]
player = 0 if cfg["player"] == "HUMAN" else 1
AISpeed = cfg["AISpeed"]