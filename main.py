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
import monsters

# processes input if and when the player does stuff
def processPlayerInput(input: str, player: play.Player, level: lvl.Level, monsterState: monsters.Monsters) -> None:
    # print help page
    if  (input == "list" or input == "help"):
        misc.clearTerminal()
        print("7 8 9\n \\|/\n4-@-6\n /|\\\n1 2 3\nyou have to press enter to actually move, through")
        print("Try to move into an enemy to attack them for the amount of damage that your current weapon does")
        print("Type \"pickup\" to pickup an item that you are over, and \"exit\" to leave the game.")
        misc.pauseTerminal()
    # test for player picking up items
    elif(input == "pickup"):
        player.pickupItem()
    else:
        # process movement input by character
        # ie: www input would move player up by 2
        for char in input:
            # store start location in case the user is
            # moving into a wall or a monster
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
            # move the player back to last position if moving 
            # into a wall or monster, and attack monster
            # test if on a monster
            anEntity = misc.entityIsOn(player, monsterState.getMonsters())
            # test if on a solid
            if(level.isAtSolid(player) or anEntity):
                # move back to last location
                player.setPos(play.Pos(lastX, lastY))
                if(anEntity):
                    player.attack(anEntity)
            # update monsters
            monsterState.checkTriggers(player)
            monsterState.updateMonsters(player)
            # have the player regen 1 health per turn
            player.regenerate(1)

# main code
def main() -> int:
    items = json.loads(open("data/items.json").read())["items"]
    monstersObj = monsters.Monsters("data/monsters.json")
    testLevel = lvl.Level("data/level.lvls", items, monstersObj)
    player = play.Player(play.Pos(2,2), items)
    command = None
    win = False
    while(command != "exit" and player.health >= 0 and not win):
        misc.clearTerminal()
        testLevel.print(player)
        player.printStats()
        monstersObj.printMonsterHealth()
        command = input("Enter a command (list to list them): ")
        processPlayerInput(command, player, testLevel, monstersObj)
        win = player.damage > 3 and not monstersObj.getMonsters()
    if(win):
        misc.clearTerminal()
        tm.cprint("Congrats! You rescued the lord from the dungeon!")
    return 0

main()