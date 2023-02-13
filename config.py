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
VELOCITY_JUMP_ORB = 12

# Levels
LEVELS = {
    1: {"name": "Stereo Madness"},
    2: {"name": "Back on Track"},
    3: {"name": "Polargeist"},
    4: {"name": "Dry Out"},
    5: {"name": "Base After Base"},
}
