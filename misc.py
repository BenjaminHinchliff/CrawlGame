# default module imports
import subprocess
import termcolor as tm
import os

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

# test if a comparison entity is on the same tile 
# as any of the entities in the comapreEntities list
def entityIsOn(mainEntity, compareEntities: list):
    mX, mY = mainEntity.getPos()
    for entity in compareEntities:
        eX, eY = entity.getPos()
        if mX == eX and mY == eY:
            return entity
    return False

def createBossHealthBar(health: int, maxHealth: int):
    columns = os.get_terminal_size()[0]
    columns -= 20
    amountFull = health / maxHealth
    return tm.colored(
        "|" + "█" * round(columns * amountFull) + " " * round(columns * (1 - amountFull))  + "|",
        'magenta'
    )

def createColoredHealthBar(health: int, maxHealth: int):
    if(maxHealth > os.get_terminal_size()[0]):
        return createBossHealthBar(health, maxHealth)
    return tm.colored(
        "|" + "█" * health + " " * (maxHealth - health) + "|",
        'green' if(health > maxHealth / 3 * 2) else 'yellow' if(health > maxHealth / 3) else 'red'
    )