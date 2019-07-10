import subprocess

# clears the terminal
def clearTerminal() -> None:
    try:
        subprocess.check_call('clear', stderr = subprocess.DEVNULL, shell = True)
    except subprocess.CalledProcessError:
        subprocess.check_call('cls', shell = True)

# pause the terminal until enter clicked
def pauseTerminal() -> None:
    input("Press enter to continue...")

# finds if two entities are directly adjacent, counting diagonals
def isAdjacentTo(entity1, entity2) -> bool:
    e1X, e1Y = entity1.getPos()
    e2X, e2Y = entity2.getPos()
    # TODO: make this nicer?
    #      find if the monster is on a diagonal        find if the monster is directly adjacent
    return (abs(e1X -   e2X) == 1 and abs(e1Y - e2Y) == 1) or abs(e1X -    e2X) + abs(e1Y - e2Y) == 1

def entityIsOn(mainEntity, compareEntities: list):
    mX, mY = mainEntity.getPos()
    for entity in compareEntities:
        eX, eY = entity.getPos()
        if mX == eX and mY == eY:
            return entity
    return False