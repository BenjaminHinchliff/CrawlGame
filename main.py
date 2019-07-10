# standard modules
import time
import copy
import enum
import os
import termcolor as tm

# local modules
import misc
import json
from pos import Pos
import level as lvl
import player as play
import monsters as mon

# processes input if and when the player does stuff
def processPlayerInput(input: str, player: play.Player, level: lvl.Level, monsterState: list) -> None:
    if  (input == "list"):
        misc.clearTerminal()
        print("Type w, s, a, and d to move up, down, left, and right, respectively (but you have to press enter to actually move)")
        print("Type \"pickup\" to pickup an item that you are over, and \"exit\" to leave the game.")
        misc.pauseTerminal()
    elif(input == "pickup"):
        player.pickupItem()
    else:
        for char in input:
            lastX, lastY = player.getPos()
            if  (char == 'w' or char == '8'):
                player.move(play.Player.Direction.UP)
            elif(char == 's' or char == '2'):
                player.move(play.Player.Direction.DOWN)
            elif(char == 'a' or char == '4'):
                player.move(play.Player.Direction.LEFT)
            elif(char == 'd' or char == '6'):
                player.move(play.Player.Direction.RIGHT)
            elif(char == '7'):
                player.move(play.Player.Direction.UP)
                player.move(play.Player.Direction.LEFT)
            elif(char == '9'):
                player.move(play.Player.Direction.UP)
                player.move(play.Player.Direction.RIGHT)
            elif(char == '3'):
                player.move(play.Player.Direction.DOWN)
                player.move(play.Player.Direction.RIGHT)
            elif(char == '1'):
                player.move(play.Player.Direction.DOWN)
                player.move(play.Player.Direction.LEFT)

            anEntity = misc.entityIsOn(player, monsterState)
            if(level.isAtSolid(player)):
                player.setPos(play.Pos(lastX, lastY))
            elif(anEntity):
                player.setPos(play.Pos(lastX, lastY))
                player.attack(anEntity)
            mon.checkTriggers(player, monsterState)
            mon.updateMonsters(player, monsterState)

# main code
def main() -> int:
    items = json.loads(open("data/items.json").read())["items"]
    monsters = []
    testLevel = lvl.Level("data/level.lvls", items, monsters)
    player = play.Player(play.Pos(2,2), items)
    command = None
    win = False
    while(command != "exit" and player.health >= 0 and not win):
        misc.clearTerminal()
        testLevel.print(player)
        player.printStats()
        command = input("Enter a command (list to list them): ")
        processPlayerInput(command, player, testLevel, monsters)
        win = player.damage > 3 and not monsters
    if(win):
        misc.clearTerminal()
        tm.cprint("Congrats! You rescued the lord from the dungeon!")
    return 0

main()