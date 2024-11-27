import pygame
import math
import os
import time
# Initialize Pygame
pygame.init()

# Set up display
width, height = 800, 800
max_frames = 20000
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Prime Spiral Visualization")

# Set up colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Number of points and prime marker array
n = 99999
p = [0] * n
t = 1

# Sieve of Eratosthenes to mark non-primes
for i in range(2, n):
    if p[i] == 0:
        for j in range(i * 2, n, i):
            p[j] = i

# Main loop
running = True
clock = pygame.time.Clock()
frame_count = 0
while running:
    if frame_count >= max_frames:
        running = False
        break
    screen.fill(BLACK)
    start = time.time()
    pointsDrawn = 0
    for i in range(3, n):
        if p[i] == 0:
            # Calculate position using polar coordinates
            x = int(math.sin(i * t) * (i / 99) + width / 2)
            y = int(math.cos(i * t) * (i / 99) + height / 2)

            # Draw the point
            if 0 <= x < width and 0 <= y < height:
                pygame.draw.circle(screen, WHITE, (x, y), 2)
                pointsDrawn += 1
    t += 1e-7
    frame_count += 1

    # Update the display
    pygame.display.flip()

    elapsed = (time.time() - start) * 1000
    with open("metrics_python.txt", "a") as f:
        f.write(
            f"Frame Time: {elapsed:.2f} ms, Points Drawn: {pointsDrawn}\n")

    # Cap the frame rate
    clock.tick(60)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

# Quit Pygame
pygame.quit()
