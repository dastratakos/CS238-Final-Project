from enum import Enum

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
VELOCITY_JUMP_PAD = 15
VELOCITY_JUMP_ORB = 8

# Levels
LEVELS = [
    {"name": "Stereo Madness", "filename": "maps/1.csv"},
    {"name": "Back on Track", "filename": "maps/2-easy.csv"},
    {"name": "Polargeist", "filename": "maps/3.csv"},
    {"name": "Dry Out", "filename": "maps/4.csv"},
    {"name": "Base After Base", "filename": "maps/5.csv"},
    {"name": "Portals", "filename": "maps/portals.csv"},
    {"name": "Portals Simple", "filename": "maps/portals-simple.csv"},
    {"name": "Portals End", "filename": "maps/portals-end.csv"},
    {"name": "SM Section 1", "filename": "maps/1-section1.csv"},
    {"name": "SM Section 534", "filename": "maps/1-section_534-866.csv"},
    {"name": "SM Section 680", "filename": "maps/1-section_680-866.csv"},
]

# Palette
PALETTE = [
    (246, 213, 207),
    (238, 132, 128),
    (235, 77, 68),
    (234, 51, 35),
    (244, 188, 125),
    (242, 164, 84),
    (238, 132, 50),
    (235, 89, 41),
    (255, 255, 199),
    (254, 250, 144),
    (255, 255, 84),
    (125, 125, 36),
    (205, 253, 170),
    (194, 253, 129),
    (159, 252, 78),
    (117, 251, 76),
    (137, 25, 16),
    (102, 16, 9),
    (74, 11, 4),
    (50, 5, 7),
    (163, 81, 29),
    (154, 101, 75),
    (110, 75, 57),
    (81, 54, 42),
    (248, 225, 168),
    (244, 188, 64),
    (142, 102, 32),
    (75, 51, 21),
    (219, 254, 94),
    (102, 173, 50),
    (111, 148, 43),
    (78, 172, 87),
    (160, 31, 75),
    (121, 81, 80),
    (113, 57, 55),
    (75, 38, 37),
    (138, 57, 21),
    (95, 51, 34),
    (84, 42, 10),
    (66, 34, 6),
    (198, 166, 124),
    (160, 125, 84),
    (105, 84, 60),
    (78, 62, 44),
    (117, 251, 139),
    (65, 147, 40),
    (39, 94, 22),
    (23, 63, 12),
    (205, 253, 226),
    (173, 252, 229),
    (117, 251, 196),
    (117, 251, 253),
    (182, 253, 254),
    (90, 197, 250),
    (53, 123, 246),
    (0, 0, 245),
    (188, 181, 250),
    (125, 125, 247),
    (114, 19, 245),
    (91, 13, 144),
    (241, 184, 250),
    (234, 51, 124),
    (137, 25, 97),
    (93, 16, 60),
    (159, 252, 182),
    (93, 159, 139),
    (64, 107, 95),
    (49, 83, 73),
    (29, 73, 169),
    (0, 0, 143),
    (2, 6, 107),
    (1, 9, 72),
    (174, 130, 247),
    (68, 7, 168),
    (55, 10, 134),
    (50, 11, 92),
    (234, 51, 247),
    (169, 34, 246),
    (114, 19, 120),
    (64, 7, 50),
    (65, 147, 104),
    (53, 123, 124),
    (39, 94, 95),
    (23, 63, 63),
    (41, 98, 146),
    (28, 71, 106),
    (17, 49, 73),
    (11, 37, 54),
    (77, 77, 138),
    (105, 74, 159),
    (79, 55, 123),
    (62, 43, 95),
    (234, 133, 248),
    (163, 91, 170),
    (121, 70, 126),
    (88, 51, 91),
]


class CollisionType(Enum):
    NONE = 1
    SOLID = 2
    SOLID_TOP = 3
    SOLID_BOTTOM = 4
    SPIKE = 5
    PORTAL_FLY_START = 6
    PORTAL_FLY_END = 7
    PORTAL_GRAVITY_REVERSE = 8
    PORTAL_GRAVITY_NORMAL = 9
    JUMP_PAD = 10
    JUMP_ORB = 11
    END = 12


