# standard library imports
import enum
import misc
import termcolor as tm

# local module imports
from pos import *

# class to hold the player's data
class Player:
    # enum thing to make things make sense
    # also confuses the outline on my editor
    class Direction(enum.Enum):
        UP = 0
        DOWN = 1
        LEFT = 2
        RIGHT = 3

    # starting player configuration
    def __init__(self, pos: Pos, items: list = None):
        self.pos = pos
        self.items = items or []
        self.health = 20
        self.MAX_HEALTH = 20
        self.damage = 1
        self.weapon = "Fists"
        self.itemColor = 'white'
    
    # get player's position
    def getPos(self) -> Pos:
        return self.pos

    # set player's position
    def setPos(self, pos: Pos) -> bool:
        self.pos = pos

    # move player 1 tile in the selected direction
    def move(self, direction: Direction) -> bool:
        if  (direction == self.Direction.UP):
            self.pos.y -= 1
        elif(direction == self.Direction.DOWN):
            self.pos.y += 1
        elif(direction == self.Direction.LEFT):
            self.pos.x -= 1
        elif(direction == self.Direction.RIGHT):
            self.pos.x += 1
        else:
            raise SyntaxError

    # Try to pickup an item at the player's current location
    def pickupItem(self):
        misc.clearTerminal()
        for item in self.items:
            itemX, itemY = [int(i) for i in item["location"].split(" ")]
            if(self.pos.x == itemX and self.pos.y == itemY):
                print("Picked up: %s.\n%s\nIt does %d damage." % (tm.colored(item["name"], item["displayColor"]), item["flavor"], int(item["damage"])))
                self.damage = int(item["damage"])
                self.weapon = item["name"]
                self.itemColor = item["displayColor"]
                item["pickedUp"] = True
                misc.pauseTerminal()
                return True
        print("An item couldn't be found at this location")
        misc.pauseTerminal()
        return False

    # attack the monster in the monster argument if the player
    # is adjacent
    def attack(self, monster):
        if(misc.isAdjacentTo(self, monster)):
            monster.health -= self.damage

    # print player's health (with a bar), weapon, and their damage
    # to the console
    def printStats(self):
        print(
            "Health: %s Weapon: %s | Damage: %d" % 
            (
                misc.createColoredHealthBar(self.health, self.MAX_HEALTH),
                tm.colored(self.weapon, self.itemColor), self.damage
            )
        )

    # regenerate a certain amount of health
    def regenerate(self, amount: int) -> None:
        if self.health < self.MAX_HEALTH:
            self.health += amount