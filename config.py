TITLE = "Geometry Dash AI"

# Screen
BLOCK_SIZE = 32
SCREEN_BLOCKS = (25, 18)
SCREEN_SIZE = tuple(x * BLOCK_SIZE for x in SCREEN_BLOCKS)

# Player
GRAVITY = 0.86
VELOCITY_X = 6
VELOCITY_MAX_FALL = 100
VELOCITY_JUMP = 10
VELOCITY_JUMP_PAD = 14
VELOCITY_JUMP_ORB = 8

# Levels
LEVELS = {
    1: {"name": "Stereo Madness", "filename": "maps/1.csv"},
    2: {"name": "Back on Track", "filename": "maps/2.csv"},
    3: {"name": "Polargeist", "filename": "maps/3.csv"},
    4: {"name": "Dry Out", "filename": "maps/4.csv"},
    5: {"name": "Base After Base", "filename": "maps/5.csv"},
}
