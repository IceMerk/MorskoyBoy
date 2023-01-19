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
        self.na4alo = na4alo # Начальная точка корабля
        self.dlina = dlina # Длина корабля
        self.orentacia = orentacia # горизонтально или вертикально
        self.hp = dlina # Жизни корабля равные его длине

    @property  # Декоратор, определяет свойства, можем вызывать функцию без call
    def dots(self):
        ship_dots = []  # Список в который собираем корабли
        for i in range(self.dlina):  # Собираем корабль больше 1
            other_x = self.na4alo.x
            other_y = self.na4alo.y

            if self.orentacia == 0:  # Смотрим как расположен корабль
                other_x += 1
            else:
                other_y += 1

            ship_dots.append(Dot(other_x, other_y))

        return ship_dots  # Возвращаем корабль

    def popal(self, shot): # Проверка на попадание в корабль
        return shot in self.dots

class Board:
    def __init__(self, size=6, hid=False):
        self.size = size # Размер поля
        self.hid = hid # Нужно ли скрывать тип bool
        self.field = [['О']*6 for i in range(self.size)] # Поле
        self.ships = [] # Спискок кораблей
        self.busy_ships = [] # Список выстрелов мимо/по кораблям
        self.death_ships = 0 # Список убитых кораблей

    def add_ship(self):
        pass

    def contour(self):
        pass

    def __str__(self): # Отрисовка поля
        v = ' | 1 | 2 | 3 | 4 | 5 | 6 |' # Поле с цифрами сверху
        for i, k in enumerate(self.field): # Рисуем поле и добавляем цифры сбоку
            v += f'\n{i + 1} | {"|".join(k)} |'

        if self.hid: # Если нужно скрыть корабли hid = True
            v = v.replace('■', 'О')

    def out(self):
        pass

    def shot(self):
        pass

s = Ship(Dot(1, 2), 4, 0)
print(s.popal(Dot(2, 2)))