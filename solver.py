from game import SlidingPuzzle
from copy import deepcopy
from game import UP, DOWN, RIGHT, LEFT
import heapq

direction = [UP, DOWN, RIGHT, LEFT]


def manhattan(arr):
    correctarr = {}
    width = len(arr)
    for i in range(width):
        for j in range(width):
            key = (j+1) +width*(i)
            correctarr[key] = (j, i)
    totaldistance = 0
    for i in range(width):
        for j in range(width):
            if arr[i][j] == " ":
                continue
            x, y = correctarr[arr[i][j]]
            totaldistance += abs((j-x)) + abs((y-i))
    return totaldistance

class SearchNode:
    def __init__(self, arr, parent= None, action= None, g = 0, h= 0):
        self.state = SlidingPuzzle(len(arr), state=deepcopy(arr))
        self.parent = parent
        self.action = action
        self.g = g
        self.h = h
        self.f = self.g + self.h
        self.nodeState = None

    def expand(self):
        result = []
        for i in direction:
            if self.state.isValidMoves(i):
                node = SearchNode(self.state.arr, self, i)
                node.state.moves(i)
                node.g = self.g + 1
                node.h = manhattan(node.state.arr) 
                node.f = node.g + node.h
                result.append(node)
        return result

    def __lt__(self, node):
        if self.f == node.f:
            return self.h < node.h
        else:
            return self.f < node.f

    def __eq__(self, node):
        return self.state.arr == node.state.arr

class AStar:
    def __init__(self, board):
        self.board = board


    def solved(self):
        frontier = [] #open_list
        explored = [] #closed_list
        startNode = SearchNode(self.board.arr, h=manhattan(self.board.arr))
        print(manhattan(self.board.arr))
        heapq.heappush(frontier, startNode)
        success = False
        while frontier:
            node = heapq.heappop(frontier)
            explored.append(node)
            if node.state.isSolved():
                success = True
                break
            for i in node.expand():
                if i not in frontier and i not in explored:
                    heapq.heappush(frontier, i)
                elif i in frontier:
                    j = frontier.index(i)
                    if i < frontier[j]:
                        frontier[j] = i
                        heapq.heapify(frontier)
            
        if not success:
            return False
        solvedArr = []
        current = explored[-1]   
        while current is not None:
            solvedArr.append(current.action) 
            current = current.parent
        return solvedArr[::-1]


if __name__ == '__main__':
    slidingpuzzle = SlidingPuzzle(3)
    slidingpuzzle.shuffle()
    slidingpuzzle.canbeSolved()
    print(slidingpuzzle)
    astar = AStar(slidingpuzzle)
    answer = astar.solved()
    for i in answer:
        if i is not None:
            print(i)
            #n = input()
            #slidingpuzzle.moves(i)
            #print(slidingpuzzle)






    




