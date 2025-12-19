import pyautogui
import time
import keyboard
import easyocr
import warnings

warnings.filterwarnings("ignore", message=".*pin_memory.*")

COORDS = {'play': [955, 954],
          'slot0': [544, 241], 'slot1': [955, 241], 'slot2': [1390, 254], 'slot3':[544, 569], 'slot4':[955, 569], 'slot5':[1390, 569],
          'nextPage': [1643, 423], 'prevPage': [278, 423],
          'beginner': [580, 977], 'intermediate': [838, 977], 'advanced': [1079, 977], 'expert': [1334, 977],
          'easy': [625, 405], 'medium': [960, 405], 'hard': [1289, 405],
          'standard': [635, 591],
          'top1': [952, 450], 'top2': [1285, 450], 'top3': [1605, 450],
          'bot1': [952, 730], 'bot2': [1285, 730], 'bot3': [1605, 730],
          'settings': [75, 206], 'language': [1063, 710], 'ch': [820, 733], 'back': [76, 55], 'en': [489, 205],
          'home': [844, 839]}

MONEY_AREA = [366, 19, 184, 43]

GAMEMODES = {'standard': 'standard',
             'primary only': 'top1', 'deflation': 'top2',
             'military only': 'top1', 'apopalypse': 'top2', 'reverse': 'bot1',
             'magic monkeys only': 'top1', 'double hp moabs': 'top2', 'half cash': 'top3', 'alternate bloons rounds': 'bot1', 'impoppable': 'bot2', 'chimps': 'bot3'}

MAPS = {"monkey meadow": [0, 0], "in the loop": [0, 1], "three mines 'round": [0, 2], "spa pits": [0, 3], "tinkerton": [0, 4], "tree stump": [0, 5],
        "town center": [1, 0], "middle of the road": [1, 1], "one two tree": [1, 2], "scrapyard": [1, 3], "the cabin": [1, 4], "resort": [1, 5],
        "skates": [2, 0], "lotus island": [2, 1], "candy falls": [2, 2], "winter park": [2, 3], "carved": [2, 4], "park path": [2, 5],
        "alpine run": [3, 0], "frozen over": [3, 1], "cubism": [3, 2], "four circles": [3, 3], "hedge": [3, 4], "end of the road": [3, 5],
        "logs": [4, 0],
        "lost crevasse": [5, 0], "luminous cove": [5, 1], "sulfur springs": [5, 2], "water park": [5, 3], "polyphemus": [5, 4], "covered garden": [5, 5],
        "quarry": [6, 0], "quiet street": [6, 1], "bloonarius prime": [6, 2], "balance": [6, 3], "encrypted": [6, 4], "bazaar": [6, 5],
        "adora's temple": [7, 0], "spring spring": [7, 1], "kartsndarts": [7, 2], "moon landing": [7, 3], "haunted": [7, 4], "downstream": [7, 5],
        "firing range": [8, 0], "cracked": [8, 1], "streambed": [8, 2], "chutes": [8, 3], "rake": [8, 4], "spice islands": [8, 5],
        "sunset gulch": [9, 0], "enchanted glade": [9, 1], "last resort": [9, 2], "ancient portal": [9, 3], "castle revenge": [9, 4], "dark path": [9, 5],
        "erosion": [10, 0], "midnight mansion": [10, 1], "sunken columns": [10, 2], "x factor": [10, 3], "mesa": [10, 4], "geared": [10, 5],
        "spillway": [11, 0], "cargo": [11, 1], "pat's pond": [11, 2], "peninsula": [11, 3], "high finance": [11, 4], "another brick": [11, 5],
        "off the coast": [12, 0], "cornfield": [12, 1], "underground": [12, 2],
        "tricky tracks": [13, 0], "glacial trail": [13, 1], "dark dungeons": [13, 2], "sanctuary": [13, 3], "ravine": [13, 4], "flooded valley": [13, 5],
        "infernal": [14,0], "bloody puddles": [14,1], "workshop": [14,2], "quad": [14,3], "dark castle": [14,4], "muddy puddles": [14,5],
        "#ouch": [15,1]}

GAMEPATH = r"C:\Program Files (x86)\Steam\steamapps\common\BloonsTD6\BloonsTD6.exe"
COMMAND = [GAMEPATH, "arg1", "arg2"]

class MapScript:
    pass

def resetToFirstPage():
    moveAndClick(COORDS['expert'])
    moveAndClick(COORDS['beginner'])

def changePage(amount):
    resetToFirstPage()
    pyautogui.moveTo(COORDS['nextPage'])
    if amount < 0:
        amount = abs(amount)
        pyautogui.moveTo(COORDS['prevPage'])
    
    for i in range(amount):
        pyautogui.click()

def selectDifficulty(difficulty):
    moveAndClick(COORDS[difficulty])

def selectMode(mode):
    moveAndClick(COORDS[GAMEMODES[mode]])

def selectMap(map, difficulty, mode):
    changePage(MAPS[map][0])
    moveAndClick(COORDS[f'slot{MAPS[map][1]}'])
    selectDifficulty(difficulty)
    selectMode(mode)

def selectLanguage(language):
    moveAndClick(COORDS['settings'])
    moveAndClick(COORDS['language'])
    time.sleep(.2)
    moveAndClick(COORDS[language])
    time.sleep(.3)
    moveAndClick(COORDS['back'])
    moveAndClick(COORDS['back'])

def returnToMenu():
    pyautogui.keyDown('esc')
    pyautogui.keyUp('esc')
    time.sleep(.2)
    moveAndClick(COORDS['home'])

def debugCursorGetScreenPositions():
    i = 0
    points = {}
    key = ''
    while i < 10:
        key = keyboard.read_hotkey()
        if key == '-':
            points[i] = pyautogui.position()
            print(points[i], i)
            i += 1
    print(points)

def displayInGameCash():
    reader = easyocr.Reader(['en'], gpu=False)
    while True:
        pyautogui.screenshot('money_region.png', region=MONEY_AREA)
        text = reader.readtext('money_region.png', detail=0, allowlist='0123456789')
        if len(text) > 0:
            print(text[0])

def moveAndClick(pos):
    pyautogui.moveTo(pos)
    pyautogui.click()

def runScript():
    selectLanguage('ch')
    moveAndClick(COORDS['play'])
    selectMap("infernal", 'hard', 'alternate bloons rounds')
    time.sleep(2)
    returnToMenu()
    time.sleep(2)
    selectLanguage('en')

debugCursorGetScreenPositions()

#process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)