import pygame

config = {
    'show_fps': True,
    'screen_size': {
        'width': 300,
        'height': 300
    },
    'background_color': (255, 255, 255),
    'tick_rate': 60
}

pygame.init()

clock = pygame.time.Clock()

size = width, height = config["screen_size"]["width"], config["screen_size"]["height"]
screen = pygame.display.set_mode(size)


class GameState:

    board = [
        [None, None, None],
        [None, None, None],
        [None, None, None]
    ]
    turn = 'X'
    next_turn = 'O'
    winner = None

    def do_turn(self, x, y):
        if self.board[x][y] is None:
            self.board[x][y] = self.turn
            self.turn, self.next_turn = self.next_turn, self.turn

            # Check for winner
            for i in range(3):
                if self.board[i][0] == self.board[i][1] == self.board[i][2] is not None:
                    self.winner = self.board[i][0]
                if self.board[0][i] == self.board[1][i] == self.board[2][i] is not None:
                    self.winner = self.board[0][i]
                if self.board[0][0] == self.board[1][1] == self.board[2][2] is not None:
                    self.winner = self.board[0][0]
                if self.board[0][2] == self.board[1][1] == self.board[2][0] is not None:
                    self.winner = self.board[0][2]

            # check for draw
            if self.winner is None and all(all(x is not None for x in row) for row in self.board):
                self.winner = "draw"

    def restart(self):
        self.board = [
            [None, None, None],
            [None, None, None],
            [None, None, None]
        ]
        self.turn = 'X'
        self.next_turn = 'O'
        self.winner = None


game = GameState()

while True:
    # Handle use input
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if game.winner is None:
                x, y = event.pos
                x //= 100
                y //= 100
                game.do_turn(x, y)
            else:
                game.restart()
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit

    screen.fill(config["background_color"])

    if game.winner is None:
        # Draw the board
        for x in range(3):
            for y in range(3):
                rect = pygame.Rect(x * 100, y * 100, 100, 100)
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

    if config["show_fps"]:
        # show fps
        font = pygame.font.SysFont("Arial", 20)
        text_surface = font.render(
            f"FPS: {clock.get_fps():.2f}", True, "black")
        text_rect = text_surface.get_rect(center=(width // 2, 20))
        screen.blit(text_surface, text_rect)

    pygame.display.flip()
    clock.tick(config["tick_rate"])
