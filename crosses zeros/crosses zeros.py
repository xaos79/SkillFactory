'''Итоговое задание'''


def game():
    def print_matr(n):
        for i in n:
            print()
            for j in i:
                j = j.center(3)
                print(j, end=' ')
        print()

    def write_x_or_o(player):
        if player == 1:
            symbol = 'x'
        elif player == 2:
            symbol = 'o'
        try:
            coordinates = input(f'Игрок {player} вводит координаты поля для {symbol} (формат: х у).\t')
            if matr[int(coordinates.split()[1])][int(coordinates.split()[0])] == '-':
                matr[int(coordinates.split()[1])][int(coordinates.split()[0])] = symbol
            else:
                print('Сюда нельзя ставить. Выберите другое поле.')
                write_x_or_o(player)
        except IndexError:
            print('Введено некорректное значение. Пожалуста, введите значения поля '
                  'от 1 до 3 через пробел в формате: x o.')
            write_x_or_o(player)

    def check_win(n, symbol, player):
        y1 = symbol == n[1][1] and n[1][1] == n[1][2] == n[1][3]
        y2 = symbol == n[2][1] and n[2][1] == n[2][2] == n[2][3]
        y3 = symbol == n[3][1] and n[3][1] == n[3][2] == n[3][3]
        x1 = symbol == n[1][1] and n[1][1] == n[2][1] == n[3][1]
        x2 = symbol == n[1][2] and n[1][2] == n[2][2] == n[3][2]
        x3 = symbol == n[1][3] and n[1][3] == n[2][3] == n[3][3]
        d1 = symbol == n[1][1] and n[1][1] == n[2][2] == n[3][3]
        d2 = symbol == n[1][3] and n[1][3] == n[2][2] == n[3][1]

        if any([
            y1, y2, y3, x1, x2, x3, d1, d2
        ]):
            print(f'Победа игрока {player}!Игра окончена.')
            return True

    print(
        'Игра крестики - нолики. Каждый игрок вводит координаты выбранного поля в фомате: х у. '
        'Между символами вводится пробел.')
    matr = [['-' for i in range(4)] for j in range(4)]
    matr[0][0], matr[0][1], matr[0][2], matr[0][3] = "y\\x", '1', '2', '3'
    matr[1][0], matr[2][0], matr[3][0] = '1', '2', '3'

    print_matr(matr)
    counter = 0
    while True:
        write_x_or_o(1)
        print_matr(matr)
        counter += 1
        if check_win(matr, 'x', 1):
            break
        if counter == 9:
            print('Ничья!')
            break
        write_x_or_o(2)
        print_matr(matr)
        counter += 1
        if check_win(matr, 'o', 2):
            break


game()
