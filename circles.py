import pygame
import math
import random as r


SCR_WIDTH = 400
SCR_HEIGHT = 400

BG_COLOR = (200, 200, 200)

GA_CIRCLE_COLOR = (200, 50, 50)

MEDIAN_FIELD_RADIUS = 20
FIELD_RADIUS_VARIATION = 10
FIELD_CIRCLE_COUNT = 20


def check_overlap(circle1, circle2):
    distance = ((circle2.x - circle1.x) ** 2 + (circle2.y - circle1.y) ** 2) ** 0.5
    if distance < circle1.radius + circle2.radius:
        return True
    else:
        return False
        
def make_field():
    field = [FieldCircle()]
    count = 1
    
    while count < FIELD_CIRCLE_COUNT:
        new_circle = FieldCircle()
        no_overlap = True
        
        for circle in field:
            if check_overlap(new_circle, circle):
                no_overlap = False
        
        if no_overlap:
            field.append(new_circle)
            count += 1
    
    return field
    
    
class FieldCircle:
    
    def __init__(self):
        self.radius = r.randint(MEDIAN_FIELD_RADIUS - FIELD_RADIUS_VARIATION,
                                MEDIAN_FIELD_RADIUS + FIELD_RADIUS_VARIATION)
        self.x = r.randint(0 + self.radius, SCR_WIDTH - self.radius)
        self.y = r.randint(0 + self.radius, SCR_HEIGHT - self.radius)
    
    def draw(self, surface):
        pygame.draw.circle(surface, (0,0,0), (self.x, self.y), self.radius, 1)
        


def run_game():
    # Initialize game and create screen object.
    pygame.init()
    screen = pygame.display.set_mode((SCR_WIDTH, SCR_HEIGHT))
    pygame.display.set_caption('Genetic Algorithm')
    
    running = True
    
    screen.fill(BG_COLOR)
    
    field = make_field()
    
    for circle in field:
        circle.draw(screen)
    
    # Start the main loop for the game.
    while running:
    
        # Watch for keyboard and mouse events.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
               running = False
        
        # Make the most recently drawn screen visible
        pygame.display.flip()

run_game()
