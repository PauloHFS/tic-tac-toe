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
