import sys
import pygame
import random as r

SCR_SIZE = 800
GRID_SIZE = 20
CELL_SIZE = 40

WALL = '#'
START = 'S'
FINISH = 'F'
ZONES = [str(x) for x in range(10)]  #strings '0' thru '9' part of determining fitness

WALL_COLOR = (20, 20 ,20)
FLOOR_COLOR = (230, 230, 230)
START_COLOR = (100, 200, 100)
FINISH_COLOR = (200, 100, 100)

GENOME_LENGTH = 300
NORTH = (0, -1)
EAST = (1, 0)
SOUTH = (0, 1)
WEST = (-1, 0)
GENES = (NORTH, EAST, SOUTH, WEST)

GENERATION_SIZE = 100
REPRODUCER_GROUP_SIZE = 20
MUTATION_RATE = 10



'''notes:
maybe completely change genome so that it is a series of instructions for what to do
(nesw) depending on 4 cell neighborhood (nesw) states (wall, not visited, visited) 
[this will be 4 (neighbors) * 3 possible states = 12 'situations' to have instructions for]
[but maybe also check zone rating for < or > if not visited...so all states are
wall, visited, not-visited lower rating, not-visited same rating, and not-visted greater rating,
which is 5 * 4 neighbors = 20 possible situations...still easy to code for...DO IT!]
therefore it can naturally select for better strategies rather than better
meaningless strings of random directions
(this should be able to evolve better solutions, especially to harder maps like MAZE3)

'''


 
MAZE1 = ['####################',
         '#33333333333###FFFF#',
         '#33333333333###9999#',
         '#33333333444###9999#',
         '#3333###4444###9999#',
         '#2222###4444###9999#',
         '#2222###4444###9999#',
         '#2222###4444###8888#',
         '#2222###4444###8888#',
         '#1111###4444###8888#',
         '#1111###4444###8888#',
         '#1111###4444###8888#',
         '#1111###5555###7777#',
         '#1111###5555###7777#',
         '#1111###5555###7777#',
         '#0000###5555###7777#',
         '#0000###55556667777#',
         '#0000###55666666666#',
         '#S000###55666666666#',
         '####################']

MAZE2 = ['####################',
         '#45555666777888999F#',
         '#445555666777888999#',
         '#444555566677788899#',
         '#444455556667778889#',
         '#344445555666777888#',
         '#334444555566677788#',
         '#333444455556667778#',
         '#333344445555666777#',
         '#233334444555566677#',
         '#223333444455556667#',
         '#222333344445555666#',
         '#122233334444555566#',
         '#112223333444455556#',
         '#111222333344445555#',
         '#111122233334444555#',
         '#000112223333444455#',
         '#000111222333344445#',
         '#S00111122233334444#',
         '####################']

MAZE3 = ['####################',
         '####################',
         '##2222##5555555555##',
         '##2##2##4##5#5#5#5##',
         '##1##2##4##5#5#5#5##',
         '##1##2##4##5#5#5#6##',
         '##1##2##4##6#6#6#6##',
         '##1##2##4##6#6#6#6##',
         '##1##2##4##6#6#6#6##',
         '##1##2##4##6#6#6#6##',
         '##1##3##4##6#6#6#6##',
         '##1##3##4##6#6#6#6##',
         '##1##3##4##6#6#6#7##',
         '##1##3##4##7#7#7#7##',
         '##1##3##4##7#7#7#8##',
         '##1##3##4##7#7#8#9##',
         '##1##3##4##7#8#9#9##',
         '##S##3333##888999F##',
         '####################',
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
        self.visited = set()

        self.fitness = 0

    def move(self, cells, turn):
        if self.finished:
            return
            
        direction = self.genome[turn]
        target = (self.position[0] + direction[0], self.position[1] + direction[1])
        if cells[target] != WALL:
            self.visited.update(self.position) 
            self.position = target
            if self.position in self.visited:
                self.fitness -= turn
            elif cells[self.position] in ZONES:
                self.fitness += int(cells[self.position])
            
        elif cells[target] == WALL:
            self.fitness -= 20
            
        if cells[self.position] == FINISH:
            self.finished = True
            self.fitness = 1000000 - turn  # major fitness bonus for finishing (less turns = better bonus)
        elif turn == GENOME_LENGTH - 1 and cells[self.position] in ZONES:
            self.fitness += int(cells[self.position]) * 10
    
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
        self.generation.sort(key=lambda runner: runner.fitness, reverse=True)
        
        next_gen = []
        for i in range(GENERATION_SIZE):
            parents = r.sample(self.generation[:REPRODUCER_GROUP_SIZE], 2)
            genome_split = r.randrange(GENOME_LENGTH // 4, GENOME_LENGTH // 4 * 3)
            child_genome = parents[0].genome[:genome_split] + parents[1].genome[genome_split:]
            
            #mutate
            for gene in child_genome:
                if MUTATION_RATE > r.randrange(100):
                    gene = r.choice(GENES)
                    
            
            
            next_gen.append(Runner(start_position, child_genome))
            
        self.generation = next_gen
        self.generation_count += 1
           
        
        
def run():
    pygame.init()
    screen = pygame.display.set_mode((SCR_SIZE, SCR_SIZE ))
    pygame.display.set_caption('GA Maze Solver')
    
        
    grid = Grid()
    grid.load_grid(MAZE2)
    
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
        
        print('gen: ', str(ga.generation_count), '\t\t', 'best fit: ', int(ga.generation[0].fitness))
        ga.next_generation(grid.start_position)

run()



