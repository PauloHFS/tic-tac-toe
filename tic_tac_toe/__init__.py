import pygame

from tic_tac_toe.GameState import GameState

config = {
    'show_fps': False,
    'screen_size': {
        'width': 800,
        'height': 600
    },
    'background_color': (255, 255, 255),
    'tick_rate': 60
}

pygame.init()

clock = pygame.time.Clock()

size = width, height = config["screen_size"]["width"], config["screen_size"]["height"]
screen = pygame.display.set_mode(size, pygame.RESIZABLE)

game = GameState()

scene = 'menu'

while True:
    for event in pygame.event.get():
        if event.type == pygame.VIDEORESIZE:
            width, height = event.size
            size = width, height
            screen = pygame.display.set_mode(size, pygame.RESIZABLE)

        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit

        if scene == 'menu':
            if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    scene = 'game'

        elif scene == 'game':
            if event.type == pygame.MOUSEBUTTONDOWN:
                if game.winner is None:
                    x, y = event.pos
                    available_width, available_height = width / 3, height / 3
                    x = int(x // available_width)
                    y = int(y // available_height)
                    game.do_turn(x, y)
                else:
                    scene = 'menu'

    screen.fill(config["background_color"])

    if scene == 'menu':

        # Draw the title
        text = "Tic Tac Toe"
        font = pygame.font.SysFont("Arial", 50)
        text_surface = font.render(text, True, "black")
        text_rect = text_surface.get_rect(center=(width // 2, height // 2))
        screen.blit(text_surface, text_rect)

        # Draw the instructions
        text = "Press SPACE to start"
        font = pygame.font.SysFont("Arial", 20)
        text_surface = font.render(text, True, "black")
        text_rect = text_surface.get_rect(
            center=(width // 2, height // 2 + 50))
        screen.blit(text_surface, text_rect)

    elif scene == 'game':
        if game.winner is None:
            # Draw the board
            for x in range(3):
                for y in range(3):

                    available_width, available_height = width / 3, height / 3

                    rect = pygame.Rect(
                        x * available_width, y * available_height, available_width, available_height)
                    pygame.draw.rect(screen, "black", rect, 1)
                    if game.board[x][y] is not None:
                        text = game.board[x][y]
                        font = pygame.font.SysFont("Arial", 50)
                        text_surface = font.render(text, True, "black")
                        text_rect = text_surface.get_rect(center=rect.center)
                        screen.blit(text_surface, text_rect)
        else:
            # Draw the winner
            text = f"{game.winner} wins!"
            font = pygame.font.SysFont("Arial", 50)
            text_surface = font.render(text, True, "black")
            text_rect = text_surface.get_rect(center=(width // 2, height // 2))
            screen.blit(text_surface, text_rect)

    # show fps
    if config["show_fps"]:
        font = pygame.font.SysFont("Arial", 20)
        text_surface = font.render(
            f"FPS: {clock.get_fps():.2f}", True, "black")
        text_rect = text_surface.get_rect(center=(width // 2, 20))
        screen.blit(text_surface, text_rect)

    pygame.display.flip()
    clock.tick(config["tick_rate"])
