#! python3
import json
import time

import keyboard
import pyautogui

from powers.models import Powers
from settings.settings import (
    BOSS_FIGHT_FAIL_INTERVAL,
    BOSS_FIGHT_FAILS_LIMIT,
    FARM_PERIOD_VALUE,
    GOLD_PICKUP_INTERVAL,
    HIRE_LAST_HERO_COOLDOWN_VALUE,
)
from utils.utils import (
    get_color,
    hire_all_relevant_heroes,
    reset_auto_clickers,
    set_auto_clicker_hire_hero,
    set_auto_clickers_to_damage,
    upgrade_all,
)


POWERS = Powers.powers


class Main(object):
    def __init__(self):
        self.farm_mode = False
        self.farm_period_mark = time.time()
        self.hire_last_hero_cooldown_mark = time.time()

        self.boss_fight_fails = 0

        with open("settings/positions.json") as json_file:
            self.positions = json.load(json_file)

        print("Starting in 3 seconds...")
        time.sleep(3)

        # Always start by Dark Ritual
        pyautogui.click(
            x=self.positions["powers"][0],
            y=self.positions["powers"][POWERS[7]["position"]],
        )
        POWERS[7]["cooldown_mark"] = time.time()
        POWERS[7]["cooldown_value"] = (
            POWERS[7]["cooldown_initial"] - 3600
        )  # Reload effect
        pyautogui.click(
            x=self.positions["powers"][0],
            y=self.positions["powers"][POWERS[9]["position"]],
        )  # Reload

        pyautogui.click(
            x=self.positions["powers"][0],
            y=self.positions["powers"][POWERS[8]["position"]],
        )  # Energize
        POWERS[1]["is_powered"] = True
        for i in range(1, 7):
            pyautogui.click(
                x=self.positions["powers"][0],
                y=self.positions["powers"][POWERS[i]["position"]],
            )

    def check_and_use_power(
        self, power_id, power_cooldown, energize_cooldown, reload_cooldown
    ):
        power_name = POWERS[power_id]["name"]
        is_infinite = POWERS[power_id]["is_infinite"]

        if power_cooldown <= 0:
            time.sleep(
                2
            )  # Garante que o poder esteja carregado por conta do lag no jogo
            print("Activated", power_name)
            if (
                not is_infinite or not POWERS[power_id]["is_powered"]
            ) and energize_cooldown <= 0:
                print("Using Energize on", power_name)
                pyautogui.click(
                    x=self.positions["powers"][0],
                    y=self.positions["powers"][8],
                )  # Energize
                POWERS[8]["cooldown_mark"] = time.time()
                POWERS[power_id]["is_powered"] = True
            pyautogui.click(
                x=self.positions["powers"][0],
                y=self.positions["powers"][POWERS[power_id]["position"]],
            )
            if not is_infinite and reload_cooldown <= 0:
                print("Using Reload on", power_name)
                pyautogui.click(
                    x=self.positions["powers"][0],
                    y=self.positions["powers"][9],
                )  # Reload
                POWERS[9]["cooldown_mark"] = time.time()
                POWERS[power_id]["cooldown_mark"] = time.time()
                POWERS[power_id]["cooldown_value"] = POWERS[power_id][
                    "duration"
                ]
            else:
                POWERS[power_id]["cooldown_mark"] = time.time()
                POWERS[power_id]["cooldown_value"] = POWERS[power_id][
                    "cooldown_initial"
                ]

    def output_cooldown(self):
        print(
            """
                {}: {}
                {}: {}
                {}: {}
                {}: {}
                {}: {}
                {}: {}
                {}: {}
                {}: {}
                {}: {}
            """.format(
                POWERS[1]["name"],
                self.clickstorm_cooldown,
                POWERS[2]["name"],
                self.powersurge_cooldown,
                POWERS[3]["name"],
                self.lucky_strikes_cooldown,
                POWERS[4]["name"],
                self.metal_detector_cooldown,
                POWERS[5]["name"],
                self.golden_clicks_cooldown,
                POWERS[6]["name"],
                self.super_clicks_cooldown,
                POWERS[7]["name"],
                self.dark_ritual_cooldown,
                POWERS[8]["name"],
                self.energize_cooldown,
                POWERS[9]["name"],
                self.reload_cooldown,
            )
        )

    def pickup_gold(self):
        for i in range(1, 4):
            pyautogui.moveTo(
                self.positions["gold_pickup"][i],
                self.positions["gold_pickup"][0],
            )
            time.sleep(GOLD_PICKUP_INTERVAL / 1000)

    def ascend(self):
        pyautogui.click(
            self.positions["ascension"][0], self.positions["ascension"][1]
        )
        time.sleep(1)
        pyautogui.click(
            self.positions["ascension_yes_button"][0],
            self.positions["ascension_yes_button"][1],
        )
        time.sleep(3)
        pyautogui.click(
            self.positions["farm_mode"][0], self.positions["farm_mode"][1]
        )
        time.sleep(1)

        pyautogui.click(
            self.positions["gold_pickup"][2],
            self.positions["gold_pickup"][0],
        )
        time.sleep(3)

        # Get new gilds and gild Treebeast
        pyautogui.click(
            self.positions["gild_new"][0], self.positions["gild_new"][1]
        )
        time.sleep(2)
        pyautogui.click(
            self.positions["gild_new"][0], self.positions["gild_new"][1]
        )
        time.sleep(2)
        pyautogui.click(
            self.positions["gild_new_openall"][0],
            self.positions["gild_new_openall"][1],
        )
        time.sleep(2)
        # pyautogui.keyDown("q")
        # pyautogui.click(
        #     self.positions["gild_treebeast"][0], self.positions["gild_treebeast"][1]
        # )
        # time.sleep(1)
        # pyautogui.keyUp("q")
        # pyautogui.click(
        #     self.positions["gild_close"][0], self.positions["gild_close"][1]
        # )

        # Hire relevant heroes
        hire_all_relevant_heroes()
        time.sleep(1)
        upgrade_all()
        time.sleep(1)

        # Put auto-clickers
        set_auto_clickers_to_damage()
        time.sleep(5)
        set_auto_clicker_hire_hero(self.positions["hero_treebeast"])

        # Reset as a new start
        self.__init__()

    def start_bot(self):
        print("Press Ctrl-C to quit.")
        print("Hold P to pause.")
        print("Hold I to get info.")
        try:
            while True:
                while True:
                    cooldown_mark = time.time()

                    farm_period = FARM_PERIOD_VALUE - (
                        cooldown_mark - self.farm_period_mark
                    )
                    hire_last_hero_cooldown = HIRE_LAST_HERO_COOLDOWN_VALUE - (
                        cooldown_mark - self.hire_last_hero_cooldown_mark
                    )
                    rgb = get_color(
                        self.positions["farm_mode"][0],
                        self.positions["farm_mode"][1],
                    )
                    r = rgb[0]
                    if not self.farm_mode and r == 255:
                        if hire_last_hero_cooldown <= 0:
                            print(
                                "Progress stopped. Hiring last hero and assigning auto-clickers"
                            )
                            reset_auto_clickers()
                            time.sleep(1)
                            set_auto_clickers_to_damage()
                            time.sleep(1)
                            set_auto_clicker_hire_hero(
                                self.positions["hero_last_hireable"]
                            )
                            self.hire_last_hero_cooldown_mark = time.time()
                            time.sleep(1)
                        else:
                            print(
                                f"Farm mode enabled, waiting {FARM_PERIOD_VALUE} to disable."
                            )
                            self.farm_mode = True
                            if (
                                cooldown_mark - self.farm_period_mark
                            ) <= BOSS_FIGHT_FAIL_INTERVAL:
                                self.boss_fight_fails += 1
                                if (
                                    self.boss_fight_fails
                                    >= BOSS_FIGHT_FAILS_LIMIT
                                ):
                                    print(
                                        "Progress is not possible. Preparing to ascend"
                                    )
                                    self.ascend()
                                print(
                                    "Progress stopped. Interval of {:.2f}s. Count: {}."
                                    " {} consecutive fails remaining to ascend".format(
                                        cooldown_mark - self.farm_period_mark,
                                        self.boss_fight_fails,
                                        BOSS_FIGHT_FAILS_LIMIT
                                        - self.boss_fight_fails,
                                    )
                                )
                                print("Upgrading all heroes")
                                upgrade_all()
                            else:
                                self.boss_fight_fails = 0
                            self.farm_period_mark = time.time()
                    elif self.farm_mode and farm_period <= 0:
                        print("Farm mode disabled")
                        pyautogui.click(
                            x=self.positions["farm_mode"][0],
                            y=self.positions["farm_mode"][1],
                        )
                        self.farm_mode = False

                    try:
                        # used try so that if user pressed other than the
                        # given key error will not be shown
                        if keyboard.is_pressed("p"):  # if key 'p' is pressed
                            print("Bot stopped, press R to resume")
                            break  # finishing the loop
                        elif keyboard.is_pressed("i"):
                            self.output_cooldown()
                        else:
                            pass
                    except Exception:
                        pass  # if user pressed other than the given key the loop will break

                    self.pickup_gold()

                    self.clickstorm_cooldown = POWERS[1]["cooldown_value"] - (
                        cooldown_mark - POWERS[1]["cooldown_mark"]
                    )
                    self.powersurge_cooldown = POWERS[2]["cooldown_value"] - (
                        cooldown_mark - POWERS[2]["cooldown_mark"]
                    )
                    self.lucky_strikes_cooldown = POWERS[3][
                        "cooldown_value"
                    ] - (cooldown_mark - POWERS[3]["cooldown_mark"])
                    self.metal_detector_cooldown = POWERS[4][
                        "cooldown_value"
                    ] - (cooldown_mark - POWERS[4]["cooldown_mark"])
                    self.golden_clicks_cooldown = POWERS[5][
                        "cooldown_value"
                    ] - (cooldown_mark - POWERS[5]["cooldown_mark"])
                    self.super_clicks_cooldown = POWERS[6][
                        "cooldown_value"
                    ] - (cooldown_mark - POWERS[6]["cooldown_mark"])
                    self.dark_ritual_cooldown = POWERS[7]["cooldown_value"] - (
                        cooldown_mark - POWERS[7]["cooldown_mark"]
                    )
                    self.energize_cooldown = POWERS[8]["cooldown_value"] - (
                        cooldown_mark - POWERS[8]["cooldown_mark"]
                    )
                    self.reload_cooldown = POWERS[9]["cooldown_value"] - (
                        cooldown_mark - POWERS[9]["cooldown_mark"]
                    )

                    self.check_and_use_power(
                        1,
                        self.clickstorm_cooldown,
                        self.energize_cooldown,
                        self.reload_cooldown,
                    )
                    self.check_and_use_power(
                        2,
                        self.powersurge_cooldown,
                        self.energize_cooldown,
                        self.reload_cooldown,
                    )
                    self.check_and_use_power(
                        3,
                        self.lucky_strikes_cooldown,
                        self.energize_cooldown,
                        self.reload_cooldown,
                    )
                    self.check_and_use_power(
                        4,
                        self.metal_detector_cooldown,
                        self.energize_cooldown,
                        self.reload_cooldown,
                    )
                    self.check_and_use_power(
                        5,
                        self.golden_clicks_cooldown,
                        self.energize_cooldown,
                        self.reload_cooldown,
                    )
                    self.check_and_use_power(
                        6,
                        self.super_clicks_cooldown,
                        self.energize_cooldown,
                        self.reload_cooldown,
                    )

                    if (
                        self.dark_ritual_cooldown <= 0
                        and self.reload_cooldown <= 0
                    ):
                        time.sleep(
                            5
                        )  # Garante que o poder esteja carregado por conta do lag no jogo
                        pyautogui.click(
                            x=self.positions["powers"][0],
                            y=self.positions["powers"][POWERS[7]["position"]],
                        )
                        POWERS[7]["cooldown_mark"] = time.time()
                        POWERS[7]["cooldown_value"] = (
                            POWERS[7]["cooldown_initial"] - 3600
                        )  # Reload effect
                        pyautogui.click(
                            x=self.positions["powers"][0],
                            y=self.positions["powers"][POWERS[9]["position"]],
                        )  # Reload
                        POWERS[9]["cooldown_mark"] = time.time()
                keyboard.wait("r")
                print("Bot resumed")
        except KeyboardInterrupt:
            print("\n")
            print("Exiting...")
