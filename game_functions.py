from tower_info import TOWER_INFO
from screen_navigation import moveAndClick
from screen_coords import MONEY_AREA
from tower_info import TOWER_INFO

import pyautogui
import pydirectinput
import time
import easyocr
import warnings
import numpy as np

PATH = {"top": ",", "mid": ".", "bot": "/"}


warnings.filterwarnings("ignore", message=".*pin_memory.*")
reader = easyocr.Reader(["en"], gpu=True)

def startRounds():
    pydirectinput.press('space', 2)

def buyTower(name, coords):
    print(f"PURCHASING {name} AT {coords}")
    pydirectinput.press(TOWER_INFO[name]["hotkey"])
    moveAndClick(coords)


def upgradeTower(coords, path):
    moveAndClick(coords)
    time.sleep(0.1)
    pydirectinput.press(PATH[path])
    pyautogui.press("esc")


def getCurrentMoney():
    screenshot = pyautogui.screenshot(region=MONEY_AREA)
    img = np.array(screenshot)
    text = reader.readtext(img, detail=0, allowlist="0123456789,")
    money = 0
    if text:
        money = int(text[0].replace(",", ""))
    if type(money) == int:
        return money
    return 0

def changeTargeting(coords, mode):
    moveAndClick(coords)
    for i in range(int(mode)):
        pydirectinput.press('tab')
    pyautogui.press("esc")

def getTower(towers, command):
    for tower in towers:
        if tower.name == command['name'] and tower.id == command['id']:
            return tower

def getPurchasePrice(command, difficulty, towers):
    if command['type'] == 'M':
        return 0
    if command['type'] == 'B':
        return TOWER_INFO[command['name']]['price'][difficulty]
    elif command['type'] == 'U':
        PATH_FORMAT = {'top': 'top', 'mid': 'middle', 'bot': 'bottom'}
        upgradePrice = getTower(towers, command).upgrades[command['path']]
        return TOWER_INFO[command['name']]['upgrades'][PATH_FORMAT[command['path']]][difficulty][upgradePrice]
