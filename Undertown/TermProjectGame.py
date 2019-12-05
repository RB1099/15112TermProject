#CMU Graphics downloaded from http://www.cs.cmu.edu/~112/notes/hw9.html
from cmu_112_graphics import *
from tkinter import *
from PIL import Image
import math, copy, random

def gameDimensions():
    rows=13
    cols=18
    cellSize=40
    margin=40
    return (rows, cols, cellSize, margin)

#Class found at https://medium.com/@nicholas.w.swift/easy-a-star-pathfinding-7e6689c7f7b2
class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position

class Chest(object):
    def __init__(self, row, col):
        self.row=row
        self.col=col
        self.gold=random.randrange(11)
        self.isHeal=random.randrange(2)
        if self.isHeal==1:
            self.heal=random.randrange(1, 6)
        else:
            self.heal=0

class Enemy(object):
    def __init__(self, row, col):
        self.row=row
        self.col=col

class Demon(Enemy):
    def __init__(self, row, col):
        super().__init__(row, col)
        self.color="brown"
        self.health=10

#Pathfinding method found at https://medium.com/@nicholas.w.swift/easy-a-star-pathfinding-7e6689c7f7b2
    def astar(maze, start, end):
        """Returns a list of tuples as a path from the given start to the given end in the given maze"""

        # Create start and end node
        start_node = Node(None, start)
        start_node.g = start_node.h = start_node.f = 0
        end_node = Node(None, end)
        end_node.g = end_node.h = end_node.f = 0

        # Initialize both open and closed list
        open_list = []
        closed_list = []

        # Add the start node
        open_list.append(start_node)

        a=0

        # Loop until you find the end
        while len(open_list) > 0:
            a+=1
            if a == 200:
                if GameMode.path!=None:
                    if len(GameMode.path)<=2:
                        break
                    else:
                        GameMode.path.pop(1)
                        return GameMode.path
                else:
                    break
            # Get the current node
            current_node = open_list[0]
            current_index = 0
            for index, item in enumerate(open_list):
                if item.f < current_node.f:
                    current_node = item
                    current_index = index

            # Pop current off open list, add to closed list
            open_list.pop(current_index)
            closed_list.append(current_node)

            # Found the goal
            if current_node == end_node:
                path = []
                current = current_node
                while current is not None:
                    path.append(current.position)
                    current = current.parent
                return path[::-1] # Return reversed path

            # Generate children
            children = []
            for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]: # Adjacent squares

                # Get node position
                node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

                # Make sure within range
                if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) -1) or node_position[1] < 0:
                    continue

                # Make sure walkable terrain
                if maze[node_position[0]][node_position[1]] != 0:
                    continue

                # Create new node
                new_node = Node(current_node, node_position)

                # Append
                children.append(new_node)

            # Loop through children
            for child in children:

                # Child is on the closed list
                for closed_child in closed_list:
                    if child == closed_child:
                        continue

                # Create the f, g, and h values
                child.g = current_node.g + 1
                child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
                child.f = child.g + child.h

                # Child is already in the open list
                for open_node in open_list:
                    if child == open_node and child.g > open_node.g:
                        continue

                # Add the child to the open list
                open_list.append(child)


class Slime(Enemy):
    def __init__(self, row, col):
        super().__init__(row, col)
        self.color="green"
        self.timerDelay=10000
        self.health=2
    
    def slimeMove(self, playerRow, playerCol):
        oRow=self.row
        oCol=self.col
        if (playerRow-self.row)>0:
            drow=1
        elif (playerRow-self.row)<0:
            drow=-1
        else:
            drow=0
        if (playerCol-self.col)>0:
            dcol=1
        elif (playerCol-self.col)<0:
            dcol=-1
        else:
            dcol=0
            
        if abs(playerRow-self.row)<=1 and abs(playerCol-self.col)<=1:
            self.row-=drow
            self.col-=dcol
            GameMode.health-=5
            if GameMode.health<0:
                GameMode.health=0

        self.row+=drow
        self.col+=dcol

        for i in range(len(GameMode.blocks)):
            for j in range(len(GameMode.blocks[i].block)):
                for c in range(len(GameMode.blocks[i].block[j])):
                    if GameMode.blocks[i].block[j][c]:
                        if self.row==GameMode.blocks[i].row+j and self.col==GameMode.blocks[i].col+c:
                            self.row-=drow
                            self.col-=dcol
    
        for i in range(len(GameMode.slimes)):
            if self!=GameMode.slimes[i] and self.row==GameMode.slimes[i].row and self.col==GameMode.slimes[i].col:
                self.row-=drow
                self.col-=dcol
        for i in range(len(GameMode.skels)):
            if self.row==GameMode.skels[i].row and self.col==GameMode.skels[i].col:
                self.row-=drow
                self.col-=dcol
        for i in range(len(GameMode.boss)):
            if self.row==GameMode.boss[i].row and self.col==GameMode.boss[i].col:
                self.row-=drow
                self.col-=dcol

        

        if self.row==playerRow and self.col==playerCol:
            self.row-=drow
            self.col-=dcol

        if self.row!=oRow or self.col!=oCol:
            GameMode.board[oRow][oCol]=0


    

