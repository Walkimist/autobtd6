with open("test.txt", "r") as f:
    content = f.read()

splitContent = content.split("\n")


def parsePositions(content):
    rawPositions = []
    for entry in content:
        if entry == "c:":
            break
        if entry != "p:":
            rawPositions.append(entry)

    positions = []
    for i, pair in enumerate(rawPositions):
        buffer = pair.split(",")
        positions.append([int(buffer[0]), int(buffer[1])])

    return positions


def parseCommands(content):
    isCommand = False
    rawCommands = []
    for entry in content:
        if entry == "c:":
            isCommand = True
        if entry != "c:" and isCommand:
            rawCommands.append(entry)

    commands = []
    for i, command in enumerate(rawCommands):
        buffer = command.split(",")
        if buffer[0] == "U":
            commands.append([buffer[0], buffer[1], int(buffer[2]), int(buffer[3])])
        else:
            commands.append([buffer[0], buffer[1]])

    return commands


p = parsePositions(splitContent)
c = parseCommands(splitContent)

print(p, c)
