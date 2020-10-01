import game
import pygame, sys
from pygame.locals import *
from game import SlidingPuzzle, GameState, Runner
from bitmapfont import BitmapFont
from solver import AStar, manhattan

direction = [(1, 0), (-1, 0), (0, 1), (0, -1)]

class MainMenu(GameState):
    def __init__(self, runner, nextState):
        super().__init__(runner)
        self.nextState = nextState
        self.arr = ["START", "EXIT"]
        self.currentSelection = 0
        self.delayTime = 200

    def update(self, deltatime):
        keys = pygame.key.get_pressed()
        if self.delayTime > 0:
            self.delayTime -= deltatime
        else:
            if keys[K_UP]:
                self.currentSelection = 0
                self.delayTime = 200
            elif keys[K_DOWN]:
                self.currentSelection = 1
                self.delayTime = 200

            elif keys[K_SPACE]:
                if self.currentSelection == 0:
                    self.runner.change_state(self.nextState)
                    self.delayTime = 200

                else:
                    self.runner.change_state(None)
                    self.delayTime = 200

        if self.delayTime < 0:
            self.delayTime = 0

    def draw(self, surface):
        self.runner.font.centre(surface, "SlidingPuzzle", self.runner.width * 0.3)
        for i, j in enumerate(self.arr):
            if i == self.currentSelection:
                msg = ">" + j + "<"
            else:
                msg = j
            self.runner.font.centre(surface, msg, self.runner.width * 0.5 + 18 * i)

class OptionMenu(GameState):
    def __init__(self, runner, mainmenuState, InGameState):
        super().__init__(runner)
        self.mainmenuState = mainmenuState
        self.InGameState = InGameState
        self.size = 3
        self.useSolver = "No"
        self.arr = ["Size " + str(self.size), "Use Solver: " +  self.useSolver, "Start", "Return"]
        self.currentSelection = 0
        self.delayTime = 200

    def on_enter(self, mainmenuState):
        self.size = 3
        self.currentSelection = 0
        self.arr = ["Size " + str(self.size), "Use Solver: " +  self.useSolver, "Start", "Return"]

    def update(self, deltatime):
        keys = pygame.key.get_pressed()
        if self.delayTime > 0:
            self.delayTime -= deltatime

        else:

            if keys[K_UP] and self.currentSelection > 0:
                self.currentSelection -= 1
                self.delayTime = 200
            elif keys[K_DOWN] and self.currentSelection < 2:
                self.currentSelection += 1
                self.delayTime = 200
            elif keys[K_LEFT] and self.currentSelection == 0:
                self.size -= 1
                self.arr[0] = "Size " + str(self.size)
                self.delayTime = 200
            elif keys[K_RIGHT] and self.currentSelection == 0:
                self.size += 1
                self.arr[0] = "Size " + str(self.size)
                self.delayTime = 200
            elif keys[K_RIGHT] and self.currentSelection == 1:
                self.useSolver = "Yes"
                self.arr[1] = "Use Solver: " +  self.useSolver
                self.delayTime = 200
            elif keys[K_LEFT] and self.currentSelection == 1:
                self.useSolver = "No"
                self.arr[1] = "Use Solver: " +  self.useSolver
                self.delayTime = 200
            elif keys[K_SPACE]:
                if self.currentSelection == 2:
                    self.runner.change_state(self.InGameState)
                    self.delayTime = 200
                elif self.currentSelection == 3:
                    self.runner.change_state(self.mainmenuState)
                    self.delayTime = 200

        if self.delayTime < 0:
            self.delayTime = 0

    def draw(self, surface):
        self.runner.font.centre(surface, "Setup", self.runner.width * 0.3)
        for i, j in enumerate(self.arr):
            if i == self.currentSelection:
                msg = ">" + j + "<"
            else:
                msg = j
            self.runner.font.centre(surface, msg, self.runner.width * 0.5 + 18* i)


