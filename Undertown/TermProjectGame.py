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
        mode.app.setActiveMode(GameMode())

class TransitionMode(Mode):
    def appStarted(mode):
        mode.timerDelay=5000
    def redrawAll(mode, canvas):
        canvas.create_rectangle(0, 0, mode.width, mode.height, fill="black")
    def timerFired(mode):
        blockNums=[random.randrange(6) for i in range(10)]
        for i in range(len(blockNums)):
            GameMode.blocks.pop(i)
            GameMode.blocks.append(Block(random.randrange(1, 12), random.randrange(1, 17), blockNums[i]))
            """for j in GameMode.blocks[i].block:
                isLegal=False
                while not isLegal:
                    isLegal=True
                    for l in range(len(j)):
                        for cell in range(len(l)):
                            if cell:"""

        mode.app.setActiveMode(GameMode())
        

class GameMode(Mode):
    blocks=[]
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
            mode.movePlayer()
        elif event.key=="Left":
            mode.drow=0
            mode.dcol=-1
            mode.movePlayer()
        elif event.key=="Down":
            mode.drow=1
            mode.dcol=0
            mode.movePlayer()
        elif event.key=="Up":
            mode.drow=-1
            mode.dcol=0
            mode.movePlayer()

    def movePlayer(mode):
        mode.playerRow+=mode.drow
        mode.playerCol+=mode.dcol
        if (mode.playerCol>=7 and mode.playerCol<=10) and (mode.playerRow<0 or mode.playerRow>12):
            mode.app.setActiveMode(TransitionMode())
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
        mode.drow=0
        mode.dcol=0

    def drawBlocks(mode, canvas):
        for i in range(len(mode.blocks)):
            for j in range(len(mode.blocks[i].block)):
                for c in range(len(mode.blocks[i].block[j])):
                    if mode.blocks[i].block[j][c]:
                        mode.drawCell(canvas, mode.blocks[i].row+j, mode.blocks[i].col+c, "red")
                

    def drawCell(mode, canvas, row, col, fillColor):
        initw=((col*mode.cellSize)+(mode.margin))
        inith=((row*mode.cellSize)+(mode.margin))
        canvas.create_rectangle(initw, inith, initw+mode.cellSize, inith+mode.cellSize, fill=fillColor)

    def redrawAll(mode, canvas):
        if mode.running:
            canvas.create_image(mode.width/2, mode.height/2, image=ImageTk.PhotoImage(mode.background))
            mode.drawBlocks(canvas)
            mode.drawCell(canvas, mode.playerRow, mode.playerCol, "black")

class MyModalApp(ModalApp):
    def appStarted(app):
        app.gameMode=GameMode()
        app.splashScreenMode=SplashScreenMode()
        app.setActiveMode(SplashScreenMode())
        app.timerDelay=50

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