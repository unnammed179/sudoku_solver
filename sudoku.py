import pygame, sys
from pygame.locals import *

WIDTH = 630
CELL = WIDTH // 9
HEIGHT = WIDTH + CELL

RED = (255, 0, 0)
BLACK = (0,  0,  0)
WHITE = (255, 255, 255)
LIGHTGRAY = (200, 200, 200)
BLUE = (0, 0, 255)


class Button:
    def __init__(self, x, val):
        self.value = val
        self.x = x
        self.y = 630
        self.selected = False
        self.color = BLUE

    def draw(self, win):
        fnt = pygame.font.SysFont("comicsans", 40)
        text = fnt.render(self.value, 1, self.color)
        win.blit(text, ((self.x + CELL, self.y + (CELL - text.get_height()) / 2)))
        if self.selected:
            pygame.draw.rect(win, self.color, (self.x, self.y, CELL, CELL), 3)

    def setColor(self, val):
        self.color = val


class Box:
    def __init__(self, row, col, value=0):
        self.row = row
        self.col = col
        self.width = WIDTH / 10
        self.height = HEIGHT / 10
        self.value = value
        self.selected = False
        self.color = BLACK

    def draw(self, win):
        x = self.row * CELL
        y = self.col * CELL
        fnt = pygame.font.SysFont("comicsans", 40)
        text = fnt.render(str(self.value), 1, self.color)
        if self.value != 0:
            win.blit(text, (x + (CELL - text.get_width()) / 2, y + (CELL - text.get_height()) / 2))
        if self.selected:
            pygame.draw.rect(win, (255, 0, 0), (x, y, CELL, CELL), 3)
            # text1 = fnt.render(str(self.row)+str(self.col),1,BLUE)
            # win.blit(text1, (0,0))

    def setVal(self, val):
        self.value = val

    def select(self, val):
        self.selected = val

    def setColor(self, val):
        self.color = val


class Board:
    def __init__(self):
        self.bo = []
        self.boxes = []
        for i in range(0, 9):
            self.boxes.append([Box(i, j) for j in range(0, 9)])

    def draw(self, win, delay=False):
        for i in range(0, 9):
            for j in range(0, 9):
                self.boxes[j][i].draw(win)

        if not self.validInput():
            fnt = pygame.font.SysFont("comicsans", 40)
            text = fnt.render('Invalid Input', 1, RED)
            win.blit(text, ((WIDTH - text.get_width()) / 2, 0))

    def selected(self, x, y):
        for i in range(0, 9):
            for j in range(0, 9):
                self.boxes[i][j].selected = False

        self.boxes[x][y].select(True)
        return self.boxes[x][y]

    def do(self):
        self.bo.clear()
        for i in range(0, 9):
            self.bo.append([self.boxes[j][i].value for j in range(0, 9)])
        # print_board(self.bo)
        if self.validInput():
            solve(self.bo)
            for i in range(0, 9):
                for j in range(0, 9):
                    self.boxes[j][i].setVal(self.bo[i][j])
        else:
            print('Invalid Input')
        # print_board(self.bo)

    def validInput(self):
        compareSet = None
        compareList = None
        for i in range(0, 9):
            compareList = list()
            compareSet = set()
            for j in range(0, 9):
                if self.boxes[j][i].color == RED:
                    compareSet.add(self.boxes[j][i].value)
                    compareList.append(self.boxes[j][i].value)
            if len(compareList) != len(compareSet):
                return False

        for i in range(0, 9):
            compareList = list()
            compareSet = set()
            for j in range(0, 9):
                if self.boxes[i][j].color == RED:
                    compareSet.add(self.boxes[i][j].value)
                    compareList.append(self.boxes[i][j].value)
            if len(compareList) != len(compareSet):
                return False

        for i in range(0, 3):
            for j in range(0, 3):
                compareList = list()
                compareSet = set()
                for k in range(0, 3):
                    for l in range(0, 3):
                        if self.boxes[i * 3 + k][j * 3 + l].color == RED:
                            compareSet.add(self.boxes[i * 3 + k][j * 3 + l].value)
                            compareList.append(self.boxes[i * 3 + k][j * 3 + l].value)
                if len(compareList) != len(compareSet):
                    return False

        return True

    def clear(self):
        for j in range(0, 9):
            for i in range(0, 9):
                self.boxes[i][j].setColor(BLACK)
                self.boxes[i][j].setVal(0)


def list_duplicates(seq,board):
  seen = set()
  seen_add = seen.add
  # adds all elements it doesn't know yet to seen and all other to seen_twice
  seen_twice = set( x for x in seq if x in seen or seen_add(x) )
  # turn the set into a list (as requested)
  for num in seen_twice:
      for i in range(0, 9):
          for j in range(0, 9):
              if board.boxes[i][j].value == num:
                  board.boxes[i][j].setColor(BLUE)


def drawGrid(win):
    for i in range(0,9):
        pygame.draw.line(win, LIGHTGRAY, (70*i, 0), (70*i, WIDTH))
        if i%3 == 0:
            pygame.draw.line(win, BLACK, (70 * i, 0), (70 * i, WIDTH))

    for i in range(0,10):
        pygame.draw.line(win, LIGHTGRAY, (0, 70*i), (WIDTH, 70*i))
        if i%3 == 0:
            pygame.draw.line(win, BLACK, (0, 70 * i), (WIDTH, 70 * i))

    return None


