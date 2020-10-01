import terminaltables
import itertools
import random
import pygame, sys
from pygame.locals import *
from bitmapfont import BitmapFont

UP = (0, -1)
DOWN = (0, 1)
RIGHT = (1, 0)
LEFT = (-1, 0)

class SlidingPuzzle():
    def __init__(self, n, state=None):
        self.width = n
        if state is None:  
            self.arr = []
            for i in range(1, self.width+1):
                arr = []
                for j in range(1, self.width+1):
                    arr.append(j+ n*(i-1))
                self.arr.append(arr)
            self.arr[-1][-1] = " "
            self.space = 3, 3
        else:
            self.arr = state
            for i in range(self.width):
                for j in range(self.width):
                    if self.arr[i][j] == " ":
                        self.space = j, i
                        break
                else:
                    continue
                break
        




    def __str__(self):
        table = terminaltables.SingleTable(self.arr)
        table.inner_row_border = True
        table.inner_column_border = True
        for i in range(self.width):
            table.justify_columns[i] = 'center'
        return table.table

    def shuffle(self):
        cells = list(itertools.chain.from_iterable(self.arr))
        for i in range(self.width*self.width-1, 0, -1):
            j = random.randint(0, i)
            cells[j], cells[i] = cells[i], cells[j]
        for i in range(self.width):
            for j in range(self.width):
                self.arr[i][j] = cells[i*self.width +j]
                if self.arr[i][j] == " ":
                    self.space = j, i

    def canbeSolved(self):
        cells = list(itertools.chain.from_iterable(self.arr))
        result = False
        totalinversion = 0
        for index, i in enumerate(cells):
            if i == " ":
                continue
            for j in range(index+1, len(cells)):
                if cells[j] == " ":
                    continue
                if i > cells[j]:
                    totalinversion += 1
            
        


        if self.width % 2 != 0 and totalinversion % 2 == 0:
            result = True      
        elif self.width % 2 == 0 and (self.width - self.space[1]) % 2  == 0 and totalinversion % 2 != 0:
            result = True
        elif self.width % 2 == 0 and (self.width - self.space[1]) % 2 !=  0 and totalinversion % 2 == 0:
            result = True

        if not result:
            for i in range(self.width):
                for j in range(self.width):
                    if self.arr[i][j] == 1:
                        pos1 = i, j
                    if self.arr[i][j] == 2:
                        pos2 = i, j
            self.arr[pos1[0]][pos1[1]], self.arr[pos2[0]][pos2[1]] = self.arr[pos2[0]][pos2[1]], self.arr[pos1[0]][pos1[1]]

    def isValidMoves(self, direction):
        targetX = self.space[0] + direction[0]
        targetY = self.space[1] + direction[1]
        return targetX < self.width and targetX >= 0 and targetY < self.width and targetY >= 0

    
    def moves(self, direction):
        if self.isValidMoves(direction):
            targetX = self.space[0] + direction[0]
            targetY = self.space[1] + direction[1]
            self.arr[self.space[1]][self.space[0]], self.arr[targetY][targetX] = self.arr[targetY][targetX], self.arr[self.space[1]][self.space[0]]
            self.space = targetX, targetY
    
    def isSolved(self):
        solved = True
        cells = list(itertools.chain.from_iterable(self.arr))
        for i in range(len(cells)-1):
            if cells[i] != i+1:
                solved = False
                break
        return solved
        

def startGame():
    n = int(input("size: "))
    slidingpuzzle = SlidingPuzzle(n)
    slidingpuzzle.shuffle()
    slidingpuzzle.canbeSolved()
    dic = {"w": UP, "a": LEFT, "d": RIGHT, "s": DOWN}
    while not slidingpuzzle.isSolved():
        print(slidingpuzzle)
        direction = input("direction: ").lower()
        direction = dic.get(direction, None)
        if direction is not None:
            slidingpuzzle.moves(direction)
    

    
class GameState: 
    def __init__(self, runner):
        self.runner = runner
    
    def on_enter(self, prev_state):
        pass

    def on_exit(self):
        pass

    def update(self, deltatime):
        pass

    def draw(self, surface):
        pass


    
class Runner:
    def __init__(self, name, width):
        self.name = name
        self.width = width
        pygame.init()
        pygame.display.set_caption(self.name)
        self.WINDOWS = pygame.display.set_mode((self.width, self.width))
        self.fpsClock = pygame.time.Clock()
        self.font = BitmapFont("fasttracker2-style_12x12.png", 12, 12)
        self.BLACK = pygame.Color(0,0,0)
        self.state = None
        self.mouseClick = None
    
    def change_state(self, newState):
        if self.state is not None:
            self.state.on_exit()

        if newState is None:
            pygame.quit()
            sys.exit()
        else:
            newState.on_enter(self.state)
            self.state = newState
    
    def run(self, initialState):
        self.change_state(initialState)

        while True:
            self.mouseClick = None
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                
                elif event.type == MOUSEBUTTONUP:
                    self.mouseClick = event.pos

            self.state.update(self.fpsClock.get_time())
            self.WINDOWS.fill(self.BLACK)
            self.state.draw(self.WINDOWS)
        
            pygame.display.update()
            self.fpsClock.tick(30)

    
if __name__ == "__main__":
    slidingpuzzle = SlidingPuzzle(3)
    startGame()
