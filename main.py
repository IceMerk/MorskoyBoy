from random import randint


class BoardOutException(Exception):  # Исключение, когда стреляем за доску
    def __str__(self):
        return '❌ Вы стреляете за доску ❌'


class BoardUseException(Exception):  # Исключение, когда стреляем туда же
    def __str__(self):
        return f'❌ Вы уже сюда стреляли ❌'


class ShipWrongException(Exception):  # Исключение для расстоновки кораблей
    pass


class Dot:  # Класс точек
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):  # Сравнение двух точек по x и y
        return self.x == other.x and self.y == other.y

    def __repr__(self):  # Отладочная информация
        return f'Dot({self.x}, {self.y})'


class Ship:  # Класс кораблей
    def __init__(self, na4alo, dlina, orentacia):
        self.na4alo = na4alo  # Начальная точка корабля
        self.dlina = dlina  # Длина корабля
        self.orentacia = orentacia  # горизонтально или вертикально
        self.hp = dlina  # Жизни корабля равные его длине

    @property  # Декоратор, определяет свойства, можем вызывать функцию без call
    def dots(self):
        ship_dots = []  # Список в который собираем корабли
        for i in range(self.dlina):  # Собираем корабль больше 1
            other_x = self.na4alo.x
            other_y = self.na4alo.y

            if self.orentacia == 0:  # Смотрим как расположен корабль
                other_x += i
            elif self.orentacia == 1:
                other_y += i

            ship_dots.append(Dot(other_x, other_y))

        return ship_dots  # Возвращаем корабль

    def popal(self, shot):  # Проверка на попадание в корабль
        return shot in self.dots


class Board:
    def __init__(self, size=6, hid=False):
        self.size = size  # Размер поля
        self.hid = hid  # Нужно ли скрывать тип bool
        self.field = [['О'] * 6 for i in range(self.size)]  # Поле
        self.ships = []  # Спискок кораблей
        self.busy_ships = []  # Список выстрелов мимо/по кораблям
        self.death_ships = 0  # Список убитых кораблей

    def add_ship(self, ship): # Добавление корабля на доску
        for dot in ship.dots: # В цикле проверяем точки: в поле ли они и нету ли её в занятых
            if self.out(dot) or dot in self.busy_ships:
                raise Exception('Сюда нельзя ставить') # Если есть, то кидаем Ошибку
        for dot in ship.dots: # Если всё норм
            self.field[dot.x][dot.y] = '■' # Заменяем О на точку корабля
            self.busy_ships.append(dot) # Добавляем в список занятых точек кораблей
        self.ships.append(ship) # Добавляем в список кораблей
        self.contour(ship)  # рисуем контур корабля

    def contour(self, ship, view=False):
        radius = [
            (1, -1), (1, 0), (1, 1),
            (0, -1), (0, 0), (0, 1),
            (-1, -1), (-1, 0), (-1, 1)
        ]
        for dot in ship.dots: # Берем точки корабля
            for dot_x, dot_y in radius: # Берем список radius
                check = Dot(dot.x + dot_x, dot.y + dot_y) # Прогоняем корабль по radius
                if not (self.out(check)) and check not in self.busy_ships: # Если не входит в диапазон и нету в
                    # списке точек/кораблей
                    if view: # Если корабль подбит, рисуем возле него точки
                        self.field[check.x][check.y] = '.'
                    self.busy_ships.append(check) # Добавляем в занятые

    def __str__(self):  # Отрисовка поля
        v = '  | 1 | 2 | 3 | 4 | 5 | 6 |'  # Поле с цифрами сверху
        for i, k in enumerate(self.field):  # Рисуем поле и добавляем цифры сбоку
            v += f'\n{i + 1} | {" | ".join(k)} | '

        if self.hid:  # Если нужно скрыть корабли hid = True
            v = v.replace('■', 'О')
        return v

    def out(self, dot): # Проверяем находится ли точка за пределами доски
        return not all([0 <= dot.x <= self.size, 0 <= dot.y <= self.size])

    def shot(self, dot): # Метод выстрела
        if self.out(dot): # Если выстрел вне доски
            raise BoardOutException()
        if dot in self.busy_ships: # Если выстрел уже был
            raise BoardUseException()

        self.busy_ships.append(dot) # Если всё ок, добавляем в список занятых

        for ship in self.ships: # Ищем в списке кораблей
            if dot in ship.popal(dot): # Сверяем - попали или нет
                ship.hp -= 1 # Если попали, то уменьшаем хп у корабля
                self.field[dot.x][dot.y] = 'X'
                if ship.hp == 0: # Если хп не осталось
                    self.death_ships += 1 # Пополняем счетчик мертвых
                    self.contour(ship, view=True) # Рисуем вокруг него точки
                    print('Корабль потоплен')
                    return False
                else:
                    print('Корабль подбит')
                    return True

        self.field[dot.x][dot.y] = '.' # Если попали Мимо
        print('Мимо')
        return False

    def start(self): # Обнуляем список занятого
        self.busy_ships = []

class Player:
    def __init__(self, board, board_second):
        self.board = board
        self.board_second = board_second

    def ask(self): # Долго гуглил это, пока не нашел исключение
        raise NotImplementedError()

    def move(self): # Спрашиваем игрока сделать выстрел
        while True:
            try:
                t = self.ask() # Запрос выстрела
                r = self.board_second.shot(t) # Проверка на доске противника
                return r
            except Exception as e:
                print(e)

class AI(Player):
    pass

class User(Player):
    pass


b = Board()

b.add_ship(Ship(Dot(1, 2), 4, 0))
b.add_ship(Ship(Dot(0, 0), 2, 1))
print(b)
