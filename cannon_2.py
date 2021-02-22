import pygame
import random
import math
import time

pygame.init()

class Ball:
    GRAVITY = 0.30
    def __init__(self,radius,x,y,x_speed,y_speed,color,cannon=True):
        self.radius = radius
        self.x = x
        self.y = y
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.color = color
        self.cannon = cannon
        self.created_time = time.time()


    def update(self,container):

        current_time = time.time()
        self.x += self.x_speed
        self.y -= self.y_speed

        if self.cannon:
            self.y_speed -= Ball.GRAVITY

        if self.x + self.radius <= 0:
            container.remove(self)

        if self.cannon and (self.x - self.radius >= 400 or self.y - self.radius >= 400):
            container.remove(self)
    
    def draw(self):

        pygame.draw.circle(screen,self.color,(int(self.x),int(self.y)),self.radius)
    
    def collided(self,other):
        if isinstance(other,Ball):

            distance = math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)
            return distance <= self.radius * 2

        raise NotImplemented

RED = (255,0,0)
BLUE = (0,0,255)

screen = pygame.display.set_mode((400,400))
pygame.display.set_caption("CANNON GAME")
screen_width,screen_height = pygame.display.get_surface().get_size()

clock = pygame.time.Clock()

TARGET_SPEED_X = -1

ADD_TARGET = pygame.USEREVENT + 1
pygame.time.set_timer(ADD_TARGET,1000) #every 1000 milliseconds
done = False
balls = []
targets = []

while not done:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x,y = pygame.mouse.get_pos()
            
            y_speed = max((screen_height - y) // 22,5)
            x_speed = x // 22
            ball = Ball(10,0,screen_height,x_speed,y_speed,RED)
            balls.append(ball)
        elif event.type == ADD_TARGET:
            new_target = Ball(20,screen_width + 20,random.randint(20,screen_height - 20),TARGET_SPEED_X,0,BLUE,False)
            targets.append(new_target)


    
    for ball in list(balls):
        ball.update(balls)

    for target in list(targets):
        target.update(targets)
    
    for ball in balls: 
        for target in list(targets):
            if ball.collided(target):
                targets.remove(target)


        
    screen.fill((255,255,255))

    for ball in balls:
        ball.draw()

    for target in targets:
        target.draw()

    pygame.display.update()
    clock.tick(60)








