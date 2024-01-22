from ctypes import windll

import pyautogui


def manual_calibrate_colors():
    """Calibrate colors"""
    print("Press Ctrl-C to quit.")
    dc = windll.user32.GetDC(0)
    try:
        while True:
            x, y = pyautogui.position()
            rgb = windll.gdi32.GetPixel(dc, x, y)
            r = rgb & 0xFF
            g = (rgb >> 8) & 0xFF
            b = (rgb >> 16) & 0xFF
            color = "{} {} {}".format(r, g, b)
            print(color, end="")
            print("\b" * len(color), end="", flush=True)
    except KeyboardInterrupt:
        return


def manual_calibrate_positions():
    """Calibrate positions"""
    print("Press Ctrl-C to quit.")
    try:
        while True:
            x, y = pyautogui.position()
            position_str = "X: " + str(x).rjust(4) + " Y: " + str(y).rjust(4)
            print(position_str, end="")
            print("\b" * len(position_str), end="", flush=True)
    except KeyboardInterrupt:
        return