class Skeleton(Enemy):
    def __init__(self, row, col):
        super().__init__(row, col)
        self.color="white"
        self.health=6
    

    def skelMove(self, playerRow, playerCol):
        oRow=self.row
        oCol=self.col
        if (playerRow-self.row)>0:
            drow=1
        elif (playerRow-self.row)<0:
            drow=-1
        else:
            drow=0
        if (playerCol-self.col)>0:
            dcol=1
        elif (playerCol-self.col)<0:
            dcol=-1
        else:
            dcol=0
            
        if abs(playerRow-self.row)<=1 and abs(playerCol-self.col)<=1:
            self.row-=drow
            self.col-=dcol
            GameMode.health-=10
            if GameMode.health<0:
                GameMode.health=0

        self.row+=drow
        self.col+=dcol

        for i in range(len(GameMode.blocks)):
            for j in range(len(GameMode.blocks[i].block)):
                for c in range(len(GameMode.blocks[i].block[j])):
                    if GameMode.blocks[i].block[j][c]:
                        if self.row==GameMode.blocks[i].row+j and self.col==GameMode.blocks[i].col+c:
                            self.row-=drow
                            self.col-=dcol
    
        for i in range(len(GameMode.slimes)):
            if self.row==GameMode.slimes[i].row and self.col==GameMode.slimes[i].col:
                self.row-=drow
                self.col-=dcol
        for i in range(len(GameMode.skels)):
            if self!=GameMode.skels[i] and self.row==GameMode.skels[i].row and self.col==GameMode.skels[i].col:
                self.row-=drow
                self.col-=dcol
        for i in range(len(GameMode.boss)):
            if self.row==GameMode.boss[i].row and self.col==GameMode.boss[i].col:
                self.row-=drow
                self.col-=dcol
        if self.row==playerRow and self.col==playerCol:
            GameMode.health-=5
            self.row-=drow
            self.col-=dcol
        
        if self.row!=oRow or self.col!=oCol:
            GameMode.board[oRow][oCol]=0

class Dragon(Enemy):
    def __init__(self, row, col):
        super().__init__(row, col)
        self.color="black"
        self.health=10
    
    def dragonMove(self, playerRow, playerCol):
        if (playerRow-self.row)>0:
            drow=1
        elif (playerRow-self.row)<0:
            drow=-1
        else:
            drow=0
        if (playerCol-self.col)>0:
            dcol=1
        elif (playerCol-self.col)<0:
            dcol=-1
        else:
            dcol=0
            
        if abs(playerRow-self.row)<=1 and abs(playerCol-self.col)<=1:
            self.row-=drow
            self.col-=dcol
            GameMode.health-=10
            if GameMode.health<0:
                GameMode.health=0

        self.row+=drow
        self.col+=dcol

        for i in range(len(GameMode.blocks)):
            for j in range(len(GameMode.blocks[i].block)):
                for c in range(len(GameMode.blocks[i].block[j])):
                    if GameMode.blocks[i].block[j][c]:
                        if self.row==GameMode.blocks[i].row+j and self.col==GameMode.blocks[i].col+c:
                            self.row-=drow
                            self.col-=dcol
    
        for i in range(len(GameMode.slimes)):
            if self.row==GameMode.slimes[i].row and self.col==GameMode.slimes[i].col:
                self.row-=drow
                self.col-=dcol
        for i in range(len(GameMode.skels)):
            if self.row==GameMode.skels[i].row and self.col==GameMode.skels[i].col:
                self.row-=drow
                self.col-=dcol
        if self.row==playerRow and self.col==playerCol:
            GameMode.health-=20
            self.row-=drow
            self.col-=dcol

class Block(object):
    def __init__(self, row, col, block):
        self.blockList=[
            [[True]],
            [[True, True]],
            [[True, True],
            [False, True]],
            [[True, True],
            [True, False]],
            [[True, False],
            [True, True]],
            [[False, True],
            [True, True]],
            [[True, True],
            [True, True]]
        ]
        self.color="red"
        self.row=row
        self.col=col
        self.block=self.blockList[block]

    def __repr__(self):
        return str(self.block)

#Modes copied from http://www.cs.cmu.edu/~112/notes/notes-animations-part2.html
class SplashScreenMode(Mode):
    def redrawAll(mode, canvas):
        canvas.create_rectangle(0, 0, mode.width, mode.height, fill="black")
        canvas.create_text(mode.width/2, mode.height/2-100, text="UNDERTOWN", font='Times 60 bold', fill="white")
        canvas.create_text(mode.width/2, mode.height/2+100, text="Press any key to continue", font='Times 40 bold', fill="white")
        canvas.create_text(mode.width/2, mode.height/2+60, text="Press h if you need help during the game", font="Times 40 bold", fill="white")

    def keyPressed(mode, event):
        mode.app.setActiveMode(mode.app.gameMode)

