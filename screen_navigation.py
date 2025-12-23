import pyautogui
import time

from screen_coords import COORDS
from maps_and_gamemodes import *


def resetToFirstPage():
    moveAndClick(COORDS["expert"])
    moveAndClick(COORDS["beginner"])


def changePage(amount):
    resetToFirstPage()
    pyautogui.moveTo(COORDS["nextPage"])
    if amount < 0:
        amount = abs(amount)
        pyautogui.moveTo(COORDS["prevPage"])

    for i in range(amount):
        pyautogui.click()


def selectDifficulty(difficulty):
    moveAndClick(COORDS[difficulty])


def selectMode(mode):
    moveAndClick(COORDS[GAMEMODES[mode]])
    closeContinuePopup()


def selectMap(map, difficulty, mode):
    changePage(MAPS[map][0])
    moveAndClick(COORDS[f"slot{MAPS[map][1]}"])
    selectDifficulty(difficulty)
    selectMode(mode)


def selectLanguage(language):
    moveAndClick(COORDS["settings"])
    moveAndClick(COORDS["language"])
    time.sleep(0.2)
    moveAndClick(COORDS[language])
    time.sleep(0.3)
    moveAndClick(COORDS["back"])
    moveAndClick(COORDS["back"])


def returnToMenu():
    pyautogui.keyDown("esc")
    pyautogui.keyUp("esc")
    time.sleep(0.2)
    moveAndClick(COORDS["home"])


def closeContinuePopup():
    moveAndClick(COORDS['continuePopup'])


def closeGamemodePopup():
    moveAndClick(COORDS['gamemodePopup'])


def moveAndClick(pos):
    pyautogui.moveTo(pos)
    pyautogui.click()
