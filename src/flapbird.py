import pygame

# Initialize Pygame
pygame.init()

# Set up some constants
WIDTH, HEIGHT = 800, 600
BIRD_SIZE = 32
PIPE_SPACING = 128
PIPE_WIDTH = 32
PIPE_HEIGHT = 400
GRAVITY = 1

# Set up some variables
bird_pos = [WIDTH // 2, HEIGHT // 2]
pipe_pos = [WIDTH, 0]
pipe_vel = -4 

# Create the window
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Set up the clock
clock = pygame.time.Clock()

# Game loop
running = True
while running:
    # Event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update the bird's position
    bird_pos[1] += GRAVITY

    # Check for collisions with the pipes
    if bird_pos[0] + BIRD_SIZE > pipe_pos[0] and bird_pos[0] < pipe_pos[0] + PIPE_WIDTH:
        if bird_pos[1] + BIRD_SIZE > pipe_pos[1] or bird_pos[1] < pipe_pos[1] + PIPE_HEIGHT:
            print("Collision!")
            running = False

    # Update the pipe's position
    pipe_pos[0] += pipe_vel

    # Draw everything
    screen.fill((30, 30, 30))
    pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(bird_pos[0], bird_pos[1], BIRD_SIZE, BIRD_SIZE))
    pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(pipe_pos[0], pipe_pos[1], PIPE_WIDTH, PIPE_HEIGHT))

    # Flip the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Clean up
pygame.quit()