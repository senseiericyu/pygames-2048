import pygame
import random
import numpy as np

BG_COLORS = {
    0: (204,196,180),
    2: (240,228,220),
    4: (244,227,204),
    8: (248,180,124),
    16: (248,148,100),
    32: (248,124,92),
    64: (248,92,60),
    128: (236,212,116),
    256: (240,204,100),
    512: (240,204,84),
    1024: (237, 197, 63),
    2048: (237, 194, 46)
}

class Game2048:
    def __init__(self) -> None:
        self.dimension = 4
        self.cellSize = 100
        self.gap = 5
        self.windowBgColor = (188,172,156)
        self.blockSize = self.cellSize + self.gap * 2

        self.score = 0
        self.numFours = 0

        self.windowWidth = self.blockSize * 4
        self.windowHeight = self.windowWidth

        pygame.init()

        # create window
        self.window = pygame.display.set_mode((self.windowWidth + 50,self.windowHeight + 100))
        self.myFont = pygame.font.SysFont("Clear Sans", 77)
        self.bigFont = pygame.font.SysFont("Clear Sans", 100)
        self.scoreFont = pygame.font.SysFont("Clear Sans", 23)
        self.scoreNumFont = pygame.font.SysFont("Clear Sans", 50)
        pygame.display.set_caption("2048")

        # initiate board status
        self.boardStatus = np.zeros((self.dimension, self.dimension))
        self.addNewNumber() # add new number to board

    
    def addNewNumber(self):
        #creates list of all free positions
        freePos = zip(*np.where(self.boardStatus == 0))
        freePos = list(freePos)

        #goes through list of all free positions and chooses 1 at random
        for pos in random.sample(freePos, k=1):
            #make sure first value is always 2
            if len(freePos) == 16:
                self.boardStatus[pos] = 2
            else:     
                newNum = random.choice([2, 2, 2, 2, 2, 2, 2, 2, 2, 4]) 
                self.boardStatus[pos] = newNum
                if newNum == 4:
                    self.numFours += 1


    def drawBoard(self):
        self.window.fill(self.windowBgColor)

        #creating borders
        pygame.draw.rect(self.window,(252,252,236), pygame.Rect(0, 0, self.windowWidth+50, 86))
        pygame.draw.rect(self.window,(252,252,236), pygame.Rect(0, self.windowHeight + 96, self.windowWidth+50, 4))
        pygame.draw.rect(self.window,(252,252,236), pygame.Rect(0, 0, 22, self.windowHeight + 100))
        pygame.draw.rect(self.window,(252,252,236), pygame.Rect(self.windowWidth + 28, 0, 22, self.windowHeight + 100))

        #creating 2048 title
        big2048 = self.bigFont.render(f'2048', True, (119,110,101))
        self.window.blit(big2048, (25, 10))

        #creating score
        pygame.draw.rect(self.window,(188,172,156), pygame.Rect(self.windowWidth - 213, 10, 200, 50))
        
        score_text = self.scoreFont.render(f'SCORE:', True, (240,228,220))
        score_number = self.scoreNumFont.render(f'{int(self.score)}', True, (255,255,255))
        self.window.blit(score_text, (self.windowWidth - 200, 28))
        self.window.blit(score_number, (self.windowWidth - 130, 20)) #make this work better with centering



        for r in range(self.dimension):
            #draws vertical component of 4x4 board
            rectY = self.blockSize * r + self.gap + 90
            for c in range(self.dimension):
                #horizontal
                rectX = self.blockSize * c + self.gap + 25
                cellValue = int(self.boardStatus[r][c])

                pygame.draw.rect(
                    self.window,
                    BG_COLORS[cellValue],
                    pygame.Rect(rectX, rectY, self.cellSize, self.cellSize)
                )
                #numbers on tiles
                if cellValue != 0 and cellValue < 8:
                    textSurface = self.myFont.render(f"{cellValue}", True, (119,110,101))
                    textRect = textSurface.get_rect(center=(rectX + self.blockSize/2 - 5, rectY + self.blockSize/2 - 3))
                    self.window.blit(textSurface, textRect)
                elif cellValue != 0:    
                    textSurface = self.myFont.render(f"{cellValue}", True, (255,255,255))
                    textRect = textSurface.get_rect(center=(rectX + self.blockSize/2 - 5, rectY + self.blockSize/2 - 3))
                    self.window.blit(textSurface, textRect)

    def findScore(self, number):
        if number == 0 or number == 2:
            return 0
        return 2*self.findScore(number/2) + number


    def totalScore(self):
        self.score = 0
        for i in range(self.dimension):
            for j in range(self.dimension):
                self.score += self.findScore(self.boardStatus[i][j])
        self.score -= self.numFours * 4                   

    def compressNumber(self, data):
        result = [0]
        data = [x for x in data if x != 0]
        for element in data:
            if element == result[-1]:
                result[-1] *= 2
                result.append(0)
            else:
                result.append(element)
        
        result = [x for x in result if x != 0]
        return result  
    

    def move(self, dir):
        for index in range(self.dimension):
            #if the direction we move is up or down, set data to a list of the values in the index'th column
            if dir in "UD":
                data = self.boardStatus[:, index]
            #else the direction is in right or left, so set data to a list of the values in the index'th row
            else:
                data = self.boardStatus[index, :]

            #need to flip to get the correct orientation to perform the compress, in the case that the move is not left or up
            flip = False
            if dir in "RD":
                flip = True
                data = data[::-1]

            data = self.compressNumber(data)
            data = data + (self.dimension - len(data)) * [0]

            if flip:
                data = data[::-1]

            if dir in "UD":
                self.boardStatus[:, index] = data
            else:
                self.boardStatus[index, :] = data


    def isGameOver(self):
        boardStatusBackup = self.boardStatus.copy()
        for dir in "UDLR":
            self.move(dir)

            if (self.boardStatus == boardStatusBackup).all() == False:
                self.boardStatus = boardStatusBackup
                return False
        return True

    def isSameBoard(self):
        boardStatusBackup = self.boardStatus.copy()
        for dir in "RD":
            self.move(dir)

            if (self.boardStatus == boardStatusBackup).all() == False:
                self.boardStatus = boardStatusBackup
                return False
        return True
    

    def play(self):
        running = True
        while running:
            self.drawBoard()
            pygame.display.update()

            for event in pygame.event.get():
                oldBoardStatus = self.boardStatus.copy()

                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.move("U")
                    elif event.key == pygame.K_DOWN:
                        if not self.isSameBoard():
                            self.move("D")
                    elif event.key == pygame.K_LEFT:
                        self.move("L")
                    elif event.key == pygame.K_RIGHT:
                        if not self.isSameBoard():
                            self.move("R")
                    elif event.key == pygame.K_ESCAPE:
                        running = False

                    self.totalScore()

                    if self.isGameOver():
                        return

                    if (self.boardStatus == oldBoardStatus).all() == False:
                        self.addNewNumber()

if __name__ == "__main__":
    game = Game2048()
    game.play()