def solve(bo):
    find = find_empty(bo)
    if not find:
        return True
    else:
        row, col = find

    for i in range(1,10):
        if valid(bo, i, (row, col)):
            bo[row][col] = i
            if solve(bo):
                return True

            bo[row][col] = 0

    return False


def valid(bo, num, pos):
    # Check row
    for i in range(len(bo[0])):
        if bo[pos[0]][i] == num and pos[1] != i:
            return False

    # Check column
    for i in range(len(bo)):
        if bo[i][pos[1]] == num and pos[0] != i:
            return False

    # Check box
    box_x = pos[1] // 3
    box_y = pos[0] // 3

    for i in range(box_y*3, box_y*3 + 3):
        for j in range(box_x * 3, box_x*3 + 3):
            if bo[i][j] == num and (i,j) != pos:
                return False

    return True


def find_empty(bo):
    for i in range(len(bo)):
        for j in range(len(bo[0])):
            if bo[i][j] == 0:
                return (i, j)  # row, col

    return None


def graphic(win):
    drawGrid(win)
    board.draw(win)
    buttonEnter.draw(win)
    buttonDel.draw(win)
    buttonQuit.draw(win)

def selectButton(str):
    buttonDel.setColor(BLUE)
    buttonEnter.setColor(BLUE)
    buttonQuit.setColor(BLUE)
    if str == 'DEL':
        buttonDel.setColor(BLACK)
    elif str == 'ENTER':
        buttonEnter.setColor(BLACK)
    elif str == 'QUIT':
        buttonQuit.setColor(BLACK)

def quitGame(board,win):
    selectButton('QUIT')
    graphic(win)
    pygame.display.update()
    pygame.time.wait(200)
    pygame.quit()
    sys.exit()

def enter(board,win, str = 'ENTER'):
    selectButton(str)
    graphic(win)
    pygame.display.update()
    for j in range(0, 9):
        for i in range(0, 9):
            if board.boxes[i][j].color == BLACK:
                board.boxes[i][j].setVal(0)
    board.do()

def clearBoard(board,win,str = 'DEL'):
    selectButton(str)
    graphic(win)
    pygame.display.update()
    board.clear()

def getKey(row, col, board, val):
    selectButton('')
    if row != None and col != None:
        board.boxes[row][col].setVal(val)
        if val:
            board.boxes[row][col].setColor(RED)
        else:
            board.boxes[row][col].setColor(BLACK)


win = pygame.display.set_mode((WIDTH, HEIGHT))
fpsClock = pygame.time.Clock()
pygame.font.init()
pygame.display.set_caption('Sudoku Solver')
board = Board()
buttonEnter = Button(0*CELL,'Solve')
buttonDel = Button(3*CELL, 'Clear')
buttonQuit = Button(6*CELL, 'Quit')


def main():
    key = 0
    select = None
    x = None
    y = None
    while True:
        win.fill(WHITE)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            keys = pygame.key.get_pressed()

            if event.type == MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if pos[1]>WIDTH:
                    if pos[0]>480 and pos[0]<550:
                        quitGame(board,win)
                    elif pos[0]>70 and pos[0]<150:
                        enter(board,win)
                    elif pos[0]>280 and pos[0]<360:
                        clearBoard(board,win)

                if pos[0] <= WIDTH and pos[1] <= WIDTH:
                    x = pos[0]//70
                    y = pos[1]//70
                if x!= None and y!= None:
                    board.selected(x, y)

            if keys[K_RIGHT] and x!= None and x<8 :
                x += 1
                board.selected(x, y)
            if keys[K_LEFT] and x!= None and x>0 :
                x -= 1
                board.selected(x, y)
            if keys[K_DOWN] and y!= None and y<8 :
                y += 1
                board.selected(x, y)
            if keys[K_UP] and x!= None and y>0 :
                y -= 1
                board.selected(x, y)

            if keys[K_0] or keys[K_KP0]:
                getKey(x, y, board, 0)
            if keys[K_1] or keys[K_KP1]:
                getKey(x, y, board, 1)
            if keys[K_2] or keys[K_KP2]:
                getKey(x, y, board, 2)
            if keys[K_3] or keys[K_KP3]:
                getKey(x, y, board, 3)
            if keys[K_4] or keys[K_KP4]:
                getKey(x, y, board, 4)
            if keys[K_5] or keys[K_KP5]:
                getKey(x, y, board, 5)
            if keys[K_6] or keys[K_KP6]:
                getKey(x, y, board, 6)
            if keys[K_7] or keys[K_KP7]:
                getKey(x, y, board, 7)
            if keys[K_8] or keys[K_KP8]:
                getKey(x, y, board, 8)
            if keys[K_9] or keys[K_KP9]:
                getKey(x, y, board, 9)
            if keys[K_DELETE]:
                getKey(x, y, board, 0)
           
            if keys[K_RETURN] or keys[K_KP_ENTER]:
                enter(board,win,'')
            if keys[K_ESCAPE]:
                clearBoard(board,win,'')

        graphic(win)
        pygame.display.update()
        fpsClock.tick(30)

if __name__ == ("__main__"):
    main()