class TransitionMode(Mode):
    def redrawAll(mode, canvas):
        canvas.create_rectangle(0, 0, mode.width, mode.height, fill="black")
    def timerFired(mode):
        GameMode.blocks=[]
        rows, cols, cellSize, margin=gameDimensions()
        GameMode.board=[]
        for row in range(rows):
            GameMode.board+=[[0] * cols]
        roomType=random.randrange(1, 4)
        for i in range(10):
            GameMode.blocks.append(Block(random.randrange(1, 12), random.randrange(1, 17), random.randrange(6)))
            isLegalBlock=False
            #checks if blocks are overlapping
            while isLegalBlock==False:
                isLegalBlock=True
                GameMode.blocks.pop(i)
                GameMode.blocks.append(Block(random.randrange(1, 12), random.randrange(1, 17), random.randrange(6)))
                for i in range(len(GameMode.blocks)-1):
                    for j in range(len(GameMode.blocks[i].block)):
                        for c in range(len(GameMode.blocks[i].block[j])):
                            if GameMode.blocks[i].block[j][c]:
                                if GameMode.blocks[len(GameMode.blocks)-1].row==GameMode.blocks[i].row+j and GameMode.blocks[len(GameMode.blocks)-1].col==GameMode.blocks[i].col+c\
                                    or GameMode.blocks[len(GameMode.blocks)-1].row==GameMode.playerRow and GameMode.blocks[len(GameMode.blocks)-1].col==GameMode.playerCol\
                                        or GameMode.blocks[len(GameMode.blocks)-1].row==6 and GameMode.blocks[len(GameMode.blocks)-1].col==9:
                                    isLegalBlock=False


        GameMode.slimes=[]
        GameMode.skels=[]
        GameMode.boss=[]
        GameMode.treasure=[]
        if roomType==1:
            GameMode.slimes.append(Slime(random.randrange(13), random.randrange(18)))
            GameMode.slimes.append(Slime(random.randrange(13), random.randrange(18)))
            GameMode.treasure.append(Chest(random.randrange(13), random.randrange(18)))
            isLegal=False
            while isLegal==False:
                isLegal=True
                if (GameMode.treasure[0].row!=0 or GameMode.treasure[0].row!=12): 
                    if (GameMode.treasure[0].col==0 or GameMode.treasure[0].col==17):
                        isLegal=True
                    else:
                        isLegal=False
                        GameMode.treasure.pop(0)
                        GameMode.treasure.append(Chest(random.randrange(13), random.randrange(18)))
                elif (GameMode.treasure[0].col!=0 or GameMode.treasure[0].col!=17):
                    if (GameMode.treasure[0].row==0 or GameMode.treasure[0].row==12):
                        isLegal=True
                    else:
                        isLegal=False
                        GameMode.treasure.pop(0)
                        GameMode.treasure.append(Chest(random.randrange(13), random.randrange(18)))
                 
            GameMode.treasure.append(Chest(random.randrange(1, 12), random.randrange(1, 17)))
            isLegal=False
            while isLegal==False:
                isLegal=True
                if (GameMode.treasure[1].row!=0 or GameMode.treasure[1].row!=12): 
                    if (GameMode.treasure[1].col==0 or GameMode.treasure[1].col==17):
                        isLegal=True
                    else:
                        isLegal=False
                        GameMode.treasure.pop(1)
                        GameMode.treasure.append(Chest(random.randrange(13), random.randrange(18)))
                elif (GameMode.treasure[1].col!=0 or GameMode.treasure[1].col!=17):
                    if (GameMode.treasure[1].row==0 or GameMode.treasure[1].row==12):
                        isLegal=True
                    else:
                        isLegal=False
                        GameMode.treasure.pop(1)
                        GameMode.treasure.append(Chest(random.randrange(13), random.randrange(18)))
                elif GameMode.treasure[0]==GameMode.treasure[1]:
                    isLegal=False
                    GameMode.treasure.pop(1)
                    GameMode.treasure.append(Chest(random.randrange(13), random.randrange(18)))
            
            isLegal=False
            while isLegal==False:
                isLegal=True
                GameMode.slimes.pop(1)
                GameMode.slimes.append(Slime(random.randrange(13), random.randrange(18)))
                if GameMode.slimes[0]==GameMode.slimes[1]:
                    isLegal=False
                elif GameMode.slimes[0].row==GameMode.playerRow and GameMode.slimes[0].col==GameMode.playerCol:
                    isLegal=False
                elif GameMode.slimes[1].row==GameMode.playerRow and GameMode.slimes[1].col==GameMode.playerCol:
                    isLegal=False
                
        elif roomType==2:
            GameMode.slimes.append(Slime(random.randrange(1, 12), random.randrange(1, 17)))
            GameMode.slimes.append(Slime(random.randrange(1, 12), random.randrange(1, 17)))
            GameMode.skels.append(Skeleton(random.randrange(1, 12), random.randrange(1, 17)))
            GameMode.skels.append(Skeleton(random.randrange(1, 12), random.randrange(1, 17)))
            GameMode.treasure.append(Chest(random.randrange(13), random.randrange(18)))
            isLegal=False
            while isLegal==False:
                isLegal=True
                if (GameMode.treasure[0].row!=0 or GameMode.treasure[0].row!=12): 
                    if (GameMode.treasure[0].col==0 or GameMode.treasure[0].col==17):
                        isLegal=True
                    else:
                        isLegal=False
                        GameMode.treasure.pop(0)
                        GameMode.treasure.append(Chest(random.randrange(13), random.randrange(18)))
                elif (GameMode.treasure[0].col!=0 or GameMode.treasure[0].col!=17):
                    if (GameMode.treasure[0].row==0 or GameMode.treasure[0].row==12):
                        isLegal=True
                    else:
                        isLegal=False
                        GameMode.treasure.pop(0)
                        GameMode.treasure.append(Chest(random.randrange(13), random.randrange(18)))
                else:
                    for i in range(len(GameMode.blocks)):
                        for j in range(len(GameMode.blocks[i].block)):
                            for c in range(len(GameMode.blocks[i].block[j])):
                                if GameMode.blocks[i].block[j][c]:
                                    if GameMode.blocks[i].row+j==GameMode.treasure[0].row and GameMode.blocks[i].col+c==GameMode.treasure[0].col:
                                        isLegal=False
                                        GameMode.treasure.pop(0)
                                        GameMode.treasure.append(Chest(random.randrange(13), random.randrange(18))) 
            GameMode.treasure.append(Chest(random.randrange(13), random.randrange(18)))
            isLegal=False
            while isLegal==False:
                isLegal=True
                if (GameMode.treasure[1].row!=0 or GameMode.treasure[1].row!=12): 
                    if (GameMode.treasure[1].col==0 or GameMode.treasure[1].col==17):
                        isLegal=True
                    else:
                        isLegal=False
                        GameMode.treasure.pop(1)
                        GameMode.treasure.append(Chest(random.randrange(13), random.randrange(18)))
                elif (GameMode.treasure[1].col!=0 or GameMode.treasure[1].col!=17):
                    if (GameMode.treasure[1].row==0 or GameMode.treasure[1].row==12):
                        isLegal=True
                    else:
                        isLegal=False
                        GameMode.treasure.pop(1)
                        GameMode.treasure.append(Chest(random.randrange(13), random.randrange(18)))
                elif GameMode.treasure[0]==GameMode.treasure[1]:
                    isLegal=False
                    GameMode.treasure.pop(1)
                    GameMode.treasure.append(Chest(random.randrange(13), random.randrange(18)))
                else:
                    for i in range(len(GameMode.blocks)):
                        for j in range(len(GameMode.blocks[i].block)):
                            for c in range(len(GameMode.blocks[i].block[j])):
                                if GameMode.blocks[i].block[j][c]:
                                    if GameMode.blocks[i].row+j==GameMode.treasure[1].row and GameMode.blocks[i].col+c==GameMode.treasure[1].col:
                                        isLegal=False
                                        GameMode.treasure.pop(1)
                                        GameMode.treasure.append(Chest(random.randrange(1, 12), random.randrange(1, 17)))
            #checks for correct placement of monsters
            isLegal=False
            while isLegal==False:
                isLegal=True
                if GameMode.slimes[0]==GameMode.slimes[1]:
                    isLegal=False
                    GameMode.slimes[1]=Slime(random.randrange(1, 12), random.randrange(1, 17))
                elif GameMode.skels[0]==GameMode.skels[1]:
                    isLegal=False
                    GameMode.skels[1]=Skeleton(random.randrange(1, 12), random.randrange(1, 17))
                elif GameMode.skels[0].row ==GameMode.slimes[0].row and GameMode.skels[0].col==GameMode.slimes[0]:
                    isLegal=False
                    GameMode.skels[0]=Skeleton(random.randrange(1, 12), random.randrange(1, 17))
                elif GameMode.skels[0].row==GameMode.slimes[1].row and GameMode.skels[0].col==GameMode.slimes[1].col:
                    isLegal=False
                    GameMode.skels[0]=Skeleton(random.randrange(1, 12), random.randrange(1, 17))
                elif GameMode.skels[1].row==GameMode.slimes[0].row and GameMode.skels[1].col==GameMode.slimes[0].col:
                    isLegal=False
                    GameMode.slimes[0]=Slime(random.randrange(1, 12), random.randrange(1, 17))
                elif GameMode.skels[1].row==GameMode.slimes[1].row and GameMode.skels[1].col==GameMode.slimes[1].col:
                    isLegal=False
                    GameMode.skels[1]=Skeleton(random.randrange(1, 12), random.randrange(1, 17))
                else:
                    for i in range(len(GameMode.blocks)):
                        for j in range(len(GameMode.blocks[i].block)):
                            for c in range(len(GameMode.blocks[i].block[j])):
                                if GameMode.blocks[i].block[j][c]:
                                    if GameMode.blocks[i].row+j==GameMode.slimes[0].row and GameMode.blocks[i].col+c==GameMode.slimes[0].col:
                                        isLegal=False
                                        GameMode.slimes[0]=Slime(random.randrange(1, 12), random.randrange(1, 17))
                                    elif GameMode.blocks[i].row+j==GameMode.slimes[1].row and GameMode.blocks[i].col+c==GameMode.slimes[1].col:
                                        isLegal=False
                                        GameMode.slimes[1]=Slime(random.randrange(1, 12), random.randrange(1, 17))
                                    elif GameMode.blocks[i].row+j==GameMode.skels[0].row and GameMode.blocks[i].col+c==GameMode.skels[0].col:
                                        isLegal=False
                                        GameMode.skels[0]=Skeleton(random.randrange(1, 12), random.randrange(1, 17))
                                    elif GameMode.blocks[i].row+j==GameMode.skels[1].row and GameMode.blocks[i].col+c==GameMode.skels[1].col:
                                        isLegalBlock=False
                                        GameMode.skels[1]=Skeleton(random.randrange(1, 12), random.randrange(1, 17))




        elif roomType==3:
            bossType=random.randrange(1, 3)
            GameMode.slimes.append(Slime(random.randrange(1, 12), random.randrange(1, 17)))
            GameMode.slimes.append(Slime(random.randrange(1, 12), random.randrange(1, 17)))
            GameMode.skels.append(Skeleton(random.randrange(1, 12), random.randrange(1, 17)))
            GameMode.skels.append(Skeleton(random.randrange(1, 12), random.randrange(1, 17)))
            GameMode.blocks=[]
            for i in range(2, 11):
                GameMode.blocks.append(Block(i, 2, 1))
                GameMode.blocks.append(Block(i, 14, 1))
            GameMode.treasure.append(Chest(0, 0))
            GameMode.treasure.append(Chest(0, 3))
            GameMode.treasure.append(Chest(0, 6))
            GameMode.treasure.append(Chest(0, 11))
            GameMode.treasure.append(Chest(0, 14))
            GameMode.treasure.append(Chest(0, 17))
            isLegal=False
            #checks for correct placement of monsters
            while isLegal==False:
                isLegal=True
                if GameMode.slimes[0]==GameMode.slimes[1]:
                    isLegal=False
                    GameMode.slimes[1]=Slime(random.randrange(1, 12), random.randrange(1, 17))
                elif GameMode.skels[0]==GameMode.skels[1]:
                    isLegal=False
                    GameMode.skels[1]=Skeleton(random.randrange(1, 12), random.randrange(1, 17))
                elif GameMode.skels[0].row ==GameMode.slimes[0].row and GameMode.skels[0].col==GameMode.slimes[0]:
                    isLegal=False
                    GameMode.skels[0]=Skeleton(random.randrange(1, 12), random.randrange(1, 17))
                elif GameMode.skels[0].row==GameMode.slimes[1].row and GameMode.skels[0].col==GameMode.slimes[1].col:
                    isLegal=False
                    GameMode.skels[0]=Skeleton(random.randrange(1, 12), random.randrange(1, 17))
                elif GameMode.skels[1].row==GameMode.slimes[0].row and GameMode.skels[1].col==GameMode.slimes[0].col:
                    isLegal=False
                    GameMode.slimes[0]=Slime(random.randrange(1, 12), random.randrange(1, 17))
                elif GameMode.skels[1].row==GameMode.slimes[1].row and GameMode.skels[1].col==GameMode.slimes[1].col:
                    isLegal=False
                    GameMode.skels[1]=Skeleton(random.randrange(1, 12), random.randrange(1, 17))
                elif GameMode.skels[0].row==6 and GameMode.skels[0].col==9:
                    isLegal=False
                    GameMode.skels[0]=Skeleton(random.randrange(1, 12), random.randrange(1, 17))
                elif GameMode.skels[1].row==6 and GameMode.skels[1].col==9:
                    isLegal=False
                    GameMode.skels[1]=Skeleton(random.randrange(1, 12), random.randrange(1, 17))
                elif GameMode.slimes[0].row==6 and GameMode.slimes[0].col==9:
                    isLegal=False
                    GameMode.slimes[0]=Slime(random.randrange(1, 12), random.randrange(1, 17))
                elif GameMode.slimes[1].row==6 and GameMode.slimes[1].col==9:
                    isLegal=False
                    GameMode.slimes[1]=Slime(random.randrange(1, 12), random.randrange(1, 17))
                else:
                    for i in range(len(GameMode.blocks)):
                        for j in range(len(GameMode.blocks[i].block)):
                            for c in range(len(GameMode.blocks[i].block[j])):
                                if GameMode.blocks[i].block[j][c]:
                                    if GameMode.blocks[i].row+j==GameMode.slimes[0].row and GameMode.blocks[i].col+c==GameMode.slimes[0].col:
                                        isLegal=False
                                        GameMode.slimes[0]=Slime(random.randrange(1, 12), random.randrange(1, 17))
                                    elif GameMode.blocks[i].row+j==GameMode.slimes[1].row and GameMode.blocks[i].col+c==GameMode.slimes[1].col:
                                        isLegal=False
                                        GameMode.slimes[1]=Slime(random.randrange(1, 12), random.randrange(1, 17))
                                    elif GameMode.blocks[i].row+j==GameMode.skels[0].row and GameMode.blocks[i].col+c==GameMode.skels[0].col:
                                        isLegal=False
                                        GameMode.skels[0]=Skeleton(random.randrange(1, 12), random.randrange(1, 17))
                                    elif GameMode.blocks[i].row+j==GameMode.skels[1].row and GameMode.blocks[i].col+c==GameMode.skels[1].col:
                                        isLegalBlock=False
                                        GameMode.skels[1]=Skeleton(random.randrange(1, 12), random.randrange(1, 17))
            for i in range(len(GameMode.blocks)):
                for j in range(len(GameMode.blocks[i].block)):
                    for c in range(len(GameMode.blocks[i].block[j])):
                        if GameMode.blocks[i].block[j][c]:
                            GameMode.board[GameMode.blocks[i].row+j][GameMode.blocks[i].col+c]=1
            if bossType==1:
                GameMode.boss.append(Demon(6, 8))
            else:
                GameMode.boss.append(Dragon(6, 8))
            GameMode.path=Demon.astar(GameMode.board, (GameMode.boss[0].row, GameMode.boss[0].col), (GameMode.playerRow, GameMode.playerCol))
        mode.app.setActiveMode(mode.app.gameMode)












