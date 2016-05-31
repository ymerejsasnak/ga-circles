import pygame
import math
import random as r


SCR_SIZE = 800
TEXT_SIZE = 20

BG_COLOR = (200, 200, 200)
RED = (200, 0, 0)
GREEN = (0, 200, 0)

GA_CIRCLE_COLOR = (200, 50, 50)

MEDIAN_FIELD_RADIUS = 40
FIELD_RADIUS_VARIATION = 5
FIELD_CIRCLE_COUNT = 30

GENERATION_SIZE = 1000
REPRODUCER_GROUP_SIZE = 100
POSITION_MUTATION_AMOUNT = 400
RADIUS_MUTATION_AMOUNT = 2
MUTATION_RATE = 10

DEFAULT_SPEED = 1 


def overlap(circle1, circle2):
    distance = ((circle2.x - circle1.x) ** 2 + (circle2.y - circle1.y) ** 2) ** 0.5
    return circle1.radius + circle2.radius - distance
        
def make_field():
    field = [FieldCircle()]
    count = 1
    
    while count < FIELD_CIRCLE_COUNT:
        new_circle = FieldCircle()
        no_overlap = True
        
        for circle in field:
            if overlap(new_circle, circle) >= 0:
                no_overlap = False
        
        if no_overlap:
            field.append(new_circle)
            count += 1
    
    return field
    
    
class FieldCircle:
    
    def __init__(self):
        self.radius = r.randint(MEDIAN_FIELD_RADIUS - FIELD_RADIUS_VARIATION,
                                MEDIAN_FIELD_RADIUS + FIELD_RADIUS_VARIATION)
        self.x = r.randint(self.radius, SCR_SIZE - self.radius)
        self.y = r.randint(self.radius, SCR_SIZE - self.radius)
    
    def draw(self, surface):
        pygame.draw.circle(surface, (0,0,0), (self.x, self.y), self.radius, 2)


class FitCircle:
    
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.fitness = radius
        self.color = RED
    
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
        
 
class GA:
    
    def __init__(self):
        self.generation_count = 1
        self.generation = []
        for i in range(GENERATION_SIZE):
            radius = r.randrange(20)
            self.generation.append(FitCircle(r.randint(radius, SCR_SIZE - radius),
                                            r.randrange(radius, SCR_SIZE - radius),
                                            radius))
    

            
    def fitness_calculation(self, field):
        # calculate fitness of circles
        for circle in self.generation:
            for field_circle in field:
                #fitness is radius size with a harsh penalty for overlaps
                penalty = overlap(circle, field_circle) * 2
                if penalty > 0:
                    circle.fitness -= penalty
                
    
    def fitness_sort(self):                    
        self.generation.sort(key=lambda circle: circle.fitness, reverse=True)
    
    def next_generation(self):
        next_gen = []
        for i in range(GENERATION_SIZE):
            parents = r.sample(self.generation[:REPRODUCER_GROUP_SIZE], 2)
            child_radius = r.choice(parents).radius
            child_x = r.choice(parents).x
            child_y = r.choice(parents).y
            
            # mutate
            if r.randint(1, 100) < MUTATION_RATE:
                child_radius += r.randrange(RADIUS_MUTATION_AMOUNT)
            #if r.randint(1, 100) < MUTATION_RATE:
                child_x = (child_x + r.randint(-POSITION_MUTATION_AMOUNT, POSITION_MUTATION_AMOUNT)) % SCR_SIZE
                child_y = (child_y + r.randint(-POSITION_MUTATION_AMOUNT, POSITION_MUTATION_AMOUNT)) % SCR_SIZE
                
            # keep child in bounds
            if child_x - child_radius < 0:
                child_x = child_radius
            elif child_x + child_radius > SCR_SIZE - 1:
                child_x = SCR_SIZE - child_radius - 1
            if child_y - child_radius < 0:
                child_y = child_radius
            elif child_y + child_radius > SCR_SIZE - 1:
                child_y = SCR_SIZE - child_radius - 1
            
            next_gen.append(FitCircle(child_x, child_y, child_radius))
            
        self.generation = next_gen
        self.generation_count += 1
        
            
        
    
    


def run():
    # Initialize and create screen object.
    pygame.init()
    screen = pygame.display.set_mode((SCR_SIZE, SCR_SIZE + TEXT_SIZE))
    pygame.display.set_caption('Genetic Algorithm')
    
    running = True
    speed = DEFAULT_SPEED
    
    field = make_field()
    ga = GA()
    
       
    # Start the main loop
    while running:
        
        screen.fill(BG_COLOR)
    
        for circle in field:
            circle.draw(screen)
        
        ga.fitness_calculation(field)
        ga.fitness_sort()
        ga.generation[0].draw(screen) # only showing the most fit each gen
                
        # Display generation and radius (fitness is usually radius)
        string1 = 'Generation: ' + str(ga.generation_count) 
        string2 = 'Largest Radius: ' + str(ga.generation[0].radius)
        string3 = 'Simulation Speed: ' + str(speed // 100)
        font = pygame.font.Font(None, 20)
        text1 = font.render(string1, 1, (10, 10, 10))
        screen.blit(text1, (0, SCR_SIZE))
        text2 = font.render(string2, 1, (10, 10, 10))
        screen.blit(text2, (SCR_SIZE // 4, SCR_SIZE))
        text3 = font.render(string3, 1, (10, 10, 10))
        screen.blit(text3, (SCR_SIZE // 2, SCR_SIZE))
        
        
        pygame.display.flip()
        
        pygame.time.wait(1000 - speed)
        
        ga.next_generation()
    
        # Watch for keyboard and mouse events.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                speed = min(speed + 100, 1000)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                speed = max(speed - 100, 1)
            
                
        
        

run()
