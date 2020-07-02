import pygame, sys

rows = int(input("Please Enter the number of rows:- "))
columns = int(input("Please Enter the number of columns:- "))
start = list(map(lambda x: int(x)-1, input("Please enter the starting points' coordinates (x, y):- ").split(',')))
goal = list(map(lambda x: int(x)-1, input("Please enter the starting points' coordinates (x, y):- ").split(',')))
dimen = max([rows, columns])
size = 600 // dimen
Astar = True


pygame.init()
black, white, red, green, blue, pink = (0, 0, 0), (255, 255, 255), (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 8, 127)
scW, scH = 1280, 720
screen = pygame.display.set_mode((scW, scH))
pygame.display.set_caption("Path Finder")
pygame.mouse.set_cursor(*pygame.cursors.diamond)
clock = pygame.time.Clock()

class Box:
    def __init__(self, i, j, buffX, buffY, blocksize):
        self.i = i
        self.j = j
        self.position = pygame.Rect(buffX+(self.j*(blocksize+(blocksize*0.2))), buffY+(self.i*(blocksize+(blocksize*0.2))), blocksize, blocksize)
        self.wall, self.open, self.closed, self.path = False, False, False, False
        self.prev = None
        self.cost = 0
        self.children = []
        self.placeholder = False

    def show(self):
        if self.wall: pygame.draw.rect(screen, black, self.position)
        elif self.placeholder: pygame.draw.rect(screen, pink, self.position)
        elif self.open: pygame.draw.rect(screen, green, self.position)
        elif self.closed: pygame.draw.rect(screen, red, self.position)
        elif self.path: pygame.draw.rect(screen, blue, self.position)
        pygame.draw.rect(screen, black, self.position, 2)

    def getChildren(self):
        i, j = self.i, self.j
        if (i-1 >= 0) and (not mygrid.boxes[i-1][j].wall):
            self.children.append(mygrid.boxes[i-1][j])
        if (i+1 < rows) and (not mygrid.boxes[i+1][j].wall):
            self.children.append(mygrid.boxes[i+1][j])
        if (j-1 >= 0) and (not mygrid.boxes[i][j-1].wall):
            self.children.append(mygrid.boxes[i][j-1])
        if (j+1 < columns) and (not mygrid.boxes[i][j+1].wall):
            self.children.append(mygrid.boxes[i][j+1])

    def getCost(self):
        h = abs(goal[0] - self.i) + abs(goal[1] - self.j)
        g = abs(start[0] - self.i) + abs(start[1] - self.j)
        self.cost = h + g

    def blit_text(self, text, color):
        font = pygame.font.SysFont('comicsans', self.position[2]//3, italic=5, bold=5)
        text = font.render(text, True, color)
        center = (self.position[0]+(self.position[2]//2), self.position[1]+(self.position[3]//2))
        textRect = text.get_rect(center=center)
        screen.blit(text, textRect)

class Grid:
    def __init__(self, rows, columns, blocksize=50):
        buffX, buffY = int((scW/2)-(((blocksize+(blocksize*0.2))*columns)/2)), int((scH/2)-(((blocksize+(blocksize*0.2))*rows)/2))
        self.boxes = [[Box(i, j, buffX, buffY, blocksize) for j in range(columns)] for i in range(rows)]

    def show(self):
        [[box.show() for box in line] for line in self.boxes]

    def waller(self, pos):
        for i in range(len(self.boxes)):
            for j in range(len(self.boxes[i])):
                if self.boxes[i][j].position.collidepoint(pos):
                    if self.boxes[i][j] != startbox and self.boxes[i][j] != goalbox:
                        self.boxes[i][j].wall = not self.boxes[i][j].wall

    def make_path(self, box):
        path_length = 0
        while box:
            box.path, box.closed = True, False
            box = box.prev
            path_length += 1

solved, start_solve = False, False
mygrid = Grid(rows, columns, size)
startbox, goalbox = mygrid.boxes[start[0]][start[1]], mygrid.boxes[goal[0]][goal[1]]
startbox.placeholder = goalbox.placeholder = True
openSet, closedSet = [startbox], []

def solve(hueristic):
    global solved
    if hueristic:
        if not openSet:
            print("Path not found")
            return
        lowestIndex = 0
        for i in range(len(openSet)):
            if openSet[i].cost < openSet[lowestIndex].cost:
                lowestIndex = i
        
        current = openSet.pop(lowestIndex)
        current.open = False
        current.closed = True
        
        if current == goalbox:
            mygrid.make_path(current)
            solved = True
            return
        else:
            for child in current.children:
                if child not in closedSet and child not in openSet:
                    child.getCost()
                    child.open = True
                    child.prev = current
                    openSet.append(child)
            closedSet.append(current)
    else:
        if not openSet:
            print("Path not found")
            return
        current = openSet.pop(0)
        current.open = False
        current.closed = True
        
        if current == goalbox:
            mygrid.make_path(current)
            solved = True
            return
        else:
            for child in current.children:
                if child not in closedSet and child not in openSet:
                    child.open = True
                    child.prev = current
                    openSet.append(child)
            closedSet.append(current)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                sys.exit()
            elif event.key == pygame.K_SPACE:
                [[box.getChildren() for box in line] for line in mygrid.boxes]
                start_solve = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            mygrid.waller(pos)

    screen.fill(white)
    if start_solve and not solved: solve(Astar)
    mygrid.show()

    pygame.display.flip()
    clock.tick(100)
