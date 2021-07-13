from random import choice, randint 


class BoardException(Exception):
    pass


class BoardOutException(BoardException):
    '''Точка за пределами доски'''
    pass


class BoardRepeatException(BoardException):
    '''Повторное использование точки'''
    pass


class WrongDot(Exception):
    pass


class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return f'Dot ({self.x}, {self.y})'


class Board:

    def __init__(self, hid=False):
        self.board = [[' O |' for i in range(6)] for j in range(6)]
        self.hid = hid
        self.ships = []
        self.alive = len(self.ships)
        self.busy = []
        self.count = 0

    def contour(self, ship):
        near = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        for d in ship.dots:
            for dx, dy in near:
                cur = Dot(d.x + dx, d.y + dy)
                if not (self.out(cur)) and cur not in self.busy:
                    self.busy.append(cur)

    def add_ship(self, ship):
        for dot in ship.dots:
            if dot in self.busy or self.out(dot):
                return False
        self.contour(ship)
        self.ships.append(ship)
        for dot in ship.dots:
            self.board[dot.y][dot.x] = ' K |'
            self.busy.append(dot)
        return True

    def show(self):
        res = ""
        res += "y\\x| 0 | 1 | 2 | 3 | 4 | 5 |"
        for i, row in enumerate(self.board):
            res += f"\n{i}  |" + "".join(row)

        if self.hid:
            res = res.replace(' K |', ' O |')
        return res

    def out(self, dot):
        if 0 > dot.x or dot.x > 5 or 0 > dot.y or dot.y > 5:
            return True

    def shot(self, dot):
        for ship in self.ships:
            if dot in ship.dots:
                ship.alive_dots -= 1
                self.board[dot.y][dot.x] = ' X |'
                if ship.alive_dots == 0:
                    self.count += 1
                    print('Корабль убит!')
                    return True
                else:
                    print('Корабль ранен!')
                    return True
        self.board[dot.y][dot.x] = ' T |'
        print('Промах!')
        return False

    def begin(self):
        self.busy = []


class Ship:

    def __init__(self, length=None, nouse=None, orientir=None):
        self.length = length
        self.nouse = nouse
        self.orientir = orientir
        self.alive_dots = length

    @property
    def dots(self):
        coord_ship = []
        for i in range(self.length):
            x = self.nouse.x
            y = self.nouse.y
            if self.orientir == 'vertical':
                y += i

            if self.orientir == 'gorizont':
                x += i

            coord_ship.append(Dot(x, y))
        return coord_ship


class Player:
    def __init__(self, my_board, enemy_board):
        self.my_board = my_board
        self.enemy_board = enemy_board

    def ask(self):
        raise NotImplementedError()

    def mode(self):
        while True:
            try:
                coord = self.ask()
                shot_by_desk = self.enemy_board.shot(coord)
                return shot_by_desk
            except BoardException as e:
                print(e)


class AI(Player):

    def ask(self):
        while True:
            try:
                x, y = randint(0, 5), randint(0, 5)
                dot = Dot(x, y)

                if self.enemy_board.board[dot.y][dot.x] == ' X |' or self.enemy_board.board[dot.y][dot.x] == ' T |':
                    raise BoardRepeatException
                else:
                    print(f"Ход компьютера: {dot.x + 1} {dot.y + 1}")
                    return dot
            except BoardRepeatException:
                pass


class User(Player):

    def ask(self):
        while True:
            try:
                x = input('Введите координату x и y через пробел\n')
                coordinate = x.split()
                if len(coordinate) != 2:
                    raise ValueError
                dot = Dot(int(coordinate[0]), int(coordinate[1]))
                if self.enemy_board.out(dot):
                    raise BoardOutException
                if self.enemy_board.board[dot.y][dot.x] == ' X |' or self.enemy_board.board[dot.y][dot.x] == ' T |':
                    raise BoardRepeatException
            except (ValueError, IndexError, TypeError, AttributeError):
                print('Пожалуйста, введите  два числа через пробел в формате: x y')
                pass
            except BoardOutException:
                print('Выстрел за пределы поля!')
                pass
            except BoardRepeatException:
                print('Нельзя стрелять в эту точку!')
                pass
            else:
                return dot


class Game:
    def __init__(self):
        pl = self.create_desk()
        co = self.create_desk()
        co.hid = True

        self.computer = AI(co, pl)
        self.user = User(pl, co)

    def greet(self):
        print('Приветствую Вас в игре морской бой!')
        print('формат выбора клетки для выстрела следующий: x y')
        print('значения вводятся через пробел')

    def random_board(self):
        ships = [3, 2, 2, 1, 1, 1, 1]
        field = Board()
        for i in ships:
            count = 0
            while True:
                try:
                    count += 1
                    if count > 1500:
                        return None
                    ship = Ship(i, Dot(randint(0, 5), randint(0, 5)), choice(['vertical', 'gorizont']))
                    ship_on_board = field.add_ship(ship)
                    if ship_on_board:
                        break
                except WrongDot:
                    pass
        field.begin()
        return field

    def create_desk(self):
        board = None
        while board is None:
            board = self.random_board()
        return board

    def loop(self):
        num = 0
        while True:
            print('Ваша доска')
            print(self.user.my_board.show())
            print('Доска противника')
            print(self.user.enemy_board.show())
            if num % 2 == 0:
                print("-" * 20)
                print('Ход игрока!')
                shot_shot = self.user.mode()
            else:
                print("-" * 20)
                print('Ход компьютера!')
                shot_shot = self.computer.mode()
            if shot_shot:
                num -= 1

            if self.user.my_board.count == 7:
                print('Компьтер победил!')
                break

            if self.computer.my_board.count == 7:
                print('Пользователь победил!')
                break
            num += 1

    def start(self):
        self.greet()
        self.loop()


game = Game()
game.start()
# game.user.my_board.show()
# game.user.enemy_board.show()
