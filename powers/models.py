import time

from settings.settings import (BIG_COOLDOWN, CLICKSTORM_DURATION,
                               GOLDEN_CLICKS_DURATION, LUCKY_STRIKES_DURATION,
                               MEDIUM_COOLDOWN, METAL_DETECTOR_DURATION,
                               POWERSURGE_DURATION, SMALL_COOLDOWN,
                               SUPER_CLICKS_DURATION, TINY_COOLDOWN)


class Powers(object):
    powers = {
        1: {
            "name": "Clickstorm",
            "position": 1,
            "duration": CLICKSTORM_DURATION,
            "cooldown_initial": TINY_COOLDOWN,
            "cooldown_value": TINY_COOLDOWN,
            "cooldown_mark": time.time(),
            "is_infinite": CLICKSTORM_DURATION > TINY_COOLDOWN,
            "is_powered": False
        },
        2: {
            "name": "Powersurge",
            "position": 2,
            "duration": POWERSURGE_DURATION,
            "cooldown_initial": TINY_COOLDOWN,
            "cooldown_value": TINY_COOLDOWN,
            "cooldown_mark": time.time(),
            "is_infinite": POWERSURGE_DURATION > TINY_COOLDOWN,
            "is_powered": False
        },
        3: {
            "name": "Lucky Strikes",
            "position": 3,
            "duration": LUCKY_STRIKES_DURATION,
            "cooldown_initial": SMALL_COOLDOWN,
            "cooldown_value": SMALL_COOLDOWN,
            "cooldown_mark": time.time(),
            "is_infinite": LUCKY_STRIKES_DURATION > SMALL_COOLDOWN,
            "is_powered": False
        },
        4: {
            "name": "Metal Detector",
            "position": 4,
            "duration": METAL_DETECTOR_DURATION,
            "cooldown_initial": SMALL_COOLDOWN,
            "cooldown_value": SMALL_COOLDOWN,
            "cooldown_mark": time.time(),
            "is_infinite": METAL_DETECTOR_DURATION > SMALL_COOLDOWN,
            "is_powered": False
        },
        5: {
            "name": "Golden Clicks",
            "position": 5,
            "duration": GOLDEN_CLICKS_DURATION,
            "cooldown_initial": MEDIUM_COOLDOWN,
            "cooldown_value": MEDIUM_COOLDOWN,
            "cooldown_mark": time.time(),
            "is_infinite": GOLDEN_CLICKS_DURATION > MEDIUM_COOLDOWN,
            "is_powered": False
        },
        6: {
            "name": "Super Clicks",
            "position": 7,
            "duration": SUPER_CLICKS_DURATION,
            "cooldown_initial": MEDIUM_COOLDOWN,
            "cooldown_value": MEDIUM_COOLDOWN,
            "cooldown_mark": time.time(),
            "is_infinite": SUPER_CLICKS_DURATION > MEDIUM_COOLDOWN,
            "is_powered": False
        },
        7: {
            "name": "The Dark Ritual",
            "position": 6,
            "duration": None,
            "cooldown_initial": BIG_COOLDOWN,
            "cooldown_value": BIG_COOLDOWN,
            "cooldown_mark": time.time(),
            "is_infinite": False,
            "is_powered": False
        },
        8: {
            "name": "Energize",
            "position": 8,
            "duration": None,
            "cooldown_initial": MEDIUM_COOLDOWN,
            "cooldown_value": MEDIUM_COOLDOWN,
            "cooldown_mark": time.time(),
            "is_infinite": False,
            "is_powered": False
        },
        9: {
            "name": "Reload",
            "position": 9,
            "duration": None,
            "cooldown_initial": MEDIUM_COOLDOWN,
            "cooldown_value": MEDIUM_COOLDOWN,
            "cooldown_mark": time.time(),
            "is_infinite": False,
            "is_powered": False
        }
    }