# Elements
ELEMENTS = {
    "0": {
        "name": "Empty",
        "filename": "",
        "collision_type": CollisionType.NONE,
    },
    "1": {
        "name": "square",
        "filename": "assets/elements/element-1.png",
        "collision_type": CollisionType.SOLID,
    },
    "2": {
        "name": "spike",
        "filename": "assets/elements/element-2.png",
        "collision_type": CollisionType.SPIKE,
    },
    "3": {
        "name": "spike short",
        "filename": "assets/elements/element-3.png",
        "collision_type": CollisionType.SPIKE,
    },
    "4": {
        "name": "grid top",
        "filename": "assets/elements/element-4.png",
        "collision_type": CollisionType.SOLID,
    },
    "5": {
        "name": "grid right",
        "filename": "assets/elements/element-5.png",
        "collision_type": CollisionType.SOLID,
    },
    "6": {
        "name": "grid top right",
        "filename": "assets/elements/element-6.png",
        "collision_type": CollisionType.SOLID,
    },
    "7": {
        "name": "grid bottom",
        "filename": "assets/elements/element-7.png",
        "collision_type": CollisionType.SOLID,
    },
    "8": {
        "name": "grid top bottom",
        "filename": "assets/elements/element-8.png",
        "collision_type": CollisionType.SOLID,
    },
    "9": {
        "name": "grid bottom right",
        "filename": "assets/elements/element-9.png",
        "collision_type": CollisionType.SOLID,
    },
    "10": {
        "name": "grid top bottom right",
        "filename": "assets/elements/element-10.png",
        "collision_type": CollisionType.SOLID,
    },
    "11": {
        "name": "grid left",
        "filename": "assets/elements/element-11.png",
        "collision_type": CollisionType.SOLID,
    },
    "12": {
        "name": "grid top left",
        "filename": "assets/elements/element-12.png",
        "collision_type": CollisionType.SOLID,
    },
    "13": {
        "name": "grid left right",
        "filename": "assets/elements/element-13.png",
        "collision_type": CollisionType.SOLID,
    },
    "14": {
        "name": "grid top left right",
        "filename": "assets/elements/element-14.png",
        "collision_type": CollisionType.SOLID,
    },
    "15": {
        "name": "grid bottom left",
        "filename": "assets/elements/element-15.png",
        "collision_type": CollisionType.SOLID,
    },
    "16": {
        "name": "grid top bottom left",
        "filename": "assets/elements/element-16.png",
        "collision_type": CollisionType.SOLID,
    },
    "17": {
        "name": "grid bottom left right",
        "filename": "assets/elements/element-17.png",
        "collision_type": CollisionType.SOLID,
    },
    "18": {
        "name": "grid top bottom left right",
        "filename": "assets/elements/element-18.png",
        "collision_type": CollisionType.SOLID,
    },
    "19": {
        "name": "grid",
        "filename": "assets/elements/element-19.png",
        "collision_type": CollisionType.SOLID,
    },
    "20": {
        "name": "platform top",
        "filename": "assets/elements/element-20.png",
        "collision_type": CollisionType.SOLID_TOP,
    },
    "21": {
        "name": "spiky bottom",
        "filename": "assets/elements/element-21.png",
        "collision_type": CollisionType.SPIKE,
    },
    "22": {
        "name": "spiky bottom tall",
        "filename": "assets/elements/element-22.png",
        "collision_type": CollisionType.SPIKE,
    },
    "23": {
        "name": "spike down",
        "filename": "assets/elements/element-23.png",
        "collision_type": CollisionType.SPIKE,
    },
    "24": {
        "name": "chain bottom",
        "filename": "assets/elements/element-24.png",
        "collision_type": CollisionType.NONE,
    },
    "25": {
        "name": "chain middle",
        "filename": "assets/elements/element-25.png",
        "collision_type": CollisionType.NONE,
    },
    "26": {
        "name": "chain top",
        "filename": "assets/elements/element-26.png",
        "collision_type": CollisionType.NONE,
    },
    "27": {
        "name": "platform top spiky bottom",
        "filename": "assets/elements/element-27.png",
        "collision_type": CollisionType.SOLID,
    },
    "28": {
        "name": "grid left platform top",
        "filename": "assets/elements/element-28.png",
        "collision_type": CollisionType.SOLID,
    },
    "29": {
        "name": "grid platform top",
        "filename": "assets/elements/element-29.png",
        "collision_type": CollisionType.SOLID,
    },
    "30": {
        "name": "grid right platform top",
        "filename": "assets/elements/element-30.png",
        "collision_type": CollisionType.SOLID,
    },
    "31": {
        "name": "portal fly exit",
        "filename": "assets/elements/element-31.png",
        "collision_type": CollisionType.PORTAL_FLY_END,
    },
    "32": {
        "name": "portal fly entrance",
        "filename": "assets/elements/element-32.png",
        "collision_type": CollisionType.PORTAL_FLY_START,
    },
    "33": {
        "name": "jump pad",
        "filename": "assets/elements/element-33.png",
        "collision_type": CollisionType.JUMP_PAD,
    },
    "34": {
        "name": "jump orb",
        "filename": "assets/elements/element-34.png",
        "collision_type": CollisionType.JUMP_ORB,
    },
    "35": {
        "name": "PortalInvert",
        "filename": "assets/elements/element-35.png",
        "collision_type": CollisionType.PORTAL_GRAVITY_REVERSE,
    },  #
    "36": {
        "name": "PortalRevert",
        "filename": "assets/elements/element-36.png",
        "collision_type": CollisionType.PORTAL_GRAVITY_NORMAL,
    },  #
    "37": {
        "name": "grid empty",
        "filename": "assets/elements/element-19.png",
        "collision_type": CollisionType.NONE,
    },
    "38": {
        "name": "spike left",
        "filename": "assets/elements/element-38.png",
        "collision_type": CollisionType.SPIKE,
    },
    "39": {
        "name": "spike right",
        "filename": "assets/elements/element-39.png",
        "collision_type": CollisionType.SPIKE,
    },
    "40": {
        "name": "spike short down",
        "filename": "assets/elements/element-40.png",
        "collision_type": CollisionType.SPIKE,
    },
    "41": {
        "name": "SpikeGround0Down",
        "filename": "assets/elements/element-41.png",
        "collision_type": CollisionType.SPIKE,
    },
    "42": {
        "name": "SpikeGround1Down",
        "filename": "assets/elements/element-42.png",
        "collision_type": CollisionType.SPIKE,
    },
    "43": {
        "name": "PlatformBottom",
        "filename": "assets/elements/element-43.png",
        "collision_type": CollisionType.SOLID_BOTTOM,
    },
    "44": {
        "name": "end",
        "filename": "assets/elements/element-11.png",
        "collision_type": CollisionType.END,
    },
}
