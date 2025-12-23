import pyautogui
import time
import keyboard

from screen_coords import *
from screen_navigation import *
from command_parser import *
from game_functions import *

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


def startGame():
    selectLanguage("ch")
    moveAndClick(COORDS["play"])
    selectMap(mapInfo['name'], mapInfo['difficulty'], mapInfo["gamemode"])
    time.sleep(4)
    closeGamemodePopup()
    

class Tower:
    def __init__(self, name, position, id):
        self.name = name
        self.position = position
        self.id = id
        self.upgrades = {"top": 0, "mid": 0, "bot": 0}

#debugCursorGetScreenPositions()
#time.sleep(10000)

mapInfo = {'name': 'infernal', 'difficulty': 'hard', 'gamemode': 'chimps'}

mapPath = f'maps/{mapInfo['name']}-{mapInfo['difficulty']}-{mapInfo["gamemode"]}.abtd'
with open(mapPath, "r") as f:
    content = f.read()
splitContent = content.split('\n')

towerPositions = parsePositions(splitContent)
scriptCommands = parseCommands(splitContent)

towers = []
time.sleep(3)
startGame()

currentPosition = 0
for i, command in enumerate(scriptCommands):
    print(f'Command {i}: {command['name']}, {command['type']}\nPosition: {towerPositions[currentPosition]}, Position ID: {currentPosition}')
    currentMoney = getCurrentMoney()
    while currentMoney < getPurchasePrice(command, mapInfo['difficulty'], towers):
        print(f'Price: {getPurchasePrice(command, mapInfo['difficulty'], towers)}, Current: {currentMoney}')
        time.sleep(0.5)
        currentMoney = getCurrentMoney()
    time.sleep(0.5)
    if command['type'] == 'B':
        buyTower(command['name'], towerPositions[currentPosition])
        t = Tower(command['name'], towerPositions[currentPosition], command['id'])
        towers.append(t)
        if currentPosition + 1 < len(towerPositions):
            currentPosition += 1
    if command['type'] == 'U':
        upgradeTower(getTower(towers, command).position, command['path'])
        getTower(towers, command).upgrades[command['path']] += 1
        print(getTower(towers, command).upgrades)
    if command['type'] == 'M':
        changeTargeting(getTower(towers, command).position, command['mode'])
    if currentPosition < 2:
        startRounds()

# process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
