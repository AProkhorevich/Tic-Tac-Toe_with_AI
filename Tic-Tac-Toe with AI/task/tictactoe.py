import exceptions
import random

global x_player
global o_player


class TicTacToe:
    levels = ['easy', 'medium', 'hard', 'user']

    def __init__(self):
        self.board = []
        for i in range(3):
            row = []
            for j in range(3):
                row.append(' ')
            self.board.append(row)

    def print(self):
        print('---------')
        for i in range(3):
            print(f"| {' '.join(self.board[i])} |")
        print('---------')

    def check_status(self):
        # Columns
        for x in range(3):
            if self.board[0][x] == self.board[1][x] == self.board[2][x]:
                if self.board[0][x] != ' ':
                    return self.board[0][x]
        # Rows
        for row in self.board:
            if row[0] == row[1] == row[2]:
                if row[0] != ' ':
                    return row[0]
        # Diagonals
        if (self.board[0][0] == self.board[1][1] == self.board[2][2]) or \
                (self.board[2][0] == self.board[1][1] == self.board[0][2]):
            if self.board[1][1] != ' ':
                return self.board[1][1]

        # Draw
        if not any([string.count(' ') for string in self.board]):
            # print("Draw")
            return "Draw"

        return False


class Player:
    def __init__(self, symbol):
        self.symbol = symbol

    def make_turn(self):
        illegal_turn = True
        while illegal_turn:
            try:
                player_turn = [int(x) - 1 for x in input('Enter the coordinates: ').split()]
                if len(player_turn) == 0:
                    continue
                if any([x > 2 for x in player_turn]) or any([x < 0 for x in player_turn]):
                    raise exceptions.CoordinatesRange
                if game.board[player_turn[0]][player_turn[1]] != ' ':
                    raise exceptions.Occupied
                make_turn_n_print(player_turn, self.symbol)
                illegal_turn = False
            except exceptions.Occupied as ex:
                print(ex)
            except ValueError as ex:
                print('You should enter numbers!')
            except exceptions.CoordinatesRange as ex:
                print(ex)


class Bot:
    def __init__(self, symbol):
        self.symbol = symbol

    def make_turn(self, symbol=None):
        if symbol is None:
            symbol = self.symbol
        illegal_turn_game = True
        while illegal_turn_game:
            try:
                turn = [random.randint(0, 3), random.randint(0, 3)]
                if any([x > 2 for x in turn]):
                    raise exceptions.CoordinatesRange
                if game.board[turn[0]][turn[1]] != ' ':
                    raise exceptions.Occupied

                make_turn_n_print(turn, symbol, self.level)

                illegal_turn_game = False
            except exceptions.Occupied as ex:
                pass
            except ValueError as ex:
                pass
            except exceptions.CoordinatesRange as ex:
                pass

    def chek_for_win(self):
        # rows
        for y in range(3):
            if sum(game.board[y][x].count(self.symbol) for x in range(3)) == 2:
                for x in range(3):
                    if game.board[y][x] == ' ':
                        return y, x
        # columns
        for x in range(3):
            if sum(game.board[y][x].count(self.symbol) for y in range(3)) == 2:
                for y in range(3):
                    if game.board[y][x] == ' ':
                        return y, x
        # diagonals
        if sum(game.board[x][x].count(self.symbol) for x in range(3)) == 2:
            for x in range(3):
                if game.board[x][x] == ' ':
                    return x, x
        return None

    def chek_for_lose(self):
        opponents_symbol = 'X' if self.symbol == 'O' else 'O'
        # rows
        for y in range(3):
            if sum(game.board[y][x].count(opponents_symbol) for x in range(3)) == 2:
                for x in range(3):
                    if game.board[y][x] == ' ':
                        return y, x
        # columns
        for x in range(3):
            if sum(game.board[y][x].count(opponents_symbol) for y in range(3)) == 2:
                for y in range(3):
                    if game.board[y][x] == ' ':
                        return y, x
        # diagonals
        if sum(game.board[x][x].count(opponents_symbol) for x in range(3)) == 2:
            for x in range(3):
                if game.board[x][x] == ' ':
                    return x, x

        if sum(game.board[2 - x][x].count(opponents_symbol) for x in range(3)) == 2:
            for x in range(3):
                if game.board[2 - x][x] == ' ':
                    return 2 - x, x
        return None


