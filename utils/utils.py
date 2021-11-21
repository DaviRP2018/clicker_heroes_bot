import json
import time
from ctypes import windll

import keyboard
import pyautogui

from settings.constants import KEYS_POSITIONS
from settings.settings import NUMBER_OF_AUTO_CLICKERS, RELEVANT_HEROES_POS_WITH_SCROLLS


def manual_calibrate_colors():
    """ Calibrate colors """
    print('Press Ctrl-C to quit.')
    dc = windll.user32.GetDC(0)
    try:
        while True:
            x, y = pyautogui.position()
            rgb = windll.gdi32.GetPixel(dc, x, y)
            r = rgb & 0xff
            g = (rgb >> 8) & 0xff
            b = (rgb >> 16) & 0xff
            color = "{} {} {}".format(r, g, b)
            print(color, end='')
            print('\b' * len(color), end='', flush=True)
    except KeyboardInterrupt:
        return


def manual_calibrate_positions():
    """ Calibrate positions """
    print('Press Ctrl-C to quit.')
    try:
        while True:
            x, y = pyautogui.position()
            position_str = 'X: ' + str(x).rjust(4) + ' Y: ' + str(y).rjust(4)
            print(position_str, end='')
            print('\b' * len(position_str), end='', flush=True)
    except KeyboardInterrupt:
        return


def calibrate_colors():
    """Calibrate colors"""
    with open("settings/colors_template.json") as json_file:
        colors = json.load(json_file)
    with open("settings/colors.json", "w") as json_file:
        json_file.truncate()
        print("Press Ctrl-C to quit.")
        print("")
        print("Press 'F' to pick the color.")
        progress = 0
        finish = 1
        dc = windll.user32.GetDC(0)
        try:
            x, y = pyautogui.position()
            colors["hero_buy_all_upgrades"].append(y)
            while progress < finish:
                if keyboard.is_pressed("f"):  # if key 'f' is pressed
                    x, y = pyautogui.position()
                    rgb = windll.gdi32.GetPixel(dc, x, y)
                    r = rgb & 0xFF
                    g = (rgb >> 8) & 0xFF
                    b = (rgb >> 16) & 0xFF
                    colors["hero_buy_all_upgrades"] = (r, g, b)
                    progress += 1
                    print("hero_buy_all_upgrades", colors["hero_buy_all_upgrades"])
                    time.sleep(1)
        except KeyboardInterrupt:
            pass
        json.dump(colors, json_file)
        print("Saved")


def calibrate_gold_pickup(positions):
    print("Defining gold pickup, 3 positions required.")
    progress = 0
    finish = 3
    try:
        x, y = pyautogui.position()
        positions["gold_pickup"].append(y)
        while progress < finish:
            if keyboard.is_pressed("f"):  # if key 'f' is pressed
                x, y = pyautogui.position()
                positions["gold_pickup"].append(x)
                progress += 1
                print("gold_pickup", positions["gold_pickup"])
                time.sleep(1)
    except KeyboardInterrupt:
        pass
    return positions


def calibrate_powers(positions):
    print("Defining powers, 9 positions required.")
    progress = 0
    finish = 9
    try:
        x, y = pyautogui.position()
        positions["powers"].append(x)
        while progress < finish:
            if keyboard.is_pressed("f"):  # if key 'f' is pressed
                x, y = pyautogui.position()
                positions["powers"].append(y)
                progress += 1
                print("powers", positions["powers"])
                time.sleep(1)
    except KeyboardInterrupt:
        pass
    return positions


def calibrate_general(positions, key):
    print(f"Defining {key}")
    progress = 0
    finish = 1
    try:
        while progress < finish:
            if keyboard.is_pressed("f"):  # if key 'f' is pressed
                x, y = pyautogui.position()
                positions[key] = (x, y)
                progress += 1
                print(key, positions[key])
                time.sleep(1)
    except KeyboardInterrupt:
        pass
    return positions


