import asyncio
import json

import websockets


class GameState:

    game_id = None
    board = [
        [None, None, None],
        [None, None, None],
        [None, None, None]
    ]
    turn = 'X'
    next_turn = 'O'
    winner = None

    def __init__(self, game_id):
        self.game_id = game_id

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


active_games = {}


async def message_handler(websocket):
    async for message in websocket:
        print(message)
        message = json.loads(message)
        if message['type'] == 'new_game':
            active_games[message['game_id']] = GameState(message['game_id'])
            await websocket.send(json.dumps({
                'type': 'game_state',
                'game_id': message["game_id"],
                'game_state': active_games[message["game_id"]].__dict__
            }))
        elif message['type'] == 'do_turn':
            game = active_games[message['game_id']]
            game.do_turn(message['x'], message['y'])
            await websocket.send(json.dumps({
                'type': 'game_state',
                'game_id': message['game_id'],
                'game_state': game.__dict__
            }))
        elif message['type'] == 'restart':
            game = active_games[message['game_id']]
            game.restart()
            await websocket.send(json.dumps({
                'type': 'game_state',
                'game_id': message['game_id'],
                'game_state': game.__dict__
            }))
        elif message['type'] == 'get_games':
            await websocket.send(json.dumps({
                'type': 'games',
                'games': [game.__dict__ for game in active_games.values()]
            }))


async def main():
    async with websockets.serve(message_handler, "localhost", 8765):
        await asyncio.Future()  # run forever

asyncio.run(main())