class EasyBot(Bot):
    level = 'easy'

    def __int__(self, symbol):
        super().__init__(symbol)


class MediumBot(Bot):
    level = 'medium'

    def __int__(self, symbol):
        super().__init__(symbol)

    def make_turn(self, symbol=None):
        if symbol is None:
            symbol = self.symbol

        if self.chek_for_win():
            y, x = self.chek_for_win()
            make_turn_n_print((y, x), self.symbol, MediumBot.level)
            return
        if self.chek_for_lose():
            y, x = self.chek_for_lose()
            make_turn_n_print((y, x), self.symbol, MediumBot.level)
            return
        EasyBot.make_turn(self, self.symbol)


class HardBot(Bot):
    level = 'hard'

    def __init__(self, symbol):
        super().__init__(symbol)

    scores_table = {
        'X': 1,
        'O': -1,
        'Draw': 0
    }

    def minimax(self, depth, isMaximizing):
        result = game.check_status()
        if result:
            score = self.scores_table[result]
            return score
        if isMaximizing:
            best_score = -10000
            for i in range(3):
                for j in range(3):
                    if game.board[i][j] == ' ':
                        game.board[i][j] = self.symbol
                        score = self.minimax(depth + 1, False)
                        game.board[i][j] = ' '
                        best_score = max(score, best_score)
            return best_score
        else:
            best_score = 10000
            for i in range(3):
                for j in range(3):
                    if game.board[i][j] == ' ':
                        game.board[i][j] = 'X' if self.symbol == 'O' else 'O'
                        score = self.minimax(depth + 1, True)
                        game.board[i][j] = ' '
                        best_score = min(score, best_score)
            return best_score

    def make_turn(self, symbol=None):
        if symbol is None:
            symbol = self.symbol

        if game.board[1][1] == ' ':
            make_turn_n_print((1, 1), symbol)
            return

        if self.chek_for_lose():
            make_turn_n_print(self.chek_for_lose(), symbol)
            return
        if self.chek_for_win():
            make_turn_n_print(self.chek_for_win(), symbol)
            return
        best_score = -10000
        best_move = (0, 0)
        for i in range(3):
            for j in range(3):
                if game.board[i][j] == ' ':
                    game.board[i][j] = symbol
                    score = self.minimax(0, False)
                    game.board[i][j] = ' '
                    if score > best_score:
                        best_score = score
                        best_move = (i, j)

        make_turn_n_print(best_move, symbol)


def make_turn_n_print(coordinates, symbol, level=None):
    if level is not None:
        print(f'Making move level "{level}"')
    game.board[coordinates[0]][coordinates[1]] = symbol
    game.print()


def game_start(state):
    bad_parameters = True
    while bad_parameters:
        try:
            if state[0] == 'exit':
                return False
            else:
                global x_player
                global o_player

                if state[1] == 'user':
                    x_player = Player('X')
                elif state[1] == 'easy':
                    x_player = EasyBot('X')
                elif state[1] == 'medium':
                    x_player = MediumBot('X')
                elif state[1] == 'hard':
                    x_player = HardBot('X')
                else:
                    raise exceptions.BadParameters
                if state[2] == 'user':
                    o_player = Player('O')
                elif state[2] == 'easy':
                    o_player = EasyBot('O')
                elif state[2] == 'medium':
                    o_player = MediumBot('O')
                elif state[2] == 'hard':
                    o_player = HardBot('O')
                else:
                    raise exceptions.BadParameters

            bad_parameters = False
        except Exception as ex:
            print('Bad parameters!')
            state = input().split()

    return False


if __name__ == '__main__':
    while True:
        try:
            state = input().split()
            if len(state) == 0:
                continue
            if state[0] == 'exit':
                break
            elif state[0] == 'start' and len(state) == 3 and state[1] in TicTacToe.levels and state[2] in TicTacToe.levels:
                game = TicTacToe()
                game_finished = game_start(state)
                if game_finished:
                    break
                game.print()
                while not game_finished:
                    x_player.make_turn()
                    game_finished = game.check_status()
                    if game_finished:
                        break
                    o_player.make_turn()
                    game_finished = game.check_status()
                if game_finished == 'Draw':
                    print('Draw')
                else:
                    print(f"{game_finished} wins")

            else:
                raise exceptions.BadParameters
        except exceptions.BadParameters as ex:
            print(ex)