class GameMode(Mode):
    blocks=[]
    slimes=[]
    skels=[]
    boss=[]
    treasure=[]
    board=[]
    playerRow=0
    playerCol=0
    health=100
    score=0
    path=[]
    def appStarted(mode):
        mode.background=mode.loadImage('dungeonBackground.png')
        mode.playerRow = 10
        mode.playerCol= 8
        mode.oldRow=10
        mode.oldCol=8
        #Player sprite from http://kidscancode.org/godot_recipes/img/Adventurer%20Sprite%20Sheet%20v1.1.png
        playerURL="http://kidscancode.org/godot_recipes/img/Adventurer%20Sprite%20Sheet%20v1.1.png"
        playerStrip=mode.loadImage(playerURL)
        mode.playerSprite=[]
        mode.spriteCounter=0
        mode.spriteAction=0
        mode.maxSpriteCount=13
        for i in range(8):
            spriteL=[]
            for j in range(13):
                sprite=playerStrip.crop((32*j, 32*i, 32*j+32, 32*i+32))
                spriteL.append(sprite)
                if j==4:
                    mode.playerSprite.append(spriteL)
        #Slime sprite from https://opengameart.org/sites/default/files/slime.jiggle.png
        slimeURL="https://opengameart.org/sites/default/files/slime.jiggle.png"
        slimeStrip=mode.loadImage(slimeURL)
        mode.slimeSprite=[]
        mode.sSpriteCounter=0
        for i in range(8):
            sprite=slimeStrip.crop((64*i, 0, 64*i+64, 64))
            mode.slimeSprite.append(sprite)
        #Skeleton sprite from https://opengameart.org/sites/default/files/skeleton_3.png
        skelURL="https://opengameart.org/sites/default/files/skeleton_3.png"
        skelStrip=mode.loadImage(skelURL)
        mode.skelSprite=[]
        mode.skelCounter=0
        for i in range(7):
            sprite=skelStrip.crop((64*i, 128, 64*i+64, 192))
            mode.skelSprite.append(sprite)
        mode.running=True
        mode.rows, mode.cols, mode.cellSize, mode.margin=gameDimensions()
        GameMode.board=[]
        for row in range(mode.rows):
            GameMode.board+=[[0] * mode.cols]
        mode.lastDirection=[]
    
    blockNums=[random.randrange(6) for i in range(10)]
    for i in range(10):
        blocks.append(Block(random.randrange(1, 12), random.randrange(1, 17), blockNums[i]))
        

    def keyPressed(mode, event):
        if event.key=="h":
            mode.app.setActiveMode(mode.app.helpScreen)
        if event.key=="Right":
            mode.drow=0
            mode.dcol=1
            mode.lastDirection=[mode.drow, mode.dcol]
            mode.movePlayer()
        elif event.key=="Left":
            mode.drow=0
            mode.dcol=-1
            mode.lastDirection=[mode.drow, mode.dcol]
            mode.movePlayer()
        elif event.key=="Down":
            mode.drow=1
            mode.dcol=0
            mode.lastDirection=[mode.drow, mode.dcol]
            mode.movePlayer()
        elif event.key=="Up":
            mode.drow=-1
            mode.dcol=0
            mode.lastDirection=[mode.drow, mode.dcol]
            mode.movePlayer()
        elif event.key=="Space":
            for i in mode.treasure:
                if mode.playerRow+mode.lastDirection[0]==i.row and mode.playerCol+mode.lastDirection[1]==i.col:
                    GameMode.score+=i.gold
                    if GameMode.health!=100:
                        GameMode.health+=i.heal
                    GameMode.treasure.remove(i)
            for slime in mode.slimes:
                if mode.playerRow+mode.lastDirection[0]==slime.row and mode.playerCol+mode.lastDirection[1]==slime.col:
                    mode.spriteCounter=1
                    mode.spriteAction=3
                    mode.maxSpriteCount=10
                    slime.health-=1
                    slime.row+=2*(mode.lastDirection[0])
                    slime.col+=2*(mode.lastDirection[1])
                    for i in range(len(GameMode.blocks)):
                        for j in range(len(GameMode.blocks[i].block)):
                            for c in range(len(GameMode.blocks[i].block[j])):
                                if GameMode.blocks[i].block[j][c]:
                                    if slime.row==GameMode.blocks[i].row+j and slime.col==GameMode.blocks[i].col+c:
                                        slime.row-=mode.lastDirection[0]
                                        slime.col-=mode.lastDirection[1]
                                        for i in range(len(GameMode.blocks)):
                                            for j in range(len(GameMode.blocks[i].block)):
                                                for c in range(len(GameMode.blocks[i].block[j])):
                                                    if GameMode.blocks[i].block[j][c]:
                                                        if slime.row==GameMode.blocks[i].row+j and slime.col==GameMode.blocks[i].col+c:
                                                            slime.row-=mode.lastDirection[0]
                                                            slime.col-=mode.lastDirection[1]
                    if slime.row<=0:
                        slime.row=0
                    if slime.row>=12:
                        slime.row=12
                    if slime.col<=0:
                        slime.col=0
                    if slime.col>=17:
                        slime.col=17

                    if slime.health==0:
                        mode.slimes.remove(slime)
                        GameMode.score+=2
            for skel in mode.skels:
                if mode.playerRow+mode.lastDirection[0]==skel.row and mode.playerCol+mode.lastDirection[1]==skel.col:
                    mode.spriteCounter=1
                    mode.spriteAction=3
                    mode.maxSpriteCount=10
                    skel.health-=1
                    skel.row+=2*(mode.lastDirection[0])
                    skel.col+=2*(mode.lastDirection[1])
                    for i in range(len(GameMode.blocks)):
                        for j in range(len(GameMode.blocks[i].block)):
                            for c in range(len(GameMode.blocks[i].block[j])):
                                if GameMode.blocks[i].block[j][c]:
                                    if skel.row==GameMode.blocks[i].row+j and skel.col==GameMode.blocks[i].col+c:
                                        skel.row-=mode.lastDirection[0]
                                        skel.col-=mode.lastDirection[1]
                                        for i in range(len(GameMode.blocks)):
                                            for j in range(len(GameMode.blocks[i].block)):
                                                for c in range(len(GameMode.blocks[i].block[j])):
                                                    if GameMode.blocks[i].block[j][c]:
                                                        if skel.row==GameMode.blocks[i].row+j and skel.col==GameMode.blocks[i].col+c:
                                                            skel.row-=mode.lastDirection[0]
                                                            skel.col-=mode.lastDirection[1]
                    if skel.row<=0:
                        skel.row=0
                    if skel.row>=12:
                        skel.row=12
                    if skel.col<=0:
                        skel.col=0
                    if skel.col>=17:
                        skel.col=17
                        
                    if skel.health==0:
                        mode.skels.remove(skel)
                        GameMode.score+=4
            for bos in mode.boss:
                if mode.playerRow+mode.lastDirection[0]==bos.row and mode.playerCol+mode.lastDirection[1]==bos.col:
                    mode.spriteCounter=1
                    mode.spriteAction=3
                    mode.maxSpriteCount=10
                    bos.health-=1
                    bos.row+=2*(mode.lastDirection[0])
                    bos.col+=2*(mode.lastDirection[1])
                    for i in range(len(GameMode.blocks)):
                        for j in range(len(GameMode.blocks[i].block)):
                            for c in range(len(GameMode.blocks[i].block[j])):
                                if GameMode.blocks[i].block[j][c]:
                                    if bos.row==GameMode.blocks[i].row+j and bos.col==GameMode.blocks[i].col+c:
                                        bos.row-=mode.lastDirection[0]
                                        bos.col-=mode.lastDirection[1]
                                        for i in range(len(GameMode.blocks)):
                                            for j in range(len(GameMode.blocks[i].block)):
                                                for c in range(len(GameMode.blocks[i].block[j])):
                                                    if GameMode.blocks[i].block[j][c]:
                                                        if bos.row==GameMode.blocks[i].row+j and bos.col==GameMode.blocks[i].col+c:
                                                            bos.row-=mode.lastDirection[0]
                                                            bos.col-=mode.lastDirection[1]
                    if bos.row<=0:
                        bos.row=0
                    if bos.row>=12:
                        bos.row=12
                    if bos.col<=0:
                        bos.col=0
                    if bos.col>=17:
                        bos.col=17

                    if bos.health==0:
                        mode.boss.remove(bos)
                        GameMode.score+=15

    def movePlayer(mode):
        mode.playerRow+=mode.drow
        mode.playerCol+=mode.dcol
        if (mode.playerCol>=7 and mode.playerCol<=10) and mode.playerRow<0:
            mode.playerRow=12
            mode.app.setActiveMode(TransitionMode())
        elif (mode.playerCol>=7 and mode.playerCol<=10) and mode.playerRow>12:
            mode.playerRow=0
            mode.app.setActiveMode(mode.app.transitionMode)
        else:
            if mode.playerRow<=0:
                mode.playerRow=0
            if mode.playerRow>=12:
                mode.playerRow=12
            if mode.playerCol<=0:
                mode.playerCol=0
            if mode.playerCol>=17:
                mode.playerCol=17
            
            for i in range(len(GameMode.blocks)):
                for j in range(len(GameMode.blocks[i].block)):
                    for c in range(len(GameMode.blocks[i].block[j])):
                        if GameMode.blocks[i].block[j][c]:
                            if mode.playerRow==GameMode.blocks[i].row+j and mode.playerCol==GameMode.blocks[i].col+c:
                                mode.playerRow-=mode.drow
                                mode.playerCol-=mode.dcol
            
            for i in range(len(mode.slimes)):
                if mode.playerRow==mode.slimes[i].row and mode.playerCol==mode.slimes[i].col:
                    mode.playerRow-=mode.drow
                    mode.playerCol-=mode.dcol
            for i in range(len(mode.skels)):
                if mode.playerRow==mode.skels[i].row and mode.playerCol==mode.skels[i].col:
                    mode.playerRow-=mode.drow
                    mode.playerCol-=mode.dcol
            for i in range(len(mode.boss)):
                if mode.playerRow==mode.boss[i].row and mode.playerCol==mode.boss[i].col:
                    mode.playerRow-=mode.drow
                    mode.playerCol-=mode.dcol
            for i in range(len(mode.treasure)):
                if mode.playerRow==mode.treasure[i].row and mode.playerCol==mode.treasure[i].col:
                    mode.playerRow-=mode.drow
                    mode.playerCol-=mode.dcol
        mode.drow=0
        mode.dcol=0
        if len(mode.boss)>0:
            GameMode.path=Demon.astar(GameMode.board, (mode.boss[0].row, mode.boss[0].col), (mode.playerRow, mode.playerCol))

    def drawEnemies(mode, canvas):
        canvas.create_image((mode.playerCol*mode.cellSize+(mode.margin))+mode.cellSize/2, (mode.playerRow*mode.cellSize+(mode.margin))+mode.cellSize/2, image=ImageTk.PhotoImage(mode.playerSprite[mode.spriteAction][mode.spriteCounter]))
        for slime in mode.slimes:
            canvas.create_image((slime.col*mode.cellSize+(mode.margin))+mode.cellSize/2, (slime.row*mode.cellSize+(mode.margin))+mode.cellSize/2, image=ImageTk.PhotoImage(mode.slimeSprite[mode.sSpriteCounter]))
            GameMode.board[slime.row][slime.col]=1
        for skel in mode.skels:
            canvas.create_image((skel.col*mode.cellSize+(mode.margin))+mode.cellSize/2, (skel.row*mode.cellSize+(mode.margin))+mode.cellSize/2, image=ImageTk.PhotoImage(mode.skelSprite[mode.skelCounter]))
            GameMode.board[skel.row][skel.col]=1
        for bos in mode.boss:
            if type(bos)==Demon:
                #Demon image from https://www.bobsprite.com/images/nerds/demon-pixelated-256x256.png
                canvas.create_image((bos.col*mode.cellSize+(mode.margin))+mode.cellSize/2, (bos.row*mode.cellSize+(mode.margin))+mode.cellSize/2, image=ImageTk.PhotoImage(file='Demon.png'))
            else:
                #Dragon from https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/95231b76-5fad-429a-a6d5-99f5f5e23f3b/da348q8-24b422d4-bbf0-46a8-8352-974f00c5f2d4.png?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwiaXNzIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsIm9iaiI6W1t7InBhdGgiOiJcL2ZcLzk1MjMxYjc2LTVmYWQtNDI5YS1hNmQ1LTk5ZjVmNWUyM2YzYlwvZGEzNDhxOC0yNGI0MjJkNC1iYmYwLTQ2YTgtODM1Mi05NzRmMDBjNWYyZDQucG5nIn1dXSwiYXVkIjpbInVybjpzZXJ2aWNlOmZpbGUuZG93bmxvYWQiXX0.VdNoNOcfzGxvZugqFcUQLWbeRFuFwaTFDwqIF7jNmWk
                canvas.create_image((bos.col*mode.cellSize+(mode.margin))+mode.cellSize/2, (bos.row*mode.cellSize+(mode.margin))+mode.cellSize/2, image=ImageTk.PhotoImage(file='Dragon.png'))
        
    def drawBlocks(mode, canvas):
        for i in range(len(GameMode.blocks)):
            for j in range(len(GameMode.blocks[i].block)):
                for c in range(len(GameMode.blocks[i].block[j])):
                    if GameMode.blocks[i].block[j][c]:
                        #Block from https://pngimage.net/wp-content/uploads/2018/05/dirt-block-png-5.png
                        url="block.png"
                        canvas.create_image(((GameMode.blocks[i].col+c+1)*mode.cellSize)+mode.cellSize/2, ((GameMode.blocks[i].row+j+1)*mode.cellSize)+mode.cellSize/2, image=ImageTk.PhotoImage(file=url))

    def drawTreasure(mode, canvas):
        for chest in mode.treasure:
            #Chest image from https://cdn.shopify.com/s/files/1/0822/1983/articles/treasure-chest-pixel-art-pixel-art-treasure-chest-pirate-8bit.png?v=1501253201
            canvas.create_image((chest.col*mode.cellSize+(mode.margin))+mode.cellSize/2, (chest.row*mode.cellSize+(mode.margin))+mode.cellSize/2, image=ImageTk.PhotoImage(file='Chest.png'))
            GameMode.board[chest.row][chest.col]=1
                

    def drawCell(mode, canvas, row, col, fillColor):
        initw=((col*mode.cellSize)+(mode.margin))
        inith=((row*mode.cellSize)+(mode.margin))
        canvas.create_rectangle(initw, inith, initw+mode.cellSize, inith+mode.cellSize, fill=fillColor)

    def timerFired(mode):
        mode.spriteCounter = (1 + mode.spriteCounter) % len(mode.playerSprite[0])
        mode.sSpriteCounter= (1 + mode.sSpriteCounter) % len(mode.slimeSprite)
        mode.skelCounter = (1 + mode.skelCounter) % len(mode.skelSprite)
        if mode.spriteCounter==mode.maxSpriteCount:
            mode.spriteAction=0
            mode.maxSpriteCount=13
            mode.spriteCounter=(1+mode.spriteCounter)%len(mode.playerSprite[0])
        for i in range(len(mode.slimes)):
            Slime.slimeMove(mode.slimes[i], mode.playerRow, mode.playerCol)
        for i in range(len(mode.skels)):
            Skeleton.skelMove(mode.skels[i], mode.playerRow, mode.playerCol)
        for i in range(len(mode.boss)):
            if type(mode.boss[i])==Demon:
                if mode.oldRow==mode.playerRow and mode.oldCol==mode.playerCol:
                    if GameMode.path != None:
                        mode.boss[i].row=GameMode.path[len(GameMode.path)-1][0]-1
                        mode.boss[i].col=GameMode.path[len(GameMode.path)-1][1]
                        if abs(mode.playerRow-mode.boss[i].row)<=1 and abs(mode.playerCol-mode.boss[i].col)<=1:
                            GameMode.health-=5
                            mode.boss[i].health+=2
                            if GameMode.health<0:
                                GameMode.health=0
                elif abs(GameMode.boss[i].row-mode.playerRow)!=1 or abs(GameMode.boss[i].col-mode.playerCol)!=1:
                    mode.path=Demon.astar(mode.board, (mode.boss[i].row, mode.boss[i].col), (mode.playerRow, mode.playerCol))
                    if GameMode.path!=None:
                        mode.boss[i].row=GameMode.path[1][0]
                        mode.boss[i].col=GameMode.path[1][1]
                        if abs(mode.playerRow-mode.boss[i].row)<=1 and abs(mode.playerCol-mode.boss[i].col)<=1:
                            GameMode.health-=5
                            mode.boss[i].health+=2
                            if GameMode.health<0:
                                GameMode.health=0
            elif type(mode.boss[i])==Dragon:
                Dragon.dragonMove(mode.boss[i], mode.playerRow, mode.playerCol)
        if mode.health==0:
            mode.app.setActiveMode(mode.app.gameOver)
        mode.oldRow=mode.playerRow
        mode.oldCol=mode.playerCol

    def redrawAll(mode, canvas):
        if mode.running:
            canvas.create_image(mode.width/2, mode.height/2, image=ImageTk.PhotoImage(mode.background))
            mode.drawEnemies(canvas)
            mode.drawTreasure(canvas)
            mode.drawBlocks(canvas)
            canvas.create_image((mode.playerCol*mode.cellSize+(mode.margin))+mode.cellSize/2, (mode.playerRow*mode.cellSize+(mode.margin))+mode.cellSize/2, image=ImageTk.PhotoImage(mode.playerSprite[mode.spriteAction][mode.spriteCounter]))
            canvas.create_text(80, 20, text=f"Score: {mode.score}", font='Times 40 bold', fill="black")
            canvas.create_text(mode.width-110, 20, text=f"Health: {mode.health}", font="Times 40 bold", fill="black")





