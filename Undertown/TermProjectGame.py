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

class Chest(object):
    def __init__(self, row, col):
        self.row=row
        self.col=col
        self.gold=random.randrange(11)

class Enemy(object):
    def __init__(self, row, col):
        self.row=row
        self.col=col

class Slime(Enemy):
    def __init__(self, row, col):
        super().__init__(row, col)
        self.color="green"
        self.timerDelay=10000
        self.health=2
    
    def slimeMove(self, playerRow, playerCol):
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


    

class Skeleton(Enemy):
    def __init__(self, row, col):
        super().__init__(row, col)
        self.color="white"
        self.health=6
    
    def skelMove(self, playerRow, playerCol):
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
            self.row-=drow
            self.col-=dcol

class Demon(Enemy):
    def __init__(self, row, col):
        super().__init__(row, col)
        self.color="brown"

class Dragon(Enemy):
    def __init__(self, row, col):
        super().__init__(row, col)
        self.color="yellow"

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
        canvas.create_text(mode.width/2, mode.height/2, text="UNDERTOWN", font='Times 60 bold', fill="white")
        canvas.create_text(mode.width/2, mode.height/2+60, text="Press any key to continue", font='Times 40 bold', fill="white")

    def keyPressed(mode, event):
        mode.app.setActiveMode(mode.app.gameMode)

class TransitionMode(Mode):
    def redrawAll(mode, canvas):
        canvas.create_rectangle(0, 0, mode.width, mode.height, fill="black")
    def timerFired(mode):
        GameMode.blocks=[]
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

        elif roomType==3:
            bossType=random.randrange(1, 3)
            GameMode.slimes.append(Slime(random.randrange(1, 12), random.randrange(1, 17)))
            GameMode.slimes.append(Slime(random.randrange(1, 12), random.randrange(1, 17)))
            GameMode.skels.append(Skeleton(random.randrange(1, 12), random.randrange(1, 17)))
            GameMode.skels.append(Skeleton(random.randrange(1, 12), random.randrange(1, 17)))
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
            if bossType==1:
                GameMode.boss.append(Demon(6, 9))
            else:
                GameMode.boss.append(Dragon(6, 9))
        mode.app.setActiveMode(mode.app.gameMode)
        

