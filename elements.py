from enum import Enum


class CollisionType(Enum):
    NONE = 1
    SOLID = 2
    SOLID_TOP = 3
    SOLID_BOTTOM = 4
    SPIKE = 5
    PORTAL = 6
    JUMP_PAD = 7
    JUMP_ORB = 8
    END = 8


class ActionType(Enum):
    NONE = 1
    FLY = 2
    GRAVITY = 3


ELEMENTS = {
    "0": {
        "name": "Air",
        "filename": f"assets/elements/element={0}.png",
        "collision_type": CollisionType.NONE,
        "action_type": ActionType.NONE,
    },
    "1": {
        "name": "Square",
        "filename": f"assets/elements/element={1}.png",
        "collision_type": CollisionType.SOLID,
        "action_type": ActionType.NONE,
    },
    "2": {
        "name": "Spike",
        "filename": f"assets/elements/element={2}.png",
        "collision_type": CollisionType.SPIKE,
        "action_type": ActionType.NONE,
    },
    "3": {
        "name": "ShortSpike0",
        "filename": f"assets/elements/element={3}.png",
        "collision_type": CollisionType.SPIKE,
        "action_type": ActionType.NONE,
    },
    "4": {
        "name": "GridSquare0",
        "filename": f"assets/elements/element={4}.png",
        "collision_type": CollisionType.SOLID,
        "action_type": ActionType.NONE,
    },
    "5": {
        "name": "GridSquare1",
        "filename": f"assets/elements/element={5}.png",
        "collision_type": CollisionType.SOLID,
        "action_type": ActionType.NONE,
    },
    "6": {
        "name": "GridSquare2",
        "filename": f"assets/elements/element={6}.png",
        "collision_type": CollisionType.SOLID,
        "action_type": ActionType.NONE,
    },
    "7": {
        "name": "GridSquare3",
        "filename": f"assets/elements/element={7}.png",
        "collision_type": CollisionType.SOLID,
        "action_type": ActionType.NONE,
    },
    "8": {
        "name": "GridSquare4",
        "filename": f"assets/elements/element={8}.png",
        "collision_type": CollisionType.SOLID,
        "action_type": ActionType.NONE,
    },
    "9": {
        "name": "GridSquare5",
        "filename": f"assets/elements/element={9}.png",
        "collision_type": CollisionType.SOLID,
        "action_type": ActionType.NONE,
    },
    "10": {
        "name": "GridSquare6",
        "filename": f"assets/elements/element={10}.png",
        "collision_type": CollisionType.SOLID,
        "action_type": ActionType.NONE,
    },
    "11": {
        "name": "GridSquare7",
        "filename": f"assets/elements/element={11}.png",
        "collision_type": CollisionType.SOLID,
        "action_type": ActionType.NONE,
    },
    "12": {
        "name": "GridSquare8",
        "filename": f"assets/elements/element={12}.png",
        "collision_type": CollisionType.SOLID,
        "action_type": ActionType.NONE,
    },
    "13": {
        "name": "GridSquare9",
        "filename": f"assets/elements/element={13}.png",
        "collision_type": CollisionType.SOLID,
        "action_type": ActionType.NONE,
    },
    "14": {
        "name": "GridSquare10",
        "filename": f"assets/elements/element={14}.png",
        "collision_type": CollisionType.SOLID,
        "action_type": ActionType.NONE,
    },
    "15": {
        "name": "GridSquare11",
        "filename": f"assets/elements/element={15}.png",
        "collision_type": CollisionType.SOLID,
        "action_type": ActionType.NONE,
    },
    "16": {
        "name": "GridSquare12",
        "filename": f"assets/elements/element={16}.png",
        "collision_type": CollisionType.SOLID,
        "action_type": ActionType.NONE,
    },
    "17": {
        "name": "GridSquare13",
        "filename": f"assets/elements/element={17}.png",
        "collision_type": CollisionType.SOLID,
        "action_type": ActionType.NONE,
    },
    "18": {
        "name": "GridSquare14",
        "filename": f"assets/elements/element={18}.png",
        "collision_type": CollisionType.SOLID,
        "action_type": ActionType.NONE,
    },
    "19": {
        "name": "GridSquare15",
        "filename": f"assets/elements/element={19}.png",
        "collision_type": CollisionType.SOLID,
        "action_type": ActionType.NONE,
    },
    "20": {
        "name": "PlatformTop",
        "filename": f"assets/elements/element={20}.png",
        "collision_type": CollisionType.SOLID_TOP,
        "action_type": ActionType.NONE,
    },
    "21": {
        "name": "SpikeGround0",
        "filename": f"assets/elements/element={21}.png",
        "collision_type": CollisionType.SPIKE,
        "action_type": ActionType.NONE,
    },
    "22": {
        "name": "SpikeGround1",
        "filename": f"assets/elements/element={22}.png",
        "collision_type": CollisionType.SPIKE,
        "action_type": ActionType.NONE,
    },
    "23": {
        "name": "SpikeDown",
        "filename": f"assets/elements/element={23}.png",
        "collision_type": CollisionType.SPIKE,
        "action_type": ActionType.NONE,
    },
    "24": {
        "name": "ChainBottom",
        "filename": f"assets/elements/element={24}.png",
        "collision_type": CollisionType.NONE,
        "action_type": ActionType.NONE,
    },
    "25": {
        "name": "ChainMiddle",
        "filename": f"assets/elements/element={25}.png",
        "collision_type": CollisionType.NONE,
        "action_type": ActionType.NONE,
    },
    "26": {
        "name": "ChainTop",
        "filename": f"assets/elements/element={26}.png",
        "collision_type": CollisionType.NONE,
        "action_type": ActionType.NONE,
    },
    "27": {
        "name": "PlatformTopSpike",
        "filename": f"assets/elements/element={27}.png",
        "collision_type": CollisionType.SOLID,
        "action_type": ActionType.NONE,
    },
    "28": {
        "name": "GridSquare16",
        "filename": f"assets/elements/element={28}.png",
        "collision_type": CollisionType.SOLID,
        "action_type": ActionType.NONE,
    },
    "29": {
        "name": "GridSquare17",
        "filename": f"assets/elements/element={29}.png",
        "collision_type": CollisionType.SOLID,
        "action_type": ActionType.NONE,
    },
    "30": {
        "name": "GridSquare18",
        "filename": f"assets/elements/element={30}.png",
        "collision_type": CollisionType.SOLID,
        "action_type": ActionType.NONE,
    },
    "31": {
        "name": "PortalEntrance",
        "filename": f"assets/elements/element={31}.png",
        "collision_type": CollisionType.PORTAL,
        "action_type": ActionType.FLY,
    },  #
    "32": {
        "name": "PortalExit",
        "filename": f"assets/elements/element={32}.png",
        "collision_type": CollisionType.PORTAL,
        "action_type": ActionType.FLY,
    },  #
    "33": {
        "name": "JumpPad",
        "filename": f"assets/elements/element={33}.png",
        "collision_type": CollisionType.JUMP_PAD,
        "action_type": ActionType.NONE,
    },
    "34": {
        "name": "JumpOrb",
        "filename": f"assets/elements/element={34}.png",
        "collision_type": CollisionType.JUMP_ORB,
        "action_type": ActionType.NONE,
    },  #
    "35": {
        "name": "PortalInvert",
        "filename": f"assets/elements/element={35}.png",
        "collision_type": CollisionType.PORTAL,
        "action_type": ActionType.GRAVITY,
    },  #
    "36": {
        "name": "PortalRevert",
        "filename": f"assets/elements/element={36}.png",
        "collision_type": CollisionType.PORTAL,
        "action_type": ActionType.GRAVITY,
    },  #
    "37": {
        "name": "GridSquare19",
        "filename": f"assets/elements/element={37}.png",
        "collision_type": CollisionType.SOLID_BOTTOM,
        "action_type": ActionType.NONE,
    },  #
    "38": {
        "name": "SpikeLeft",
        "filename": f"assets/elements/element={38}.png",
        "collision_type": CollisionType.SPIKE,
        "action_type": ActionType.NONE,
    },
    "39": {
        "name": "SpikeRight",
        "filename": f"assets/elements/element={39}.png",
        "collision_type": CollisionType.SPIKE,
        "action_type": ActionType.NONE,
    },
    "40": {
        "name": "ShortSpikeDown",
        "filename": f"assets/elements/element={40}.png",
        "collision_type": CollisionType.SPIKE,
        "action_type": ActionType.NONE,
    },
    "41": {
        "name": "SpikeGround0Down",
        "filename": f"assets/elements/element={41}.png",
        "collision_type": CollisionType.SPIKE,
        "action_type": ActionType.NONE,
    },
    "42": {
        "name": "SpikeGround1Down",
        "filename": f"assets/elements/element={42}.png",
        "collision_type": CollisionType.SPIKE,
        "action_type": ActionType.NONE,
    },
    "43": {
        "name": "PlatformBottom",
        "filename": f"assets/elements/element={43}.png",
        "collision_type": CollisionType.SOLID_BOTTOM,
        "action_type": ActionType.NONE,
    },
    "44": {
        "name": "End",
        "filename": f"assets/elements/element={44}.png",
        "collision_type": CollisionType.END,
        "action_type": ActionType.NONE,
    },
}
