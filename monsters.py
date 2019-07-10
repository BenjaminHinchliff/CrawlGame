# standard modules
import json
import termcolor as tm

# local modules
from pos import Pos
from player import Player
import misc

# base class to derive other monsters from
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
    def __init__(self, startPos: Pos, level: int):
        Monster.__init__(self, "Slime", tm.colored('_', 'green'), startPos, level * 5, 3)

class DemonKing(Monster):
    def __init__(self, startPos: Pos):
        Monster.__init__(self, 'King of Demons', tm.colored('X', 'red'), startPos, 131070, 9)

# class to store the current state of the monsters
class Monsters:
    def __init__(self, monsterConfigFilePath: str):
        self.config = json.loads(open("data/monsters.json").read())["monsters"]
        self.monsters = []

    # get the current state of the monsters list
    def getMonsters(self) -> list:
        return self.monsters

    # check the triggers in the monsters.json file to see if the monster should appear
    def checkTriggers(self, playerState: Player):
        pX, pY = playerState.getPos()
        for configMonster in self.config:
            tX, tY = [int(i) for i in configMonster["trigger"].split()]
            if(pX == tX and pY == tY and not configMonster["spawned"]):
                configMonster["spawned"] = True
                mX, mY = [int(i) for i in configMonster["location"].split()]
                if configMonster["type"] == "Slime":
                    self.monsters.append(Slime(Pos(mX, mY), configMonster["level"]))
                elif configMonster["type"] == "DemonKing":
                    self.monsters.append(DemonKing(Pos(mX, mY)))

    # move all the monsters toward player or delete a dead monster
    def updateMonsters(self, playerState: Player):
        for monster in self.monsters:
            if monster.health <= 0:
                del self.monsters[self.monsters.index(monster)]
            else:
                monster.moveAndAttack(playerState)

    # print the health of all the current monsters that exist
    def printMonsterHealth(self):
        for monster in self.monsters:
            print(
                "%s: %s" % (
                    monster.monsterType,
                    misc.createColoredHealthBar(
                        monster.health,
                        monster.MAX_HEALTH
                    )
                ),
                end=""
            )
        print()