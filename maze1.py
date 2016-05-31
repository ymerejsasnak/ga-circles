import pygame
import random as r

SCR_SIZE = 800
GRID_SIZE = 20
CELL_SIZE = 40

WALL = '#'
START = 'S'
FINISH = 'F'
ZONES = [str(x) for x in range(1, 10)]  #strings '1' thru '9' part of determining fitness

WALL_COLOR = (20, 20 ,20)
FLOOR_COLOR = (230, 230, 230)
START_COLOR = (100, 200, 100)
FINISH_COLOR = (200, 100, 100)

GENOME_LENGTH = 200
NORTH = (0, -1)
EAST = (1, 0)
SOUTH = (0, 1)
WEST = (-1, 0)
GENES = (NORTH, EAST, SOUTH, WEST)



'''notes:
guys will be circles (that fit w/in cells...radius 1/2 cell size or maybe a bit less)
genome will have how many moves?  1000?
fitness will start at a set value (1000?) then subtract one for each movement (so getting
to finish faster is better), subtract more for hitting a wall, then give multiplier(?)
bonus for landing in better 'zones' (to reward getting closer to finish) 
'''







# maze representation ideas --- replace . with numbers representing zones to grade fitness
MAZE1 = ['####################',
         '#22222222222###FFFF#',
         '#22222222222###5555#',
         '#22222222222###5555#',
         '#1111###3333###5555#',
         '#1111###3333###5555#',
         '#1111###3333###5555#',
         '#1111###3333###5555#',
         '#1111###3333###5555#',
         '#1111###3333###5555#',
         '#1111###3333###5555#',
         '#1111###3333###5555#',
         '#1111###3333###5555#',
         '#1111###3333###5555#',
         '#1111###3333###5555#',
         '#1111###3333###5555#',
         '#1111###44444444444#',
         '#1111###44444444444#',
         '#SSSS###44444444444#',
         '####################']
         

class Grid:
    
    def __init__(self):
        self.cells = {}
    
    def load_grid(self, grid):
        # proper size and contents are assumed
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                self.cells[(j, i)] = grid[i][j]

    def draw_grid(self, screen):
        for position, contents in self.cells.items():
            x = position[0] * CELL_SIZE
            y = position[1] * CELL_SIZE
            size = CELL_SIZE
            if contents == WALL:
                color = WALL_COLOR
            elif contents == START:
                color = START_COLOR
            elif contents == FINISH:
                color = FINISH_COLOR
            else:
                color = FLOOR_COLOR
            pygame.draw.rect(screen, color, (x, y, size, size))
            
            #add grid
            pygame.draw.rect(screen, (0,0,0), (x, y, size, size), 1)


class Runner:
    
    def __init__(self):
        #temp - hard coded start spot:
        self.position = (1, 18)
        self.genome = [r.choice(GENES) for x in range(GENOME_LENGTH)]
        self.current = 0
        self.color = (r.randint(0, 150), r.randint(0, 100), r.randint(100, 250))
        
    def move(self, cells):
        direction = self.genome[self.current]
        self.current += 1
        target = (self.position[0] + direction[0], self.position[1] + direction[1])
        if cells[target] != WALL:
            self.position = target
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.position[0] * CELL_SIZE, self.position[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        
        
        
           
        
        
def run():
    pygame.init()
    screen = pygame.display.set_mode((SCR_SIZE, SCR_SIZE ))
    pygame.display.set_caption('GA Maze Solver')
    
    
    running = True
    
        
    grid = Grid()
    grid.load_grid(MAZE1)
        
    runners = [Runner() for x in range(10)]
        
    while running:
    
        screen.fill(FLOOR_COLOR)
        
        grid.draw_grid(screen)
        
        for runner in runners:
            runner.move(grid.cells)
            runner.draw(screen)
        
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
               running = False
        
        
        pygame.display.flip()
        
        pygame.time.delay(100)

run()



