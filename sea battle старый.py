class BoardOutException(Exception):
    '''Точка за пределами доски'''
    pass


class BoardRepeatException(Exception):
    '''Повторная стрельба по точке'''
    pass


class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


class Board:
    ships = [
        {'name': 'long', 'quantity': 1, 'length': 3},
        {'name': 'middle', 'quantity': 2, 'length': 2},
        {'name': 'small', 'quantity': 4, 'length': 1}
    ]
    hid = True
    alive = len(ships)
    board = None

    def __init__(self, board):
        self.board = board

    def contour(self, ship):
        lst = ship.copy()
        for i in ship:
            cont = [[i[0], i[1] + 1], [i[0], i[1] - 1], [i[0] + 1, i[1]], [i[0] - 1, i[1]],
                    [i[0] + 1, i[1] + 1], [i[0] + 1, i[1] - 1], [i[0] - 1, i[1] - 1], [i[0] - 1, i[1] + 1]]
            lst.extend(cont)
        lst = [i for i in lst if 0 <= i[0] < 6 and 0 <= i[1] < 6]
        for i in lst:
            if self.board[i[0]][i[1]] == ' K |':
                return False
        else:
            return ship

    def add_ship(self, length):
        from random import choice
        choises = choice(['vertical', 'gorizont'])
        try:
            ship = []
            if choises == 'vertical':
                nouse_x, nouse_y = choice([n for n in range(6)]), \
                                   choice([q for q in range(6 - length + 1)])
                for j in range(length):
                    ship.append([nouse_y + j, nouse_x])
                if self.contour(ship) == ship:
                    for j in ship:
                        self.board[j[0]][j[1]] = ' K |'
                else:
                    return False
            elif choises == 'gorizont':
                nouse_x, nouse_y = choice([n for n in range(6 - length + 1)]), \
                                   choice([q for q in range(6)])
                for j in range(length):
                    ship.append([nouse_y, nouse_x + j])
                if self.contour(ship) == ship:
                    for j in ship:
                        self.board[j[0]][j[1]] = ' K |'
                else:
                    return False
        except:
            pass
        else:
            return True

    def show(self):
        if self.hid:
            print('y\\x ', "".join([str(i) + ' | ' for i in range(len(self.board))]))
            for num, elem in enumerate(self.board):
                print(f' {str(num)} |{"".join(elem)}')
            else:
                print()

    def out(self, dot):
        if 0 > dot.x or dot.x > 6 or 0 > dot.y or dot.y > 6:
            return True

    def shot(self, dot):
        if self.board[dot.y][dot.x] == ' K |':
            self.board[dot.y][dot.x] = ' X |'
            return True
        elif self.board[dot.y][dot.x] == ' O |':
            self.board[dot.y][dot.x] = ' T |'
            return False


class Ship:
    _dots = None

    def __init__(self, length=None, nouse=None, orientir=None, alive_dots=None):
        self.length = length
        self.nouse = nouse
        self.orientir = orientir
        self.alive_dots = alive_dots

    @property
    def dots(self):
        return self._dots

    @dots.setter
    def dots(self, value):
        self._dots = value


class Player:
    my_board = Board([[' O |' for i in range(6)] for j in range(6)])
    enemy_board = Board([[' O |' for i in range(6)] for j in range(6)])

    def ask(self):
        pass

    def mode(self, dot):
        self.enemy_board.shot(dot)


class AI(Player):

    def ask(self):
        from random import randint
        try:
            x, y = randint(0, 5), randint(0, 5)
            dot = Dot(x, y)

            if self.enemy_board.board[dot.y][dot.x] == ' X |' or self.enemy_board.board[dot.y][dot.x] == ' T |':
                raise BoardRepeatException
        except BoardRepeatException:
            self.ask()
        else:
            return dot


class User(Player):

    def ask(self):
        try:
            x = input('Введите координату x и y через пробел ')
            coordinate = x.split()
            dot = Dot(int(coordinate[0]), int(coordinate[1]))
            if len(coordinate) > 2:
                raise ValueError
            elif self.enemy_board.out(dot):
                raise BoardOutException
            elif self.enemy_board.board[dot.y][dot.x] == ' X |' or self.enemy_board.board[dot.y][dot.x] == ' T |':
                raise BoardRepeatException
        except (ValueError, IndexError, TypeError):
            print('Пожалуйста, введите  два числа через пробел в формате: x y')
            self.ask()
        except BoardOutException:
            print('Выстрел за пределы поля!')
            self.ask()
        except BoardRepeatException:
            print('Нельзя стрелять в эту точку!')
            self.ask()
        else:
            return dot


class Game:
    user = User()
    my_board = user.my_board
    computer = AI()
    computer_board = computer.enemy_board

    def random_board(self, board):
        for ship in board.ships:
            quantity = ship['quantity']
            for i in range(quantity):
                while True:
                    if board.add_ship(ship['length']):
                        break


g = Game()
print('his empty board')
g.computer_board.show()
print('his full board')
g.random_board(g.computer_board)
g.computer_board.show()
print('my empty board')
g.my_board.show()
print('my full board')
g.random_board(g.my_board)
g.my_board.show()
print('again his full board')
g.computer_board.show()

