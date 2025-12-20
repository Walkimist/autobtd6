import pyautogui
import time
import keyboard
import easyocr
import warnings

from resources.screen_coords import *
from resources.UI_navigation import *

warnings.filterwarnings("ignore", message=".*pin_memory.*")

GAMEPATH = r"C:\Program Files (x86)\Steam\steamapps\common\BloonsTD6\BloonsTD6.exe"
COMMAND = [GAMEPATH, "arg1", "arg2"]


def debugCursorGetScreenPositions():
    i = 0
    points = {}
    key = ""
    while i < 10:
        key = keyboard.read_hotkey()
        if key == "-":
            points[i] = pyautogui.position()
            print(points[i], i)
            i += 1
    print(points)


def displayInGameCash():
    reader = easyocr.Reader(["en"], gpu=False)
    while True:
        pyautogui.screenshot("money_region.png", region=MONEY_AREA)
        text = reader.readtext("money_region.png", detail=0, allowlist="0123456789")
        if len(text) > 0:
            print(text[0])


def runScript():
    selectLanguage("ch")
    moveAndClick(COORDS["play"])
    selectMap("infernal", "hard", "alternate bloons rounds")
    time.sleep(3)
    returnToMenu()
    time.sleep(3)
    selectLanguage("en")


# displayInGameCash()
# debugCursorGetScreenPositions()
# runScript()

# process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
