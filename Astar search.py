import pygame, sys
from tkinter import *
from tkinter.ttk import Combobox

screen = Tk()
screen.geometry('280x260')
screen.title("PathFinder")

def get_form_info():
    global rows, columns, startx, starty, endx, endy, start, goal, Astar
    try:
        rows = int(rows.get())
        columns = int(columns.get())
        start = (int(startx.get())-1, int(starty.get())-1)
        goal = (int(endx.get())-1, int(endy.get())-1)
        if combo.get()[0] == 'A': Astar = True
        else: Astar = False
    except:
        print("Error")
    screen.destroy()

Label(screen, text="Path Finding Algorithm Visualizer", width="300", height='3', font='comicsans').pack()
Label(screen, text='Size of the grid        Rows:').place(x=10, y=60)
Label(screen, text='Cols:').place(x=180, y=60)
Label(screen, text='Starting Coordinates     X:').place(x=10, y=100)
Label(screen, text='Y:').place(x=195, y=100)
Label(screen, text='Ending Coordinates       X:').place(x=10, y=140)
Label(screen, text='Y:').place(x=195, y=140)
Label(screen, text='Algorithm: ').place(x=10, y=180)

rows, columns, startx, starty, endx, endy = StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar()
Entry(screen, textvariable=rows).place(x=150, y=62, width='30')
Entry(screen, textvariable=columns).place(x=210, y=62, width='30')
Entry(screen, textvariable=startx).place(x=150, y=102, width='30')
Entry(screen, textvariable=starty).place(x=210, y=102, width='30')
Entry(screen, textvariable=endx).place(x=150, y=142, width='30')
Entry(screen, textvariable=endy).place(x=210, y=142, width='30')
combo = Combobox(screen, width=20, values=['A* Algorithm', 'Dijkstras\'  Algorithm'])
combo.place(x=80, y=182)
Button(screen, text='Generate Maze', bg="grey", width='20', height='2', command=get_form_info).place(x=60, y=210)

screen.mainloop()

#rows, columns, start, goal, Astar = 30, 30, (0, 0), (25, 25), True #debugging
dimen = max([rows, columns])
size = 600 // dimen

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
        self.cost, self.g, self.h = 0, 0, 0
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
        self.g = g
        self.h = h

class Grid:
    def __init__(self, rows, columns, blocksize=50):
        buffX, buffY = int((scW/2)-(((blocksize+(blocksize*0.2))*columns)/2)), int((scH/2)-(((blocksize+(blocksize*0.2))*rows)/2))
        self.boxes = [[Box(i, j, buffX, buffY, blocksize) for j in range(columns)] for i in range(rows)]

    def show(self):
        [[box.show() for box in line] for line in self.boxes]
        #self.show_costs() #use this to see the costs the algorithm assigns

    def waller(self, pos):
        for i in range(len(self.boxes)):
            for j in range(len(self.boxes[i])):
                if self.boxes[i][j].position.collidepoint(pos):
                    if self.boxes[i][j] != startbox and self.boxes[i][j] != goalbox:
                        self.boxes[i][j].wall = not self.boxes[i][j].wall

    def make_path(self, box):
        self.path_length = 0
        while box:
            box.path, box.closed = True, False
            box = box.prev
            self.path_length += 1
        self.pop_up()
    
    def pop_up(self):
        global solved
        screen = Tk()
        screen.geometry('300x80')
        if solved:
            screen.title('Path Found')
            Label(screen, text=f"The Algorithm found a path between the two Nodes.\nThe shortest distance is {self.path_length} blocks", width="300", height='3', font='comicsans', wraplength='300').pack()
        else:
            screen.title('Path Not Found')
            Label(screen, text="The Algorithm could not find a path between the two Nodes", width="300", height='3', font='comicsans', wraplength='300').pack()
        solved = True
        screen.mainloop()

solved, start_solve = False, False
mygrid = Grid(rows, columns, size)
startbox, goalbox = mygrid.boxes[start[0]][start[1]], mygrid.boxes[goal[0]][goal[1]]
startbox.placeholder = goalbox.placeholder = True
openSet, closedSet = [startbox], []

def solve(hueristic):
    global solved
    if hueristic:
        if not openSet:
            mygrid.pop_up()
            return

        lowestIndex = openSet.index(min(openSet, key=lambda x: x.h))    
        current = openSet.pop(lowestIndex)
        current.open = False
        current.closed = True
        
        if current == goalbox:
            solved = True
            mygrid.make_path(current)
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
            mygrid.pop_up()
            return
        current = openSet.pop(0)
        current.open = False
        current.closed = True
        
        if current == goalbox:
            solved = True
            mygrid.make_path(current)
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