class HelpScreen(Mode):
    def redrawAll(mode, canvas):
        canvas.create_rectangle(0, 0, mode.width, mode.height, fill="black")
        canvas.create_rectangle(100, 100, 300, 150, fill="gray")
        canvas.create_text(200, 125, text="Controls", font="Times 40 bold", fill="black")
        canvas.create_text(200, 200, text="Use the arrow keys to move!", font="Times 20 bold", fill="white")
        canvas.create_text(200, 225, text="And the space bar to attack!", font="Times 20 bold", fill="white")
        canvas.create_text(200, 250, text="Just cause it's simple doesn't mean it's easy...", font="Times 20 bold", fill="white")
        canvas.create_text(200, 275, text="Be careful young explorer!", font="Times 20 bold", fill="white")
        canvas.create_rectangle(mode.width-300, 100, mode.width-100, 150, fill="gray")
        canvas.create_text(mode.width-200, 125, text="Monsters", font="Times 40 bold", fill="black")
        canvas.create_text(mode.width-200, 175, text="Slime", font="Times 40 bold", fill="white")
        canvas.create_text(mode.width-200, 200, text="This beast isn't too harmful", font="Times 20 bold", fill="white")
        canvas.create_text(mode.width-200, 225, text="but don't underestimate it!", font="Times 20 bold", fill="white")
        canvas.create_text(mode.width-200, 250, text="each hit will do 5 damage", font="Times 20 bold", fill="white")
        canvas.create_text(mode.width-200, 300, text="Skeleton", font="Times 40 bold", fill="white")
        canvas.create_text(mode.width-200, 325, text="This beast hits harder than the slime", font="Times 20 bold", fill="white")
        canvas.create_text(mode.width-200, 350, text="It will do 10 damage per hit", font="Times 20 bold", fill="white")
        canvas.create_text(mode.width-200, 400, text="Dragon", font="Times 40 bold", fill="white")
        canvas.create_text(mode.width-200, 425, text="Fight this beast if you dare", font="Times 20 bold", fill="white")
        canvas.create_text(mode.width-200, 450, text="Beware its attack, for it does 20 damage", font="Times 20 bold", fill="white")
        canvas.create_text(mode.width-200, 500, text="Demon", font="Times 40 bold", fill="white")
        canvas.create_text(mode.width-200, 525, text="Don't underestimate this beast for its low", font="Times 20 bold", fill="white")
        canvas.create_text(mode.width-200, 550, text="damage because while it does 5 damage per", font="Times 20 bold", fill="white")
        canvas.create_text(mode.width-200, 575, text="hit it sucks your soul, healing itself", font="Times 20 bold", fill="white")
        canvas.create_text(mode.width/2, 20, text="Press any key to return to the game", font="Times 40 bold", fill="white")

    def keyPressed(mode, event):
        mode.app.setActiveMode(mode.app.gameMode)

class GameOverMode(Mode):
    def redrawAll(mode, canvas):
        canvas.create_rectangle(0, 0, mode.width, mode.height, fill="black")
        canvas.create_text(mode.width/2, mode.height/2-40, text="Game Over!", font="Times 40 bold", fill="white")
        canvas.create_text(mode.width/2, mode.height/2, text=f"Final Score: {GameMode.score}", font="Times 40 bold", fill="white")
        canvas.create_text(mode.width/2, mode.height/2+40, text="Press R to restart", font="Times 40 bold", fill="white")
    
    def keyPressed(mode, event):
        if event.key=="r":
            GameMode.health=100
            GameMode.score=0
            mode.app.setActiveMode(GameMode())

class MyModalApp(ModalApp):
    def appStarted(app):
        app.gameMode=GameMode()
        app.splashScreenMode=SplashScreenMode()
        app.transitionMode=TransitionMode()
        app.helpScreen=HelpScreen()
        app.gameOver=GameOverMode()
        app.setActiveMode(app.splashScreenMode)
        app.timerDelay=400

app=MyModalApp(width=800, height=600)