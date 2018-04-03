# Import a library of functions called 'pygame'
import pygame
from math import pi
import math


def draw_point(x, y, color):
    pygame.draw.circle(screen, color, [int(x), int(y)], 2)


def draw_circle(x, y, r, color):
    c = 2 * pi / 401
    for j in range(0, r+1):
        for i in range(0, 401):
            draw_point(x + j*math.cos(i * c), y + j*math.sin(i * c), color)


# Initialize the game engine
pygame.init()

# Define the colors we will use in RGB format
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Set the height and width of the screen
size = [400, 300]
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Example code for the draw module")

# Loop until the user clicks the close button.
done = False
clock = pygame.time.Clock()

print("%-2d,%d" % (1, 2))

while not done:

    # This limits the while loop to a max of 10 times per second.
    # Leave this out and we will use all CPU we can.
    clock.tick(10)

    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop

    # All drawing code happens after the for loop and but
    # inside the main while done==False loop.

    # Clear the screen and set the screen background
    screen.fill(WHITE)
    # 从这里开始写
    draw_circle(200, 150, 40, BLACK)
    draw_circle(100, 150, 40, RED)
    draw_circle(300, 100, 50, GREEN)


    # Go ahead and update the screen with what we've drawn.
    # This MUST happen after all the other drawing commands.
    pygame.display.flip()

# Be IDLE friendly
pygame.quit()


