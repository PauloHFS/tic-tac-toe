import pygame

pygame.init()

clock = pygame.time.Clock()

size = width, height = 300, 300
screen = pygame.display.set_mode(size)

while True:
    # Handle use input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit

    screen.fill("white")

    pygame.display.flip()
    clock.tick(60)