class GameMode(Mode):
    blocks=[]
    slimes=[]
    skels=[]
    boss=[]
    treasure=[]
    lastDirection=""
    playerRow=0
    playerCol=0
    def appStarted(mode):
        mode.background=mode.loadImage('dungeonBackground.png')
        mode.playerRow = 10
        mode.playerCol= 8
        mode.running=True
        mode.rows, mode.cols, mode.cellSize, mode.margin=gameDimensions()
        mode.board=[]
        for row in range(mode.rows):
            mode.board+=[[None] * mode.cols]
        mode.health=100
        mode.score=0
    
    blockNums=[random.randrange(6) for i in range(10)]
    for i in range(10):
        blocks.append(Block(random.randrange(1, 12), random.randrange(1, 17), blockNums[i]))


    def keyPressed(mode, event):
        if event.key=="Right":
            mode.drow=0
            mode.dcol=1
            lastDirection="Right"
            mode.movePlayer()
        elif event.key=="Left":
            mode.drow=0
            mode.dcol=-1
            lastDirection="Left"
            mode.movePlayer()
        elif event.key=="Down":
            mode.drow=1
            mode.dcol=0
            lastDirection="Down"
            mode.movePlayer()
        elif event.key=="Up":
            mode.drow=-1
            mode.dcol=0
            lastDirection="Up"
            mode.movePlayer()

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
            
            for i in range(len(mode.blocks)):
                for j in range(len(mode.blocks[i].block)):
                    for c in range(len(mode.blocks[i].block[j])):
                        if mode.blocks[i].block[j][c]:
                            if mode.playerRow==mode.blocks[i].row+j and mode.playerCol==mode.blocks[i].col+c:
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
        mode.drow=0
        mode.dcol=0

    def drawEnemies(mode, canvas):
        for slime in mode.slimes:
            mode.drawCell(canvas, slime.row, slime.col, slime.color)
        for skel in mode.skels:
            mode.drawCell(canvas, skel.row, skel.col, skel.color)
        for bos in mode.boss:
            mode.drawCell(canvas, bos.row, bos.col, bos.color)
        
    def drawBlocks(mode, canvas):
        for i in range(len(mode.blocks)):
            for j in range(len(mode.blocks[i].block)):
                for c in range(len(mode.blocks[i].block[j])):
                    if mode.blocks[i].block[j][c]:
                        mode.drawCell(canvas, mode.blocks[i].row+j, mode.blocks[i].col+c, "red")
    
    def drawTreasure(mode, canvas):
        for chest in mode.treasure:
            mode.drawCell(canvas, chest.row, chest.col, "yellow")
                

    def drawCell(mode, canvas, row, col, fillColor):
        initw=((col*mode.cellSize)+(mode.margin))
        inith=((row*mode.cellSize)+(mode.margin))
        canvas.create_rectangle(initw, inith, initw+mode.cellSize, inith+mode.cellSize, fill=fillColor)

    def timerFired(mode):
        for i in range(len(mode.slimes)):
            Slime.slimeMove(mode.slimes[i], mode.playerRow, mode.playerCol)
        for i in range(len(mode.skels)):
            Skeleton.skelMove(mode.skels[i], mode.playerRow, mode.playerCol)

    def redrawAll(mode, canvas):
        if mode.running:
            canvas.create_image(mode.width/2, mode.height/2, image=ImageTk.PhotoImage(mode.background))
            mode.drawBlocks(canvas)
            mode.drawEnemies(canvas)
            mode.drawTreasure(canvas)
            mode.drawCell(canvas, mode.playerRow, mode.playerCol, "black")

class MyModalApp(ModalApp):
    def appStarted(app):
        app.gameMode=GameMode()
        app.splashScreenMode=SplashScreenMode()
        app.transitionMode=TransitionMode()
        app.setActiveMode(app.splashScreenMode)
        app.timerDelay=500

app=MyModalApp(width=800, height=600)
"""pygame.init()


class GameMode(Mode):
    def appStarted(mode):
        screen=pygame.display.set_mode((800, 600))
        #background image: https://wallpapersafari.com/w/KOoJ2e
        background=pygame.image.load('dungeonBackground.png')
        mode.playerX = 400-40
        mode.playerY=300-80
        mode.playerX_change=0
        mode.playerY_change=0
        mode.running=True

    def keyPressed(mode, event):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                mode.running = False

        if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    modeplayerX_change = -5
                if event.key == pygame.K_RIGHT:
                    mode.playerX_change = 5
                if event.key == pygame.K_UP:
                    mode.playerY_change = -5
                if event.key == pygame.K_DOWN:
                    mode.playerY_change = 5

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_DOWN or event.key == pygame.K_UP:
                mode.playerX_change = 0
                mode.playerY_change=0
        
        mode.playerX += mode.playerX_change
        if mode.playerX <= 40:
            mode.playerX = 40
        elif mode.playerX >= 720:
            mode.playerX = 720

        mode.playerY += mode.playerY_change
        if mode.playerY <= 40:
            mode.playerY = 40
        elif mode.playerY >= 480:
            mode.playerY = 480
        
    def redrawAll(mode):
        while running:
            screen.fill((0, 0, 0))
            screen.blit(background, (0, 0))
            pygame.draw.rect(screen, [255, 0, 0], [mode.playerX, mode.playerY, 40, 80], 0)
            pygame.display.update()

class MyModalApp(ModalApp):
    def appStarted(app):
        app.gameMode=GameMode()
        app.setActiveMode(app.gameMode)
        app.timerDelay=50

app=MyModalApp(width=800, height=600)"""