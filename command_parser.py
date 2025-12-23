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
        if buffer[0] == "M":
            if len(buffer) == 3:
                buffer.append(0)
            commands.append({'type': buffer[0], 'name': buffer[1], 'mode': buffer[2], 'id': int(buffer[3])})
        if buffer[0] == "U":
            if len(buffer) == 3:
                buffer.append(0)
            commands.append({'type': buffer[0], 'name': buffer[1], 'path': buffer[2], 'id': int(buffer[3])})
        elif buffer[0] == "B":
            if len(buffer) == 2:
                buffer.append(0)
            commands.append({'type': buffer[0], 'name': buffer[1], 'id': int(buffer[2])})

    return commands
