import sys
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

GENERATION_SIZE = 20
REPRODUCER_GROUP_SIZE = 5



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
         '#S111###44444444444#',
         '####################']
         

class Grid:
    
    def __init__(self):
        self.cells = {}
    
    def load_grid(self, grid):
        # proper size and contents are assumed
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                self.cells[(x, y)] = grid[y][x]
                if grid[y][x] == START:
                    self.start_position = (x, y)
                    

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
    
    def __init__(self, start_position, genome):
        self.position = start_position
        self.genome = genome
        self.color = (r.randint(0, 150), r.randint(0, 100), r.randint(100, 250))
        
        self.finished = False

        self.fitness = 1000 # for now, will have to tweak this...

    def move(self, cells, turn):
        direction = self.genome[turn]
        target = (self.position[0] + direction[0], self.position[1] + direction[1])
        if cells[target] == WALL:
            self.fitness -= 10
        else:
            self.position = target
            self.fitness -= 1
            
        if cells[target] == FINISH:
            self.finished == True
            self.fitness *= 10
            
        if turn == GENOME_LENGTH - 1 and self.position in ZONES:
            self.fitness *= int(cells[self.position])
    
    def draw(self, screen):
        size = CELL_SIZE
        x = self.position[0] * size + size // 2
        y = self.position[1] * size + size // 2
        radius = size // 3
        pygame.draw.circle(screen, self.color, (x, y), radius)
        
        
class GA:
    
    def __init__(self, start_position):
        self.generation = []
        for runner in range(GENERATION_SIZE):
            genome = [r.choice(GENES) for x in range(GENOME_LENGTH)]
            self.generation.append(Runner(start_position, genome))
        self.generation_count = 1
    
    def next_generation(self, start_position):
        # sort based on fitness
        self.generation.sort(key=lambda runner: runner.fitness)
        
        next_gen = []
        for i in range(GENERATION_SIZE):
            parents = r.sample(self.generation[:REPRODUCER_GROUP_SIZE], 2)
            genome_split = r.randint(GENOME_LENGTH // 3, GENOME_LENGTH // 3 * 2)
            child_genome = parents[0].genome[:genome_split] + parents[1].genome[genome_split:]
            
            
            # mutate
            
            
            next_gen.append(Runner(start_position, child_genome))
            
        self.generation = next_gen
        self.generation_count += 1
           
        
        
def run():
    pygame.init()
    screen = pygame.display.set_mode((SCR_SIZE, SCR_SIZE ))
    pygame.display.set_caption('GA Maze Solver')
    
        
    grid = Grid()
    grid.load_grid(MAZE1)
    
    ga = GA(grid.start_position)
        
    while True:
    
        for turn in range(GENOME_LENGTH):
            
            screen.fill(FLOOR_COLOR)
            grid.draw_grid(screen)
        
            for runner in ga.generation:
                runner.move(grid.cells, turn)
                runner.draw(screen)
            
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                   running = sys.exit()
            
            #show generation, turn, best fitness, speed?
            
            pygame.display.flip()
            
            #pygame.time.delay(100)
        
        ga.next_generation(grid.start_position)

run()



