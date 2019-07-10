# standard modules
import json
import termcolor as tm

# local modules
from pos import Pos
from player import Player
import misc

class Monster:
    def __init__(self, monsterType: str,  display: str, startPos: Pos, health: int, damage: int):
        self.monsterType = monsterType
        self.display = display
        self.pos = startPos
        self.health = health
        self.MAX_HEALTH = health
        self.damage = damage

    # get the position of the monster
    def getPos(self):
        return (self.pos.x, self.pos.y)

    # move toward the player and attack if required
    def moveAndAttack(self, player: Player):
        pX, pY = player.getPos()
        if(not misc.isAdjacentTo(self, player)):
            if(self.pos.x < pX):
                self.pos.x += 1
            elif(self.pos.x > pX):
                self.pos.x -= 1
            if(self.pos.y < pY):
                self.pos.y += 1
            elif(self.pos.y > pY):
                self.pos.y -= 1
        else:
            player.health -= self.damage

class Slime(Monster):
    def __init__(self, startPos: Pos, health: int):
        Monster.__init__(self, "Slime", tm.colored('_', 'green'), startPos, health, 3)


# TODO: package these methods in a Monsters class and
# store the pointer to the monster list from there
# (if I can be bothered)
monsterConfig = json.loads(open("data/monsters.json").read())["monsters"]

# check the triggers in the monsters.json file to see if the monster should appear
def checkTriggers(playerState: Player, monsters: list):
    pX, pY = playerState.getPos()
    for protoMonster in monsterConfig:
        tX, tY = [int(i) for i in protoMonster["trigger"].split()]
        if(pX == tX and pY == tY):
            print("monster found with type of %s" % (protoMonster["type"]))
            if protoMonster["type"] == "Slime":
                mX, mY = [int(i) for i in protoMonster["location"].split()]
                monsters.append(Slime(Pos(mX, mY), protoMonster["health"]))

# move all the monsters toward player
def updateMonsters(playerState: Player, monsters: list):
    for monster in monsters:
        if monster.health <= 0:
            del monsters[monsters.index(monster)]
        else:
            monster.moveAndAttack(playerState)

# print the health of all the current monsters that exist
def printMonsterHealth(monsters: list):
    for monster in monsters:
        print("%s: %s" % (monster.monsterType, misc.createColoredHealthBar(monster.health, monster.MAX_HEALTH)), end="")
    print()