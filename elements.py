from enum import Enum


class CollisionType(Enum):
    NONE = 1
    SOLID = 2
    SOLID_TOP = 3
    SOLID_BOTTOM = 4
    SPIKE = 5
    PORTAL_FLY_START = 6
    PORTAL_FLY_END = 6
    PORTAL_GRAVITY_REVERSE = 6
    PORTAL_GRAVITY_NORMAL = 6
    JUMP_PAD = 7
    JUMP_ORB = 8
    END = 8


ELEMENTS = {
    "0": {
        "name": "Empty",
        "filename": "",
        "collision_type": CollisionType.NONE,
    },
    "1": {
        "name": "square",
        "filename": f"assets/elements/element-1.png",
        "collision_type": CollisionType.SOLID,
    },
    "2": {
        "name": "spike",
        "filename": f"assets/elements/element-2.png",
        "collision_type": CollisionType.SPIKE,
    },
    "3": {
        "name": "spike short",
        "filename": f"assets/elements/element-3.png",
        "collision_type": CollisionType.SPIKE,
    },
    "4": {
        "name": "grid top",
        "filename": f"assets/elements/element-4.png",
        "collision_type": CollisionType.SOLID,
    },
    "5": {
        "name": "grid right",
        "filename": f"assets/elements/element-5.png",
        "collision_type": CollisionType.SOLID,
    },
    "6": {
        "name": "grid top right",
        "filename": f"assets/elements/element-6.png",
        "collision_type": CollisionType.SOLID,
    },
    "7": {
        "name": "grid bottom",
        "filename": f"assets/elements/element-7.png",
        "collision_type": CollisionType.SOLID,
    },
    "8": {
        "name": "grid top bottom",
        "filename": f"assets/elements/element-8.png",
        "collision_type": CollisionType.SOLID,
    },
    "9": {
        "name": "grid bottom right",
        "filename": f"assets/elements/element-9.png",
        "collision_type": CollisionType.SOLID,
    },
    "10": {
        "name": "grid top bottom right",
        "filename": f"assets/elements/element-10.png",
        "collision_type": CollisionType.SOLID,
    },
    "11": {
        "name": "grid left",
        "filename": f"assets/elements/element-11.png",
        "collision_type": CollisionType.SOLID,
    },
    "12": {
        "name": "grid top left",
        "filename": f"assets/elements/element-12.png",
        "collision_type": CollisionType.SOLID,
    },
    "13": {
        "name": "grid left right",
        "filename": f"assets/elements/element-13.png",
        "collision_type": CollisionType.SOLID,
    },
    "14": {
        "name": "grid top left right",
        "filename": f"assets/elements/element-14.png",
        "collision_type": CollisionType.SOLID,
    },
    "15": {
        "name": "grid bottom left",
        "filename": f"assets/elements/element-15.png",
        "collision_type": CollisionType.SOLID,
    },
    "16": {
        "name": "grid top bottom left",
        "filename": f"assets/elements/element-16.png",
        "collision_type": CollisionType.SOLID,
    },
    "17": {
        "name": "grid bottom left right",
        "filename": f"assets/elements/element-17.png",
        "collision_type": CollisionType.SOLID,
    },
    "18": {
        "name": "grid top bottom left right",
        "filename": f"assets/elements/element-18.png",
        "collision_type": CollisionType.SOLID,
    },
    "19": {
        "name": "grid",
        "filename": f"assets/elements/element-19.png",
        "collision_type": CollisionType.SOLID,
    },
    "20": {
        "name": "platform top",
        "filename": f"assets/elements/element-20.png",
        "collision_type": CollisionType.SOLID_TOP,
    },
    "21": {
        "name": "spiky bottom",
        "filename": f"assets/elements/element-21.png",
        "collision_type": CollisionType.SPIKE,
    },
    "22": {
        "name": "spiky bottom tall",
        "filename": f"assets/elements/element-22.png",
        "collision_type": CollisionType.SPIKE,
    },
    "23": {
        "name": "spike down",
        "filename": f"assets/elements/element-23.png",
        "collision_type": CollisionType.SPIKE,
    },
    "24": {
        "name": "chain bottom",
        "filename": f"assets/elements/element-24.png",
        "collision_type": CollisionType.NONE,
    },
    "25": {
        "name": "chain middle",
        "filename": f"assets/elements/element-25.png",
        "collision_type": CollisionType.NONE,
    },
    "26": {
        "name": "chain top",
        "filename": f"assets/elements/element-26.png",
        "collision_type": CollisionType.NONE,
    },
    "27": {
        "name": "platform top spiky bottom",
        "filename": f"assets/elements/element-27.png",
        "collision_type": CollisionType.SOLID,
    },
    "28": {
        "name": "grid left platform top",
        "filename": f"assets/elements/element-28.png",
        "collision_type": CollisionType.SOLID,
    },
    "29": {
        "name": "grid platform top",
        "filename": f"assets/elements/element-29.png",
        "collision_type": CollisionType.SOLID,
    },
    "30": {
        "name": "grid right platform top",
        "filename": f"assets/elements/element-30.png",
        "collision_type": CollisionType.SOLID,
    },
    "31": {
        "name": "portal fly exit",
        "filename": f"assets/elements/element-31.png",
        "collision_type": CollisionType.PORTAL_FLY_END,
    },
    "32": {
        "name": "portal fly entrance",
        "filename": f"assets/elements/element-32.png",
        "collision_type": CollisionType.PORTAL_FLY_START,
    },
    "33": {
        "name": "jump pad",
        "filename": f"assets/elements/element-33.png",
        "collision_type": CollisionType.JUMP_PAD,
    },
    "34": {
        "name": "jump orb",
        "filename": f"assets/elements/element-34.png",
        "collision_type": CollisionType.JUMP_ORB,
    },
    "35": {
        "name": "PortalInvert",
        "filename": f"assets/elements/element-35.png",
        "collision_type": CollisionType.PORTAL_GRAVITY_REVERSE,
    },  #
    "36": {
        "name": "PortalRevert",
        "filename": f"assets/elements/element-36.png",
        "collision_type": CollisionType.PORTAL_GRAVITY_NORMAL,
    },  #
    "37": {
        "name": "grid empty",
        "filename": f"assets/elements/element-19.png",
        "collision_type": CollisionType.NONE,
    },  #
    "38": {
        "name": "spike left",
        "filename": f"assets/elements/element-38.png",
        "collision_type": CollisionType.SPIKE,
    },
    "39": {
        "name": "spike right",
        "filename": f"assets/elements/element-39.png",
        "collision_type": CollisionType.SPIKE,
    },
    "40": {
        "name": "spike short down",
        "filename": f"assets/elements/element-40.png",
        "collision_type": CollisionType.SPIKE,
    },
    "41": {
        "name": "SpikeGround0Down",
        "filename": f"assets/elements/element-41.png",
        "collision_type": CollisionType.SPIKE,
    },
    "42": {
        "name": "SpikeGround1Down",
        "filename": f"assets/elements/element-42.png",
        "collision_type": CollisionType.SPIKE,
    },
    "43": {
        "name": "PlatformBottom",
        "filename": f"assets/elements/element-43.png",
        "collision_type": CollisionType.SOLID_BOTTOM,
    },
    "44": {
        "name": "end",
        "filename": f"assets/elements/element-11.png",
        "collision_type": CollisionType.END,
    },
}
