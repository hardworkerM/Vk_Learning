import os
s_clr = 'cls' if os.name == 'nt' else 'clear'


class TicTacGame:
    board = [
        ['.', '.', '.', '3'],
        ['.', '.', '.', '2'],
        ['.', '.', '.', '1'],
        ['a', 'b', 'c']
    ]

    def show_board(self):
        for strok in self.board:
            for i in range(len(strok)):
                print(strok[i], end='   ')
            print('')

    def validate_input(self):
        nums = ['3', '2', '1']
        lets = ['a', 'b', 'c']
        while True:
            coord = input('\nEnter coordinates: ')
            try:
                left, right = coord[0], coord[1]
                if left in nums:
                    left, right = right, left
                x = lets.index(left)
                y = nums.index(right)
                if not self.board[y][x] == '.' or len(coord) > 2:
                    raise ValueError()
            except (ValueError, IndexError):
                print('Input Error, try again')
            else:
                break
        return x, y

    def start_game(self):
        self.show_board()
        step = 0
        while step < 9:
            if step >= 5 and self.check_winner():
                break
            x, y = self.validate_input()
            step += 1
            if step % 2 == 0:
                self.board[y][x] = 'O'
            else:
                self.board[y][x] = 'X'

            os.system(s_clr)
            self.show_board()
        winner = self.check_winner()
        if winner:
            print(f'Winner is: {winner}!')
        else:
            print('Draw!')
        return winner

    def check_winner(self):
        # Проверка столбцов
        stack = []
        for i in range(3):
            stack.append(self.board[0][i])
            for j in range(1, 3):
                if self.board[j][i] == stack[j-1]:
                    stack.append(self.board[j][i])
                else:
                    break
            if len(stack) == 3 and '.' not in stack:
                if stack[0] == 'X':
                    winner = 'X'
                else:
                    winner = 'O'
                return winner
            stack = []
        # Проверка строк
        for i in range(3):
            stack.append(self.board[i][0])
            for j in range(1, 3):
                if self.board[i][j] == stack[j-1]:
                    stack.append(self.board[i][j])
                else:
                    break
            if len(stack) == 3 and '.' not in stack:
                if stack[0] == 'X':
                    winner = 'X'
                else:
                    winner = 'O'
                return winner
            stack = []
        # Проверка диагоналей: сначала \ ,потом /
        stack.append(self.board[0][0])
        for i in range(1, 3):
            if self.board[i][i] == stack[i - 1]:
                stack.append(self.board[i][i])
            else:
                break
        if len(stack) == 3 and '.' not in stack:
            if stack[0] == 'X':
                winner = 'X'
            else:
                winner = 'O'
            return winner

        stack = [self.board[2][0]]
        for i in range(1, 3):
            if self.board[2 - i][0 + i] == stack[i - 1]:
                stack.append(self.board[2 - i][0 + i])
            else:
                break
        if len(stack) == 3 and '.' not in stack:
            if stack[0] == 'X':
                winner = 'X'
            else:
                winner = 'O'
            return winner
        return False


if __name__ == "__main__":
    game = TicTacGame()
    game.start_game()
    input('Press enter to exit')