class InGame(GameState):
    def __init__(self, runner, mainmenuState):
        super().__init__(runner)
        self.mainmenuState = mainmenuState
        self.endFlag = False
        self.font = BitmapFont("fasttracker2-style_12x12.png", 12, 12)
        self.delayTime = 200
        


    def on_enter(self, OptionMenuState):
        self.size = optionmenu.size
        self.useSolver = optionmenu.useSolver
        self.slidingPuzzle = SlidingPuzzle(self.size)
        self.endFlag = False
        self.slidingPuzzle.shuffle()
        self.slidingPuzzle.canbeSolved()
        if self.useSolver == "Yes":
            self.astar = AStar(self.slidingPuzzle)
            self.answer = self.astar.solved()
            self.i = 1

    def draw(self, surface):
        self.width = 600/self.size
        for i in range(self.size):
            for j in range(self.size):
                x, y = j* self.width, i * self.width
                rect = Rect(x, y, self.width, self.width)
                pygame.draw.rect(surface, (100, 100, 100), rect, 3)
                currentCell = self.slidingPuzzle.arr[i][j]
                fontWidth = 12 * len(str(currentCell))
                self.font.draw(surface, str(currentCell), x+((self.width-fontWidth)/2), y+((self.width-12)/2))


    def update(self, deltatime):
        keys = pygame.key.get_pressed()
        self.endFlag = self.slidingPuzzle.isSolved()
        if self.delayTime > 0:
            self.delayTime -= deltatime
        else:
            if keys[K_ESCAPE]:
                self.runner.change_state(self.mainmenuState)
                self.delayTime = 200
            if not self.endFlag:
                if self.useSolver == "No":
                    if keys[K_UP]:
                        self.slidingPuzzle.moves((0,-1))
                        self.delayTime = 200
                    if keys[K_LEFT]:
                        self.slidingPuzzle.moves((-1,0))
                        self.delayTime = 200
                    if keys[K_DOWN]:
                        self.slidingPuzzle.moves((0,1))
                        self.delayTime = 200
                    if keys[K_RIGHT]:
                        self.slidingPuzzle.moves((1,0))
                        self.delayTime = 200
                else:
                    #print(self.answer)
                    if keys[K_n]:
                        if self.answer[self.i] is not None:
                            self.slidingPuzzle.moves(self.answer[self.i])
                        self.delayTime = 200
                        if self.i < len(self.answer) - 1:
                            self.i += 1
                    if keys[K_p]:
                        directionA = self.answer[self.i-1]
                        if directionA is not None:
                            if directionA == (1, 0):
                                directionA = (-1, 0)
                            elif directionA == (-1, 0):
                                directionA = (1, 0)
                            elif directionA == (0, 1):
                                directionA = (0, -1)
                            elif directionA == (0, -1):
                                directionA = (0, 1)
                            self.slidingPuzzle.moves(directionA)
                        self.delayTime = 200
                        if self.i > 1:
                            self.i -= 1
     



                
                            
                        


        if self.runner.mouseClick is not None:       
            mouseX, mouseY = self.runner.mouseClick

            if self.useSolver == "No":  
                #distance from mousepress position to space position
                x = int(mouseX/self.width)
                y = int(mouseY/self.width)
                directionX = x - self.slidingPuzzle.space[0]
                directionY = y - self.slidingPuzzle.space[1]

                #make directionX into 1 or -1 and no diagonal
                if directionX > 0:
                    directionX = 1
                if directionX < 0:
                    directionX = -1
                if directionY > 0:
                    directionY = 1
                if directionY < 0:
                    directionY = -1
                for i in direction:
                    if (directionX, directionY) == i:
                        self.slidingPuzzle.moves((directionX, directionY))
                        break

if __name__ == '__main__':
    runner = Runner('SlidingPuzzle', 200*3)
    mainmenu = MainMenu(runner, None)
    optionmenu = OptionMenu(runner, mainmenu, None)
    ingamemenu = InGame(runner, mainmenu)
    mainmenu.nextState = optionmenu
    optionmenu.InGameState = ingamemenu
    runner.run(mainmenu)