def calibrate_positions():
    """Calibrate positions"""
    with open("settings/positions_template.json") as json_file:
        positions = json.load(json_file)
    with open("settings/positions.json", "w") as json_file:
        json_file.truncate()
        print("Press Ctrl-C to quit.")
        print("")
        print("Press 'F' to pick the position.")
        positions = calibrate_gold_pickup(positions)
        positions = calibrate_powers(positions)
        print("Defining everything else.")
        for key in KEYS_POSITIONS:
            positions = calibrate_general(positions, key)
        json.dump(positions, json_file)
        print("Saved")


def scroll_hero_up_maximum():
    with open("settings/positions.json") as json_file:
        positions = json.load(json_file)
        pyautogui.click(
            positions["scroll_hero_up_maximum"][0],
            positions["scroll_hero_up_maximum"][1],
        )


def scroll_hero_down_maximum():
    with open("settings/positions.json") as json_file:
        positions = json.load(json_file)
        pyautogui.click(
            positions["scroll_hero_down_maximum"][0],
            positions["scroll_hero_down_maximum"][1],
        )


def scroll_hero_down():
    with open("settings/positions.json") as json_file:
        positions = json.load(json_file)
        pyautogui.click(
            positions["scroll_hero_down"][0], positions["scroll_hero_down"][1]
        )


def get_color(x, y):
    """Return a list containing the RGB of a given position"""
    dc = windll.user32.GetDC(0)
    rgb = windll.gdi32.GetPixel(dc, x, y)
    r = rgb & 0xFF
    g = (rgb >> 8) & 0xFF
    b = (rgb >> 16) & 0xFF
    return [r, g, b]


def upgrade_all():
    scroll_hero_up_maximum()
    time.sleep(1 / 2)
    scroll_hero_down_maximum()
    time.sleep(1 / 2)
    # Check if button is where it is supposed to be
    with open("settings/positions.json") as f:
        positions = json.load(f)
        with open("settings/colors.json") as json_file:
            colors = json.load(json_file)
            if (
                    get_color(
                        positions["hero_buy_all_upgrades"][0],
                        positions["hero_buy_all_upgrades"][1],
                    )
                    == colors["hero_buy_all_upgrades"]
            ):
                pyautogui.click(
                    positions["hero_buy_all_upgrades"][0],
                    positions["hero_buy_all_upgrades"][1],
                )
            else:
                time.sleep(5)
                upgrade_all()


def hire_all_relevant_heroes():
    scroll_hero_up_maximum()
    time.sleep(1 / 2)
    # change to hire MAX
    for i in range(0, 5):
        pyautogui.press("t")
        time.sleep(1 / 2)
    for item in RELEVANT_HEROES_POS_WITH_SCROLLS:
        if isinstance(item, int):
            for i in range(0, item):
                scroll_hero_down()
                time.sleep(1 / 2)
        else:
            pyautogui.click(item[0], item[1])
            time.sleep(1 / 2)
    pyautogui.press("t")


def reset_auto_clickers():
    pyautogui.keyDown("c")
    time.sleep(1 / 2)
    with open("settings/positions.json") as json_file:
        positions = json.load(json_file)
        pyautogui.click(positions["auto_clicker"][0], positions["auto_clicker"][1])
    time.sleep(1 / 2)
    pyautogui.keyDown("c")


def set_auto_clickers_to_damage():
    pyautogui.keyDown("c")
    with open("settings/positions.json") as json_file:
        positions = json.load(json_file)
        for i in range(1, NUMBER_OF_AUTO_CLICKERS):
            pyautogui.click(positions["gold_pickup"][1], positions["gold_pickup"][3])
            time.sleep(1)
    pyautogui.keyUp("c")


def set_auto_clicker_hire_hero(hero_pos):
    pyautogui.keyDown("c")
    time.sleep(1 / 2)
    pyautogui.click(hero_pos[0], hero_pos[1])
    time.sleep(1 / 2)
    pyautogui.keyDown("c")
