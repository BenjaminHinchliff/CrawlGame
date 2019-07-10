# standard library imports
import enum
import copy
import json
import misc
import termcolor as tm

# local module imports
from player import Player
import monsters

# class to hold the level data and level's supporting functions
class Level:
    # open the level file and process the data to create the level the user sees
    def __init__(self, pathToLevelFile: list, items: list, monsters: monsters.Monsters):
        self.room = [i.split(" ") for i in open(pathToLevelFile).read().split('\n') ]
        for i, arr in enumerate(self.room):
            # replace all the ` in the load file's array with spaces
            while '`' in arr:
                arr[arr.index('`')] = ' '
            # change the color of all the wall objects to cyan
            for j, item in enumerate(arr):
                if(item == '#'):
                    self.room[i][j] = tm.colored(item, 'cyan')
        
        # store items
        self.items = items
        # store monsters
        self.monsters = monsters

    # test if the player passed into the method is on a wall
    def isAtSolid(self, player: Player) -> bool:
        x, y = player.getPos()
        # has to have tm.colored so that the data actually matches
        return(self.room[y][x] == tm.colored('#', 'cyan'))

    def print(self, player: Player = None) -> None:
        # copy the room by value so that it can be edited
        cRoom = copy.deepcopy(self.room)
        # add items
        for item in self.items:
            if(not item["pickedUp"]):      
                x, y = [int(i) for i in item["location"].split(" ")]
                cRoom[y][x] = tm.colored(item["display"], item["displayColor"])
        # add monsters
        for monster in self.monsters.getMonsters():
            x, y = monster.getPos()
            cRoom[y][x] = monster.display
        # add player
        if(player): 
            x, y = player.getPos()
            cRoom[y][x] = tm.colored('@', 'yellow')
        # print modified room
        for arr in cRoom:
            print(" ".join(arr))