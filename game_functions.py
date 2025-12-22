from tower_info import TOWER_INFO
from screen_navigation import moveAndClick
from screen_coords import MONEY_AREA

import pyautogui
import pydirectinput
import time
import easyocr
import warnings

warnings.filterwarnings("ignore", message=".*pin_memory.*")

PATH = {"top": ",", "mid": ".", "bot": "/"}


def buyTower(name, coords):
    print(f"PURCHASING {name} AT {coords}")
    pydirectinput.press(TOWER_INFO[name]["hotkey"])
    moveAndClick(coords)


def upgradeTower(coords, path):
    moveAndClick(coords)
    pydirectinput.press(PATH[path])
    pyautogui.press("esc")


def getCurrentMoney():
    reader = easyocr.Reader(["en"], gpu=False, verbose=False)
    pyautogui.screenshot("money_region.png", region=MONEY_AREA)
    text = reader.readtext("money_region.png", detail=0, allowlist="0123456789,")
    return int(text[0].replace(",", ""))


while True:
    print(getCurrentMoney())
    time.sleep(1)
