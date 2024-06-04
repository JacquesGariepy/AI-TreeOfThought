import pygame
import time

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Cool Animation')
white = (255, 255, 255)
red = (255, 0, 0)
x, y = 50, 50
dx, dy = 5, 5
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    x += dx
    y += dy   

    if x <= 0 or x >= 750:
        dx = -dx
    if y <= 0 or y >= 550:
        dy = -dy    

    screen.fill(white)    
    pygame.draw.circle(screen, red, (x, y), 30)
    pygame.display.update()
    time.sleep(0.02)

pygame.quit()
