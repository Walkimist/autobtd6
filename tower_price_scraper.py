from bs4 import BeautifulSoup
import requests
import re

TOWER_PAGES = [
    "https://www.bloonswiki.com/Dart_Monkey_(BTD6)",
    "https://www.bloonswiki.com/Boomerang_Monkey_(BTD6)",
    "https://www.bloonswiki.com/Bomb_Shooter_(BTD6)",
    "https://www.bloonswiki.com/Tack_Shooter_(BTD6)",
    "https://www.bloonswiki.com/Ice_Monkey_(BTD6)",
    "https://www.bloonswiki.com/Glue_Gunner_(BTD6)",
    "https://www.bloonswiki.com/Desperado_(BTD6)",
    "https://www.bloonswiki.com/Sniper_Monkey_(BTD6)",
    "https://www.bloonswiki.com/Monkey_Sub_(BTD6)",
    "https://www.bloonswiki.com/Monkey_Buccaneer_(BTD6)",
    "https://www.bloonswiki.com/Monkey_Ace_(BTD6)",
    "https://www.bloonswiki.com/Heli_Pilot_(BTD6)",
    "https://www.bloonswiki.com/Mortar_Monkey_(BTD6)",
    "https://www.bloonswiki.com/Dartling_Gunner_(BTD6)",
    "https://www.bloonswiki.com/Wizard_Monkey_(BTD6)",
    "https://www.bloonswiki.com/Super_Monkey_(BTD6)",
    "https://www.bloonswiki.com/Ninja_Monkey_(BTD6)",
    "https://www.bloonswiki.com/Alchemist_(BTD6)",
    "https://www.bloonswiki.com/Druid_(BTD6)",
    "https://www.bloonswiki.com/Mermonkey_(BTD6)",
    "https://www.bloonswiki.com/Banana_Farm_(BTD6)",
    "https://www.bloonswiki.com/Spike_Factory_(BTD6)",
    "https://www.bloonswiki.com/Monkey_Village_(BTD6)",
    "https://www.bloonswiki.com/Engineer_Monkey_(BTD6)",
    "https://www.bloonswiki.com/Beast_Handler_(BTD6)",
]

HERO_PAGES = [
    "https://www.bloonswiki.com/Quincy_(BTD6)",
    "https://www.bloonswiki.com/Gwendolin_(BTD6)",
    "https://www.bloonswiki.com/Striker_Jones_(BTD6)",
    "https://www.bloonswiki.com/Obyn_Greenfoot_(BTD6)",
    "https://www.bloonswiki.com/Captain_Churchill_(BTD6)",
    "https://www.bloonswiki.com/Benjamin_(BTD6)",
    "https://www.bloonswiki.com/Ezili_(BTD6)",
    "https://www.bloonswiki.com/Pat_Fusty_(BTD6)",
    "https://www.bloonswiki.com/Adora_(BTD6)",
    "https://www.bloonswiki.com/Admiral_Brickell_(BTD6)",
    "https://www.bloonswiki.com/Etienne_(BTD6)",
    "https://www.bloonswiki.com/Sauda_(BTD6)",
    "https://www.bloonswiki.com/Psi_(BTD6)",
    "https://www.bloonswiki.com/Geraldo_(BTD6)",
    "https://www.bloonswiki.com/Corvus_(BTD6)",
    "https://www.bloonswiki.com/Rosalia_(BTD6)",
    "https://www.bloonswiki.com/Silas_(BTD6)",
]


def getTowerPrices(html):
    soup = BeautifulSoup(html, "html.parser")
    heading = soup.find("h1", id="firstHeading")
    table = heading.find_next("table", class_="info")

    buyPricesTd = table.find(
        "th", string=lambda s: s and s.strip() == "Cost"
    ).find_next()

    prices = re.findall(r"\$([\d,]+)", buyPricesTd.get_text())
    prices = [int(p.replace(",", "")) for p in prices]
    prices = prices[:4]

    pricing = {}
    for p in prices:
        if p == prices[0]:
            pricing["easy"] = p
        if p == prices[1]:
            pricing["medium"] = p
        if p == prices[2]:
            pricing["hard"] = p
        if p == prices[3]:
            pricing["impoppable"] = p

    return pricing


def getPathDivs(html):
    paths = []
    soup = BeautifulSoup(html, "html.parser")
    h3s = soup.find_all("h3")
    i = 1
    for h3 in h3s:
        p = (
            h3.find("span", id="Path_1")
            or h3.find("span", id="Path_2")
            or h3.find("span", id="Path_3")
        )
        if p:
            paths.append(h3.find("span", id=f"Path_{i}").find_next())
            i += 1

    return paths


def getUpgradeTiersValues(div):
    tables = div.find_all("table", class_="wide-sub")
    tiers = {"easy": [], "medium": [], "hard": [], "impoppable": []}
    for t in tables:
        prices = getUpgradeTableValues(t)
        for i, k in enumerate(tiers.keys()):
            tiers[k].append(prices[i])
    return tiers


def getUpgradeTableValues(table):
    if table.find("table"):
        pricesTr = table.find("table").find_all("tr")[1]

        prices = re.findall(r"\$([\d,]+)", pricesTr.get_text())
        prices = [int(p.replace(",", "")) for p in prices]
    else:
        prices = [5000, 5000, 5000, 5000]
    return prices


def getUpgradePaths(html):
    I_TO_PATH = {0: "top", 1: "middle", 2: "bottom"}

    path = getPathDivs(html)
    paths = {}
    for i, p in enumerate(path):
        paths[I_TO_PATH[i]] = getUpgradeTiersValues(p)

    return paths


def getTowerName(html):
    soup = BeautifulSoup(html, "html.parser")
    heading = soup.find("h1", id="firstHeading")
    table = heading.find_next("table", class_="info")

    th = table.find("th", class_="head")

    name = th.find(string=True, recursive=False)
    return name.strip().lower()


def getTowerHotkey(html):
    soup = BeautifulSoup(html, "html.parser")
    if soup.find("kbd"):
        hotkey = soup.find("kbd").get_text().strip().lower()
    else:
        hotkey = "none"
    return hotkey


def loadTowers():
    d = {}
    for page in TOWER_PAGES:
        url = page
        response = requests.get(url)
        htmlContent = response.text

        d[getTowerName(htmlContent)] = {
            "price": getTowerPrices(htmlContent),
            "upgrades": getUpgradePaths(htmlContent),
            "hotkey": getTowerHotkey(htmlContent),
        }
        print(f"LOADED {getTowerName(htmlContent)}")

    for page in HERO_PAGES:
        url = page
        response = requests.get(url)
        htmlContent = response.text

        d[getTowerName(htmlContent)] = {
            "price": getTowerPrices(htmlContent),
            "hotkey": "u",
        }
        print(f"LOADED {getTowerName(htmlContent)}")

    print(d)


loadTowers()
