# standard library imports
import enum
import copy
import json
import misc
import termcolor as tm

# local module imports
from player import Player

# class to hold the level data and level's supporting functions
class Level:
    # TODO: find the file type
    def __init__(self, pathToLevelFile: list, items: list, monsters: list):
        self.room = [i.split(" ") for i in open(pathToLevelFile).read().split('\n') ]
        # replace all the ` in the load file's array with spaces
        for i, arr in enumerate(self.room):
            while '`' in arr:
                arr[arr.index('`')] = ' '
            for j, item in enumerate(arr):
                if(item == '#'):
                    self.room[i][j] = tm.colored(item, 'cyan')
        
        # store items
        self.items = items
        # store monsters
        self.monsters = monsters

    def isAtSolid(self, player: Player) -> bool:
        x, y = player.getPos()
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
        for monster in self.monsters:
            x, y = monster.getPos()
            cRoom[y][x] = monster.display
        # add player
        if(player): 
            x, y = player.getPos()
            cRoom[y][x] = tm.colored('@', 'yellow')
        # print rendered room
        for arr in cRoom:
            print(" ".join(arr))