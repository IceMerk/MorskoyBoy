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
        self.na4alo = na4alo
        self.dlina = dlina
        self.orentacia = orentacia
        self.hp = dlina

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


a = Dot(1, 1)
b = Dot(2, 1)
c = Dot(1, 1)

print([a, b, c])
