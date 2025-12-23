import pyautogui
import time
import keyboard

from screen_coords import *
from screen_navigation import *

GAMEPATH = r"C:\Program Files (x86)\Steam\steamapps\common\BloonsTD6\BloonsTD6.exe"
COMMAND = [GAMEPATH, "arg1", "arg2"]


def debugCursorGetScreenPositions():
    print(
        'listening for "-" key to record cursor position. Press "-" to record position'
    )
    i = 0
    points = {}
    while i < 20:
        keyboard.wait("-")
        points[i] = pyautogui.position()
        print(points[i], i)
        i += 1
    print(points)


def runScript():
    selectLanguage("ch")
    moveAndClick(COORDS["play"])
    selectMap("infernal", "hard", "alternate bloons rounds")
    time.sleep(3)
    returnToMenu()
    time.sleep(3)
    selectLanguage("en")


class Tower:
    def __init__(self, name, position, id):
        self.name = name
        self.position = position
        self.id = id
        self.upgrades = {"top": 0, "mid": 0, "bot": 0}


# displayInGameCash()
# debugCursorGetScreenPositions()
# runScript()

# process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
