import pygame
import random
import heapq
from collections import deque

pygame.init()

# ---------- CONFIG ----------
WIDTH, HEIGHT = 800, 800
ROWS, COLS = 20, 20
CELL = WIDTH // COLS

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("GOOD PERFORMANCE TIME APP")

# Colors
WHITE = (255,255,255)
BLACK = (0,0,0)
GREY = (200,200,200)
GREEN = (0,200,0)
BLUE = (0,0,255)
RED = (200,0,0)
YELLOW = (255,255,0)
PURPLE = (128,0,128)

DYNAMIC_PROB = 0.02
DELAY = 50

# Movement order (clockwise + all diagonals)
MOVES = [
    (-1,0),  # Up
    (-1,1),  # Top
    (0,1),   # Right
    (1,1),   # Bottom Right
    (1,0),   # Bottom
    (1,-1),  # Bottom Left
    (0,-1),  # Left
    (-1,-1)  # Top Left
]

# ---------- GRID ----------
def make_grid():
    grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]
    return grid

grid = make_grid()

start = (ROWS-3, COLS-5)
target = (ROWS-3, 2)

def draw():
    WIN.fill(WHITE)

    for r in range(ROWS):
        for c in range(COLS):
            color = WHITE
            if grid[r][c] == -1:
                color = RED
            elif grid[r][c] == 1:
                color = YELLOW
            elif grid[r][c] == 2:
                color = GREY
            elif grid[r][c] == 3:
                color = PURPLE

            pygame.draw.rect(WIN, color, (c*CELL, r*CELL, CELL, CELL))
            pygame.draw.rect(WIN, BLACK, (c*CELL, r*CELL, CELL, CELL), 1)

    pygame.draw.rect(WIN, GREEN, (start[1]*CELL, start[0]*CELL, CELL, CELL))
    pygame.draw.rect(WIN, BLUE, (target[1]*CELL, target[0]*CELL, CELL, CELL))

    pygame.display.update()

def neighbors(node):
    r,c = node
    for dr,dc in MOVES:
        nr,nc = r+dr, c+dc
        if 0 <= nr < ROWS and 0 <= nc < COLS:
            if grid[nr][nc] != -1:
                yield (nr,nc)

def spawn_dynamic():
    if random.random() < DYNAMIC_PROB:
        r = random.randint(0,ROWS-1)
        c = random.randint(0,COLS-1)
        if (r,c) not in [start,target]:
            grid[r][c] = -1

def reconstruct(parent):
    node = target
    while node in parent:
        r,c = node
        grid[r][c] = 3
        node = parent[node]

# ---------- ALGORITHMS ----------

def bfs():
    q = deque([start])
    parent = {}
    visited = {start}

    while q:
        spawn_dynamic()
        node = q.popleft()

        if node == target:
            reconstruct(parent)
            return

        for nb in neighbors(node):
            if nb not in visited:
                visited.add(nb)
                parent[nb] = node
                q.append(nb)
                r,c = nb
                grid[r][c] = 1

        r,c = node
        grid[r][c] = 2
        draw()
        pygame.time.delay(DELAY)

def dfs():
    stack = [start]
    parent = {}
    visited = {start}

    while stack:
        spawn_dynamic()
        node = stack.pop()

        if node == target:
            reconstruct(parent)
            return

        for nb in neighbors(node):
            if nb not in visited:
                visited.add(nb)
                parent[nb] = node
                stack.append(nb)
                r,c = nb
                grid[r][c] = 1

        r,c = node
        grid[r][c] = 2
        draw()
        pygame.time.delay(DELAY)

def ucs():
    pq = [(0,start)]
    parent = {}
    cost = {start:0}

    while pq:
        spawn_dynamic()
        g,node = heapq.heappop(pq)

        if node == target:
            reconstruct(parent)
            return

        for nb in neighbors(node):
            new = g+1
            if nb not in cost or new < cost[nb]:
                cost[nb] = new
                parent[nb] = node
                heapq.heappush(pq,(new,nb))
                r,c = nb
                grid[r][c] = 1

        r,c = node
        grid[r][c] = 2
        draw()
        pygame.time.delay(DELAY)

def dls(limit=20):
    stack = [(start,0)]
    parent = {}
    visited = {start}

    while stack:
        spawn_dynamic()
        node,depth = stack.pop()

        if node == target:
            reconstruct(parent)
            return

        if depth < limit:
            for nb in neighbors(node):
                if nb not in visited:
                    visited.add(nb)
                    parent[nb] = node
                    stack.append((nb,depth+1))
                    r,c = nb
                    grid[r][c] = 1

        r,c = node
        grid[r][c] = 2
        draw()
        pygame.time.delay(DELAY)

def iddfs():
    for depth in range(1,ROWS*COLS):
        dls(depth)

def bidirectional():
    q1 = deque([start])
    q2 = deque([target])

    parent1 = {}
    parent2 = {}

    visited1 = {start}
    visited2 = {target}

    while q1 and q2:
        spawn_dynamic()

        node1 = q1.popleft()
        for nb in neighbors(node1):
            if nb not in visited1:
                visited1.add(nb)
                parent1[nb] = node1
                q1.append(nb)
                if nb in visited2:
                    return

        node2 = q2.popleft()
        for nb in neighbors(node2):
            if nb not in visited2:
                visited2.add(nb)
                parent2[nb] = node2
                q2.append(nb)
                if nb in visited1:
                    return

        draw()
        pygame.time.delay(DELAY)

# ---------- MAIN LOOP ----------
def reset():
    global grid
    grid = make_grid()

def main():
    run = True
    while run:
        draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                reset()
                if event.key == pygame.K_1: bfs()
                if event.key == pygame.K_2: dfs()
                if event.key == pygame.K_3: ucs()
                if event.key == pygame.K_4: dls()
                if event.key == pygame.K_5: iddfs()
                if event.key == pygame.K_6: bidirectional()
                if event.key == pygame.K_r: reset()

    pygame.quit()

main()
