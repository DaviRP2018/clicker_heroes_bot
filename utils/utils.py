import time
from ctypes import windll

import pyautogui

from settings.settings import *


def calibrate_colors():
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


def calibrate_positions():
    """ Calibrate positions """
    print('Press Ctrl-C to quit.')
    try:
        while True:
            x, y = pyautogui.position()
            positionStr = 'X: ' + str(x).rjust(4) + ' Y: ' + str(y).rjust(4)
            print(positionStr, end='')
            print('\b' * len(positionStr), end='', flush=True)
    except KeyboardInterrupt:
        return


def scroll_hero_up_maximum():
    pyautogui.click(SCROLL_HERO_UP_MAXIMUM_POS[0], SCROLL_HERO_UP_MAXIMUM_POS[1])


def scroll_hero_down_maximum():
    pyautogui.click(SCROLL_HERO_DOWN_MAXIMUM_POS[0], SCROLL_HERO_DOWN_MAXIMUM_POS[1])


def scroll_hero_down():
    pyautogui.click(SCROLL_HERO_DOWN_POS[0], SCROLL_HERO_DOWN_POS[1])


def get_color(x, y):
    """ Return a list containing the RGB of a given position """
    dc = windll.user32.GetDC(0)
    rgb = windll.gdi32.GetPixel(dc, x, y)
    r = rgb & 0xff
    g = (rgb >> 8) & 0xff
    b = (rgb >> 16) & 0xff
    return [r, g, b]


def upgrade_all():
    scroll_hero_up_maximum()
    time.sleep(1/2)
    scroll_hero_down_maximum()
    time.sleep(1/2)
    # Check if button is where it is supposed to be
    if get_color(HERO_BUY_ALL_UPGRADES_POS[0], HERO_BUY_ALL_UPGRADES_POS[1]) == HERO_BUY_ALL_UPGRADES_COLOR:
        pyautogui.click(HERO_BUY_ALL_UPGRADES_POS[0], HERO_BUY_ALL_UPGRADES_POS[1])
    else:
        time.sleep(5)
        upgrade_all()


def hire_all_relevant_heroes():
    scroll_hero_up_maximum()
    time.sleep(1/2)
    # change to hire MAX
    for i in range(0, 5):
        pyautogui.press("t")
        time.sleep(1/2)
    for item in RELEVANT_HEROES_POS_WITH_SCROLLS:
        if isinstance(item, int):
            for i in range(0, item):
                scroll_hero_down()
                time.sleep(1/2)
        else:
            pyautogui.click(item[0], item[1])
            time.sleep(1/2)
    pyautogui.press("t")


def reset_auto_clickers():
    pyautogui.keyDown("c")
    time.sleep(1/2)
    pyautogui.click(AUTO_CLICKER_POS[0], AUTO_CLICKER_POS[1])
    time.sleep(1/2)
    pyautogui.keyDown("c")


def set_auto_clickers_to_damage():
    pyautogui.keyDown("c")
    for i in range(1, NUMBER_OF_AUTO_CLICKERS):
        pyautogui.click(GOLD_PICKUP_POS[1], GOLD_PICKUP_POS[3])
        time.sleep(1)
    pyautogui.keyUp("c")


def set_auto_clicker_hire_hero(hero_pos):
    pyautogui.keyDown("c")
    time.sleep(1/2)
    pyautogui.click(hero_pos[0], hero_pos[1])
    time.sleep(1/2)
    pyautogui.keyDown("c")
