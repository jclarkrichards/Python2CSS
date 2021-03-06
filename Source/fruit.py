class Node(object):
    def __init__(self, row, column):
        self.row, self.column = row, column
        self.position = Vector2(column*TILEWIDTH, row*TILEHEIGHT)
        self.neighbors = {UP:None, DOWN:None, LEFT:None, RIGHT:None}
        self.portalNode = None
        self.portalVal = 0
        self.homeGuide = False
        self.homeEntrance = False
        self.spawnNode = False
        self.pacmanStart = False
        #newtext::self.fruitStart = False


class NodeGroup(object):
    def __init__(self, level):
        self.nodeList = []
        self.homeList = []
        self.level = level
        self.grid = None
        self.nodeStack = Stack()
        self.pathSymbols = ["p", "P"]
        self.portalSymbols = ["1"]
        self.nodeSymbols = ["+", "n", "N", "H", "S", "Y", "F"] + self.portalSymbols
        self.grid = self.readMazeFile(level)
        self.homegrid = self.getHomeArray()
        self.createNodeList(self.grid, self.nodeList)
        self.createNodeList(self.homegrid, self.homeList)
        self.setupPortalNodes()
        self.moveHomeNodes()
        self.homeList[0].homeEntrance = True

    def pathToFollow(self, direction, row, col, path, grid):
        tempSymbols = [path]+self.nodeSymbols + self.pathSymbols
        if grid[row][col] in tempSymbols:
            while grid[row][col] not in self.nodeSymbols:
                if direction is LEFT: col -= 1
                elif direction is RIGHT: col += 1
                elif direction is UP: row -= 1
                elif direction is DOWN: row += 1
            node = Node(row, col)
            if grid[row][col] == "H":
                node.homeGuide = True
            if grid[row][col] == "S":
                node.spawnNode = True
            if grid[row][col] == "Y":
                node.pacmanStart = True
            #newtext::if grid[row][col] == "F":
                #newtext::node.fruitStart = True
            if grid[row][col] in self.portalSymbols:
                node.portalVal = grid[row][col]
            return node
        else:
            return None

        
#fruit.py
import pygame
from entity import MazeRunner
from constants import *

class Fruit(MazeRunner):
    def __init__(self, nodes):
        MazeRunner.__init__(self, nodes)
        self.name = "fruit"
        self.color = (0,200,0)
        self.setStartPosition()
        self.lifespan = 5
        self.timer = 0
        self.destroy = False

    def update(self, dt):
        self.timer += dt
        if self.timer >= self.lifespan:
            self.destroy = True
            
    def setStartPosition(self):
        self.node = self.findStartNode()
        self.target = self.node.neighbors[LEFT]
        self.setPosition()
        self.position.x -= (self.node.position.x - self.target.position.x) / 2

    def findStartNode(self):
        for node in self.nodes.nodeList:
            if node.fruitStart:
                return node
        return None


#run.py
import pygame
from pygame.locals import *
from constants import *
from pacman import Pacman
from nodes import NodeGroup
from pellets import PelletGroup
from ghosts import GhostGroup
#newtext::from fruit import Fruit

class GameController(object):
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SCREENSIZE, 0, 32)
        self.background = None
        self.setBackground()
        self.clock = pygame.time.Clock()
        self.pelletsEaten = 0
        #newtext::self.fruit = None
        

    def update(self):
        dt = self.clock.tick(30) / 1000.0
        self.pacman.update(dt)
        self.ghosts.update(dt, self.pacman)
        #newtext::if self.fruit is not None:
            #newtext::self.fruit.update(dt)
        self.checkEvents()
        self.render()

    def checkEvents(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
        self.checkPelletEvents()
        self.checkGhostEvents()
        #newtext::self.checkFruitEvents()

    def checkPelletEvents(self):
        pellet = self.pacman.eatPellets(self.pellets.pelletList)
        if pellet:
            self.pelletsEaten += 1
            #newtext::if (self.pelletsEaten == 70 or self.pelletsEaten == 140):
                #newtext::if self.fruit is None:
                    #newtext::self.fruit = Fruit(self.nodes)
            self.pellets.pelletList.remove(pellet)
            if pellet.name == "powerpellet":
                self.ghosts.freightMode()

            
    #newtext::def checkFruitEvents(self):
        #newtext::if self.fruit is not None:
            #newtext::if self.pacman.eatFruit(self.fruit) or self.fruit.destroy:
                #newtext::self.fruit = None

            
    def render(self):
        self.screen.blit(self.background, (0,0))
        self.nodes.render(self.screen)
        self.pellets.render(self.screen)
        #newtext::if self.fruit is not None:
            #newtext::self.fruit.render(self.screen)
        self.pacman.render(self.screen)
        self.ghosts.render(self.screen)
        pygame.display.update()

        
#pacman.py
def eatFruit(self, fruit):
    d = self.position - fruit.position
    dSquared = d.magnitudeSquared()
    rSquared = (self.collideRadius+fruit.collideRadius)**2
    if dSquared <= rSquared:
        return True
    return False
